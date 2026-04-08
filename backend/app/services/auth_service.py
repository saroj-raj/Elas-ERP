"""
Authentication service using Supabase Auth
Handles signup, login, password reset, and session management
"""
import logging
import os
import secrets
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.db.supabase_client import get_supabase, get_supabase_admin

# --------------- auth file logger ---------------
_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

auth_logger = logging.getLogger("auth")
auth_logger.setLevel(logging.DEBUG)
if not auth_logger.handlers:
    _handler = RotatingFileHandler(
        os.path.join(_LOG_DIR, "auth.log"),
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=3,
    )
    _handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
    )
    auth_logger.addHandler(_handler)


class AuthService:
    """Service for handling authentication operations"""

    @staticmethod
    def _raise_signup_error(error_message: str) -> None:
        normalized = error_message.lower()
        auth_logger.warning("Signup error: %s", error_message)

        if "rate limit" in normalized or "too many requests" in normalized:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Email rate limit exceeded. "
                    "Please wait a few minutes and try again."
                )
            )

        if (
            "already registered" in normalized
            or "already been registered" in normalized
            or "already exists" in normalized
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "This email is already registered. "
                    "If you already have an account, please log in or reset your password."
                )
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {error_message}"
        )

    @staticmethod
    def _build_profile(user_data: Dict[str, Any]) -> Dict[str, Any]:
        business = user_data.get("businesses") or {}
        return {
            "id": user_data["id"],
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "role": user_data["role"],
            "business_id": user_data["business_id"],
            "business_name": business.get("name"),
            "avatar_url": user_data.get("avatar_url"),
            "is_active": user_data.get("is_active"),
        }

    @staticmethod
    def _get_user_profile(user_id: str) -> Dict[str, Any]:
        auth_logger.debug("Fetching profile for user_id=%s", user_id)
        admin_client = get_supabase_admin()
        user_response = admin_client.table("users").select(
            "*, businesses(*)"
        ).eq("id", user_id).single().execute()

        if not user_response.data:
            auth_logger.error("Profile not found for user_id=%s", user_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )

        auth_logger.debug("Profile loaded for user_id=%s email=%s", user_id, user_response.data.get("email"))
        return user_response.data

    @staticmethod
    def _update_last_login(user_id: str) -> None:
        admin_client = get_supabase_admin()
        admin_client.table("users").update({
            "last_login": datetime.utcnow().isoformat()
        }).eq("id", user_id).execute()
    
    @staticmethod
    async def signup_business_owner(
        email: str,
        password: str,
        full_name: str,
        business_name: str,
        industry: Optional[str] = None,
        size: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sign up a new business owner (admin)
        Creates both the business and the admin user
        """
        auth_logger.info("SIGNUP attempt email=%s business=%s", email, business_name)
        try:
            auth_admin = get_supabase_admin()
            db_admin = get_supabase_admin()
            
            # Step 1: Create auth user in Supabase Auth
            auth_response = auth_admin.auth.admin.create_user({
                "email": email,
                "password": password,
                "user_metadata": {
                    "full_name": full_name
                },
                "email_confirm": True,
            })

            if getattr(auth_response, "error", None):
                error_message = str(auth_response.error.message or auth_response.error)
                AuthService._raise_signup_error(error_message)

            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create user account"
                )
            
            user_id = auth_response.user.id
            
            # Step 2: Create business
            business_data = {
                "name": business_name,
                "industry": industry,
                "size": size,
                "is_active": True
            }
            business_response = db_admin.table("businesses").insert(business_data).execute()
            
            if not business_response.data:
                # Rollback: delete auth user if business creation fails
                auth_admin.auth.admin.delete_user(user_id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create business"
                )
            
            business_id = business_response.data[0]["id"]
            
            # Step 3: Create user profile (links to auth.users)
            user_data = {
                "id": user_id,
                "business_id": business_id,
                "email": email,
                "full_name": full_name,
                "role": "admin",
                "is_active": True,
                "last_login": datetime.utcnow().isoformat()
            }
            user_response = db_admin.table("users").insert(user_data).execute()
            
            if not user_response.data:
                # Rollback: delete business and auth user
                db_admin.table("businesses").delete().eq("id", business_id).execute()
                auth_admin.auth.admin.delete_user(user_id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user profile"
                )
            
            auth_logger.info("SIGNUP success email=%s user_id=%s", email, user_id)
            return {
                "user": auth_response.user,
                "session": getattr(auth_response, "session", None),
                "business_id": business_id,
                "business_name": business_name
            }
            
        except HTTPException:
            raise
        except Exception as e:
            auth_logger.exception("SIGNUP exception email=%s", email)
            AuthService._raise_signup_error(str(e))
    
    @staticmethod
    async def login(email: str, password: str) -> Dict[str, Any]:
        """Login user and return session"""
        auth_logger.info("LOGIN attempt email=%s", email)
        try:
            auth_client = get_supabase()
            
            # Authenticate with Supabase
            auth_response = auth_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not auth_response.user or not auth_response.session:
                auth_logger.warning("LOGIN failed – invalid credentials email=%s", email)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            user_id = auth_response.user.id
            auth_logger.debug("LOGIN auth ok user_id=%s, fetching profile", user_id)
            user_data = AuthService._get_user_profile(user_id)
            AuthService._update_last_login(user_id)
            
            auth_logger.info("LOGIN success email=%s user_id=%s", email, user_id)
            return {
                "user": auth_response.user,
                "session": auth_response.session,
                "profile": AuthService._build_profile(user_data)
            }
            
        except HTTPException:
            raise
        except Exception as e:
            auth_logger.exception("LOGIN exception email=%s", email)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(e)}"
            )
    
    @staticmethod
    async def logout(access_token: str) -> Dict[str, str]:
        """Logout user (invalidate session)"""
        try:
            supabase = get_supabase()
            supabase.auth.sign_out()
            return {"message": "Logged out successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Logout failed: {str(e)}"
            )
    
    @staticmethod
    async def get_current_user(access_token: str) -> Dict[str, Any]:
        """Get current user from access token"""
        auth_logger.debug("GET_CURRENT_USER validating token")
        try:
            supabase = get_supabase()
            
            # Get user from token
            user_response = supabase.auth.get_user(access_token)
            
            if not user_response.user:
                auth_logger.warning("GET_CURRENT_USER – invalid/expired token")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            
            user_id = user_response.user.id
            auth_logger.debug("GET_CURRENT_USER token valid user_id=%s", user_id)
            user_data = AuthService._get_user_profile(user_id)
            return AuthService._build_profile(user_data)
            
        except HTTPException:
            raise
        except Exception as e:
            auth_logger.exception("GET_CURRENT_USER exception")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    @staticmethod
    async def send_password_reset(email: str) -> Dict[str, str]:
        """Send password reset email"""
        try:
            supabase = get_supabase()
            supabase.auth.reset_password_email(email)
            return {"message": "Password reset email sent"}
        except Exception as e:
            # Don't reveal if email exists
            return {"message": "If the email exists, a reset link has been sent"}
    
    @staticmethod
    async def update_password(access_token: str, new_password: str) -> Dict[str, str]:
        """Update user password"""
        try:
            supabase = get_supabase()
            supabase.auth.update_user({
                "password": new_password
            })
            return {"message": "Password updated successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update password: {str(e)}"
            )
