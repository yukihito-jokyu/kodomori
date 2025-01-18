import asyncio
import base64

import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.setup import camera_thread

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
            frame = camera_thread.next(black=False)
            if frame is not None:
                ret, buffer = cv2.imencode(".jpg", frame)
                # フレームをJPEG形式にエンコード
                _, buffer = cv2.imencode(".jpg", frame)
                # Base64エンコードしてテキスト形式に変換
                frame_base64 = base64.b64encode(buffer).decode("utf-8")
                # WebSocketで送信
                await websocket.send_text(frame_base64)
                # 適切なフレームレートで送信
                await asyncio.sleep(0.03)  # 約30fps
            else:
                print("not frame")
                break

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")
