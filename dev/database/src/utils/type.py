from pydantic import BaseModel


# Pydanticモデルの定義
# 使用
class Camera(BaseModel):
    camera_id: str
    camera_name: str


class UserResponse(BaseModel):
    is_admin: bool
    nursery_school_id: int

    class Config:
        from_attributes = True


# 使用
class CameraResponse(BaseModel):
    camera_id: str
    picture: bool

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


# 使用〇
class DangersCreate(BaseModel):
    danger_id: int
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int


# 使用
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
class AllCamera(BaseModel):
    camera_id: str
