from fastapi import APIRouter
from utils.setup import main_app
from utils.types import Pin, PinAndDistance

router = APIRouter(
    prefix="/frame",
    tags=["frame"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    return {"message": "here is frame!"}


@router.post("/get_frame")
async def get_frame():
    frame_base64 = main_app.get_frame()
    return {"frame_base64": frame_base64}


@router.get("/get_wrap")
async def get_wrap():
    wrap_base64, height, width = main_app.get_wrap_code()
    return {"wrap_base64": wrap_base64, "height": height, "width": width}


@router.post("/floor_setting")
async def floor_setting(data: PinAndDistance):
    print(data)
    warped_base64 = main_app.set_floor(data)
    return {"warped_base64": warped_base64}


@router.post("/zone_setting")
async def zone_setting(data: Pin):
    print(data)
    warped_with_zone = main_app.set_zone(data)
    return {"warped_with_zone": warped_with_zone}
