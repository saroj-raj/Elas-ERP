from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard")
def get_dashboard():
    return {"widgets": []}
