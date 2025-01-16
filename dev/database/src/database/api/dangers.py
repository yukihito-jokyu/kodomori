from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.type import DangersCreate, DangersResponse
from fastapi.responses import JSONResponse

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


# camera_idに対応するdanger_idを取得するAPI
@router.get("/get_danger_id", response_model=DangersResponse)
def get_dange_id(camera_id: int, db: Session = Depends(get_db)):
    return db.query(DANGERS).filter(DANGERS.camera_id == camera_id).first()


# 危険エリアを保存するAPI
@router.post("/add_danger")
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
    return JSONResponse(status_code=200, content={"message": "success"})


# 危険エリアを取得するAPI
@router.get("/get_danger_area", response_model=DangersResponse)
def get_danger_area(danger_id: str, db: Session = Depends(get_db)):
    danger_area = db.query(DANGERS).filter(DANGERS.camera_id == danger_id).first()
    return (
        danger_area.coordnate_p1,
        danger_area.coordnate_p2,
        danger_area.coordnate_p3,
        danger_area.coordnate_p4,
    )
