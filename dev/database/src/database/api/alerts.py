from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.function import make_massage_alerts
from utils.type import AlertsResponse

from ..session_db import get_db
from ..setup import ALERTS

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    return {"message": "here is alerts!"}


# alert_idを取得するAPI
@router.get("/get_alert_id", response_model=AlertsResponse)
def get_alert(nursery_school_id: str, db: Session = Depends(get_db)):
    return db.query(ALERTS).filter(ALERTS.nursery_school_id == nursery_school_id).all()


# 通知情報を所得するAPI
@router.get("/get_alert", response_model=list[AlertsResponse])
def get_alerts(alert_id: str, db: Session = Depends(get_db)):
    new_message = make_massage_alerts(alert_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    alert = (
        db.query(ALERTS.message, ALERTS.time, ALERTS.is_read)
        .filter(ALERTS.alert_id == alert_id)
        .all()
    )
    return alert


# -----------------------------------------------------
# 以下変更前のAPIコード、参考までに残しておきます

# 通知一覧ページ（保育士）get
# @router.get("/alerts", response_model=list[AlertsResponse])
# def get_alerts(db: Session = Depends(get_db)):
#     new_message = ALERTS(message=make_massage_alerts())
#     db.add(new_message)
#     db.commit()

#     alerts = db.query(ALERTS).all()
#     return alerts

# # カメラ映像一覧ページ（全員）get
# @router.get("/view_all_camera", response_model=CameraALLView)
# def view_all_camera(db: Session = Depends(get_db)):
#     new_message = ALERTS(message=make_massage_view_all_camera())
#     db.add(new_message)
#     db.commit()

#     cameras = db.query(CAMERAS).all()  # 要修正
#     return cameras
