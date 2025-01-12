from datetime import datetime

from pydantic import BaseModel


# Pydanticモデルの定義
class Camera(BaseModel):
    camera_id: str
    camera_name: str


class UserCreate(BaseModel):
    user_id: int
    is_admin: bool
    nursery_school_id: int


class UserResponse(BaseModel):
    user_id: int
    is_admin: bool
    nursery_school_id: int

    class Config:
        from_attributes = True


class CameraResponse(BaseModel):
    camera_id: str
    picture: bool

    class Config:
        from_attributes = True


class AlertsResponse(BaseModel):
    alert_id: str
    message: str
    time: datetime

    class Config:
        from_attributes = True


class DangersResponse(BaseModel):
    danger_id: int
    camera_id: str
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int

    class Config:
        from_attributes = True


class DangersCreate(BaseModel):
    danger_id: int
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int


class CamerasFloorResponse(BaseModel):
    camera_id: str
    is_setting_floor_area: bool
    picture: bool

    distance_p1_p2: int
    distance_p1_p3: int
    distance_p1_p4: int
    distance_p2_p3: int
    distance_p2_p4: int
    distance_p3_p4: int

    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int


class CamerasFloorCreate(BaseModel):
    camera_id: str
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int

    class Config:
        from_attributes = True


class AdminResponse(BaseModel):
    camera_id: str
    picture: bool
    denger_id: str
    is_setting_floor_area: bool

    class Config:
        from_attributes = True


class Login(BaseModel):
    user_id: int


class CameraALLView(BaseModel):
    camera_id: int
    picture: bool
    camera_id: str
    denge_id: str
    alert_id: str
    message: str
