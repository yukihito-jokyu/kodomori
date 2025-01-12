from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.type import DangersCreate, DangersResponse

from ..session_db import get_db
from ..setup import DANGERS

router = APIRouter(
    prefix="/dangers",
    tags=["dangers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    return {"message": "here is dangers!"}


# 危険エリアの設定ページ（管理者）post
@router.post("/add_danger", response_model=DangersResponse)
def create_danger(danger: DangersCreate, db: Session = Depends(get_db)):
    db_danger = DANGERS(
        danger_id=danger.danger_id,
        coordinate_p1=danger.coordinate_p1,
        coordinate_p2=danger.coordinate_p2,
        coordinate_p3=danger.coordinate_p3,
        coordinate_p4=danger.coordinate_p4,
    )
    db.add(db_danger)
    db.commit()
    db.refresh(db_danger)
    return db_danger
