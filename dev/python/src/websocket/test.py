from fastapi import APIRouter

router = APIRouter(
    prefix="/ws/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)
