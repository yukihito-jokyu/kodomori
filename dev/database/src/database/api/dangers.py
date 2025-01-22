from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.type import DangersCreate, DangersResponse, DangersIdResponse
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
@router.get("/get_danger_id", response_model=DangersIdResponse)
def get_dange_id(camera_id: str, db: Session = Depends(get_db)):
    return db.query(DANGERS.danger_id).filter(DANGERS.camera_id == camera_id).first()


# 危険エリアを保存するAPI
def check_danger_id_exists(danger_id: str, db: Session) -> bool:
    return db.query(DANGERS).filter(DANGERS.danger_id == danger_id).first() is not None


@router.post("/add_danger")
def create_danger(danger: DangersCreate, db: Session = Depends(get_db)):
    try:
        # danger_idの重複チェック
        if check_danger_id_exists(danger.danger_id, db):
            raise HTTPException(
                status_code=400, detail=f"Danger ID {danger.danger_id} already exists"
            )

        db_danger = DANGERS(
            danger_id=danger.danger_id,
            camera_id="camera1",
            coordinate_p1=danger.coordinate_p1,
            coordinate_p2=danger.coordinate_p2,
            coordinate_p3=danger.coordinate_p3,
            coordinate_p4=danger.coordinate_p4,
        )

        db.add(db_danger)
        db.commit()
        db.refresh(db_danger)

        return JSONResponse(status_code=201, content={"message": "success"})

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to create danger area: {str(e)}"
        )


# 危険エリアを取得するAPI
@router.get("/get_danger_area", response_model=DangersResponse)
def get_danger_area(danger_id: str, db: Session = Depends(get_db)):
    danger_area = db.query(DANGERS).filter(DANGERS.danger_id == danger_id).first()
    return {
        "coordinate_p1": danger_area.coordinate_p1,
        "coordinate_p2": danger_area.coordinate_p2,
        "coordinate_p3": danger_area.coordinate_p3,
        "coordinate_p4": danger_area.coordinate_p4,
    }
