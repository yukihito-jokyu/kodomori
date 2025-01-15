from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from utils.type import (
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


# カメラIDを取得するAPI
@router.get("/all_cameras", response_model=list[CameraResponse])
def get_cameras(nursery_school_id: str, db: Session = Depends(get_db)):
    cameras = (
        db.query(CAMERAS.camera_id)
        .filter(CAMERAS.nursery_school_id == nursery_school_id)
        .all()
    )
    return cameras


# 床を設定しているかどうかを確認するAPI
@router.get("/floor_setting", response_model=CamerasFloorResponse)
def floor_setting(camera_id: str, db: Session = Depends(get_db)):
    cameras = db.query(CAMERAS).filter(CAMERAS.camera_id == camera_id).first()
    return cameras.is_setting_floor_area


# 画像を取得するAPI
@router.get("/picture", response_model=CameraResponse)
def get_picture(camera_id: str, db: Session = Depends(get_db)):
    cameras = db.query(CAMERAS).filter(CAMERAS.camera_id == camera_id).first()
    return cameras.picture


# 床エリアを保存するAPI
@router.post("/add_floor")
def create_floor(floor: CamerasFloorCreate, db: Session = Depends(get_db)):
    db_floor = CAMERAS(
        camera_id=floor.camera_id,
        coordinate_p1=floor.coordinate_p1,
        coordinate_p2=floor.coordinate_p2,
        coordinate_p3=floor.coordinate_p3,
        coordinate_p4=floor.coordinate_p4,
        distance_p1_p2=floor.distance_p1_p2,
        distance_p1_p3=floor.distance_p1_p3,
        distance_p1_p4=floor.distance_p1_p4,
        distance_p2_p3=floor.distance_p2_p3,
        distance_p2_p4=floor.distance_p2_p4,
        distance_p3_p4=floor.distance_p3_p4,
    )
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)

    return JSONResponse(status_code=200, content={"message": "success"})


# 床エリアを取得するAPI
@router.get("/get_floor", response_model=CamerasFloorResponse)
def get_floor(camera_id: str, db: Session = Depends(get_db)):
    cameras = db.query(CAMERAS).filter(CAMERAS.camera_id == camera_id).first()
    return (
        cameras.distance_p1_p2,
        cameras.distance_p1_p3,
        cameras.distance_p1_p4,
        cameras.distance_p2_p3,
        cameras.distance_p2_p4,
        cameras.distance_p3_p4,
        cameras.coordinate_p1,
        cameras.coordinate_p2,
        cameras.coordinate_p3,
        cameras.coordinate_p4,
    )


# ---------------------------------------------------------------------
# 以下変更前のAPIコード、参考までに残しておきます

# 通知詳細ページ（保育士）get
# @router.get("/view_camera", response_model=CameraResponse)
# def view_camera(camera: Camera, db: Session = Depends(get_db)):
#     camera = db.query(CAMERAS).filter(CAMERAS.camera_id == camera.camera_id).first()
#     return camera

# @router.post("/add_floor_4point", response_model=CamerasFloorResponse)
# def create_floor(floor: CamerasFloorCreate, db: Session = Depends(get_db)):
#     (
#         new_distance_p1_p2,
#         new_distance_p1_p3,
#         new_distance_p1_p4,
#         new_distance_p2_p3,
#         new_distance_p2_p4,
#         new_distance_p3_p4,
#     ) = floor_coordinate_distance(
#         floor.coordinate_p1,
#         floor.coordinate_p2,
#         floor.coordinate_p3,
#         floor.coordinate_p4,
#     )

#     db_floor = CAMERAS(
#         camera_id=floor.camera_id,
#         coordinate_p1=floor.coordinate_p1,
#         coordinate_p2=floor.coordinate_p2,
#         coordinate_p3=floor.coordinate_p3,
#         coordinate_p4=floor.coordinate_p4,
#         distance_p1_p2=new_distance_p1_p2,
#         distance_p1_p3=new_distance_p1_p3,
#         distance_p1_p4=new_distance_p1_p4,
#         distance_p2_p3=new_distance_p2_p3,
#         distance_p2_p4=new_distance_p2_p4,
#         distance_p3_p4=new_distance_p3_p4,
#     )
#     db.add(db_floor)
#     db.commit()
#     db.refresh(db_floor)

#     return db_floor


# # 管理者ページ（管理者）get
# @router.get("/admin", response_model=AdminResponse)
# def get_admin(db: Session = Depends(get_db)):
#     cameras = db.query(CAMERAS).all()  # 要修正
#     return cameras
