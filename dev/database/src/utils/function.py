from fastapi import Depends
from sqlalchemy.orm import Session

from ..database.session_db import get_db
from ..database.setup import CAMERAS, DANGERS, USERS


def make_massage_alerts(db: Session = Depends(get_db)):
    nursery_school = (
        db.query(USERS.nursery_school_id).filter(USERS.user_id == 1).first()
    )  # 保育園IDを取得
    camera_name = (
        db.query(CAMERAS.camera_id).filter(CAMERAS.nursery_school_id == 1).first()
    )  # カメラIDを取得
    danger_name = (
        db.query(DANGERS.danger_id).filter(DANGERS.nursery_school_id == 1).first()
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


def make_massage_view_all_camera(db: Session = Depends(get_db)):
    nursery_school = (
        db.query(USERS.nursery_school_id).filter(USERS.user_id == 1).first()
    )  # 保育園IDを取得
    camera_name = (
        db.query(CAMERAS.camera_id).filter(CAMERAS.nursery_school_id == 1).first()
    )  # カメラIDを取得
    danger_name = (
        db.query(DANGERS.danger_id).filter(DANGERS.nursery_school_id == 1).first()
    )  # 危険エリアIDを取得
    return f"現在{nursery_school}の{camera_name}は{danger_name}です"
