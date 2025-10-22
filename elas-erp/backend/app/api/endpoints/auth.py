"""Auth endpoints placeholder"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/auth/ping")
def ping():
    return {"auth": "ok"}
