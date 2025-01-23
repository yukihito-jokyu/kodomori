import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.setup import main_app

router = APIRouter(
    prefix="/ws/camera",
    tags=["camera"],
    responses={404: {"description": "Not found"}},
)


# WebSocketエンドポイント
@router.websocket("/get")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # WebSocket接続を承認

    try:
        while True:
            warped_with_zone_base64 = main_app.next()
            if warped_with_zone_base64 is not None:
                # WebSocketで送信
                await websocket.send_text(warped_with_zone_base64)
                # 適切なフレームレートで送信
                await asyncio.sleep(0.03)  # 約30fps
            else:
                print("not frame")
                break

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")
