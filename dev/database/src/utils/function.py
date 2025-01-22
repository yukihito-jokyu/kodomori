from fastapi import Depends
from sqlalchemy.orm import Session

from database.session_db import get_db
from database.setup import CAMERAS, DANGERS, USERS, ALERTS


def make_massage_alerts(alert_id: str, db: Session = Depends(get_db)):
    user = db.query(ALERTS.user_id).filter(ALERTS.alert_id == alert_id).all()
    nursery_school = (
        db.query(USERS.nursery_school_id).filter(USERS.user_id == user).first()
    )  # 保育園IDを取得
    camera_name = (
        db.query(CAMERAS.camera_id)
        .filter(CAMERAS.nursery_school_id == nursery_school)
        .first()
    )  # カメラIDを取得
    danger_name = (
        db.query(DANGERS.danger_id).filter(DANGERS.camera_id == camera_name).first()
    )  # 危険エリアIDを取得
    return f"{nursery_school}の{camera_name}で園児が{danger_name}に入りそうです"


def floor_coordinate_distance(p1, p2, p3, p4):
    # 2点間の距離を計算
    p1_p2 = abs(p1 - p2)
    p1_p3 = abs(p1 - p3)
    p1_p4 = abs(p1 - p4)
    p2_p3 = abs(p2 - p3)
    p2_p4 = abs(p2 - p4)
    p3_p4 = abs(p3 - p4)
    return p1_p2, p1_p3, p1_p4, p2_p3, p2_p4, p3_p4
