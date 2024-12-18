# import asyncio
# from fastapi import APIRouter, WebSocketDisconnect ,WebSocket

# router = APIRouter()
#     # prefix="/ws/streaming",
#     # tags=["websocket"],
#     # responses={404: {"description": "Not found"}},


# # WebSocketエンドポイント
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()  # WebSocket接続を受け入れる
#     try:
#         response = await websocket.receive_text()
#         logger.info(f"receive {response}")
#         await asyncio.sleep(10)
#         await websocket.send_text(f"Message text was {response}")
#         logger.info("send message")

#     except WebSocketDisconnect:
#         print("WebSocket connection closed")
#         logger.error(traceback.format_exc())

###################################12月17日#################################
# import asyncio
# import json
# from fastapi import APIRouter, WebSocketDisconnect, WebSocket
# from websocket_router import router

# router = APIRouter(
#     prefix="/ws/streaming",
#     tags=["test"],
#     responses={404: {"description": "Not found"}},
# )

# # WebSocketエンドポイント
# @router.websocket("/test")
# async def websocket_endpoint(websocket: WebSocket):
#     is_connected = False  # 接続状態を追跡するフラグ

#     try:
#         await websocket.accept()  # WebSocket接続を受け入れる
#         is_connected = True
#         print(f"WebSocket connection status: {is_connected}")  # 接続時にtrueを出力

#         for i in range(10):  # 0～9の数値を送信
#             await websocket.send_text(json.dumps({"number": i}))  # JSON形式で送信
#             print(f"Sent: {i}")
#             await asyncio.sleep(1)  # 1秒間隔で送信
#     except WebSocketDisconnect:
#         is_connected = False
#         print(f"WebSocket connection status: {is_connected}")  # 切断時にfalseを出力

# import asyncio
# import json
# from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# router = APIRouter(
#     prefix="/ws/streaming",
#     tags=["test"],
#     responses={404: {"description": "Not found"}},
# )

# # 接続しているクライアントを管理するクラス
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# manager = ConnectionManager()

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_message(f"You said: {data}", websocket)
#             await manager.broadcast(f"Broadcast message: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast("A client disconnected.")

######################################12月18日########################################

from fastapi import WebSocket
import asyncio


async def websocket_send_numbers(websocket: WebSocket):
    await websocket.accept()  # WebSocket接続を承認
    try:
        for i in range(10):  # 0～9を順に送信
            await websocket.send_text(str(i))
            await asyncio.sleep(1)  # 1秒間隔
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
