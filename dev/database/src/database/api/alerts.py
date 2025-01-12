from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.function import make_massage_alerts, make_massage_view_all_camera
from utils.type import AlertsResponse, CameraALLView

from ..session_db import get_db
from ..setup import ALERTS, CAMERAS

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    return {"message": "here is alerts!"}


# 通知一覧ページ（保育士）get
@router.get("/alerts", response_model=list[AlertsResponse])
def get_alerts(db: Session = Depends(get_db)):
    new_message = ALERTS(message=make_massage_alerts())
    db.add(new_message)
    db.commit()

    alerts = db.query(ALERTS).all()
    return alerts


# カメラ映像確認ページ（全員）get、、、通知詳細ページと同じ？
# カメラ映像一覧ページ（全員）get
@router.get("/view_all_camera", response_model=CameraALLView)
def view_all_camera(db: Session = Depends(get_db)):
    new_message = ALERTS(message=make_massage_view_all_camera())
    db.add(new_message)
    db.commit()

    cameras = db.query(CAMERAS).all()  # 要修正
    return cameras
