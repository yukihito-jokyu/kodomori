from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.function import floor_coordinate_distance
from utils.type import (
    AdminResponse,
    Camera,
    CameraResponse,
    CamerasFloorCreate,
    CamerasFloorResponse,
)

from ..session_db import get_db
from ..setup import CAMERAS

router = APIRouter(
    prefix="/cameras",
    tags=["cameras"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    return {"message": "here is cameras!"}


# 通知詳細ページ（保育士）get
@router.get("/view_camera", response_model=CameraResponse)
def view_camera(camera: Camera, db: Session = Depends(get_db)):
    camera = db.query(CAMERAS).filter(CAMERAS.camera_id == camera.camera_id).first()
    return camera


@router.post("/add_floor", response_model=CamerasFloorResponse)
def create_floor(floor: CamerasFloorCreate, db: Session = Depends(get_db)):
    (
        new_distance_p1_p2,
        new_distance_p1_p3,
        new_distance_p1_p4,
        new_distance_p2_p3,
        new_distance_p2_p4,
        new_distance_p3_p4,
    ) = floor_coordinate_distance(
        floor.coordinate_p1,
        floor.coordinate_p2,
        floor.coordinate_p3,
        floor.coordinate_p4,
    )

    db_floor = CAMERAS(
        camera_id=floor.camera_id,
        coordinate_p1=floor.coordinate_p1,
        coordinate_p2=floor.coordinate_p2,
        coordinate_p3=floor.coordinate_p3,
        coordinate_p4=floor.coordinate_p4,
        distance_p1_p2=new_distance_p1_p2,
        distance_p1_p3=new_distance_p1_p3,
        distance_p1_p4=new_distance_p1_p4,
        distance_p2_p3=new_distance_p2_p3,
        distance_p2_p4=new_distance_p2_p4,
        distance_p3_p4=new_distance_p3_p4,
    )
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)

    return db_floor


# 管理者ページ（管理者）get
@router.get("/admin", response_model=AdminResponse)
def get_admin(db: Session = Depends(get_db)):
    cameras = db.query(CAMERAS).all()  # 要修正
    return cameras
