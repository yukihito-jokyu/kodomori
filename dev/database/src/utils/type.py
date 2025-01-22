from pydantic import BaseModel


# Pydanticモデルの定義

# GETモデル定義


# 使用
class AlertsResponse(BaseModel):
    alert_id: str


# 使用
class AlertsMessageResponse(BaseModel):
    message: str
    time: str
    is_read: bool


# 使用
class CameraResponse(BaseModel):
    camera_id: str


# 使用
class CamerasFloorCheck(BaseModel):
    is_setting_floor_area: bool


class PictureResponse(BaseModel):
    picture: bytes


class CamerasFloorResponse(BaseModel):
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


# 使用
class DangersIdResponse(BaseModel):
    danger_id: str

    class Config:
        from_attributes = True


# 使用
class DangersResponse(BaseModel):
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int

    class Config:
        from_attributes = True


# POSTモデル定義


class CamerasFloorCreate(BaseModel):
    camera_id: str
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


# 使用〇
class DangersCreate(BaseModel):
    danger_id: str
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int

    # 使用


class UserResponse(BaseModel):
    is_admin: bool
    nursery_school_id: str


class LoginRequest(BaseModel):
    user_id: str
