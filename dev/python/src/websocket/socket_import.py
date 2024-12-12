# from fastapi import FastAPI, WebSocket

# app = FastAPI()

# from fastapi import APIRouter

# router = APIRouter(
#     prefix="/ws/test",
#     tags=["test"],
#     responses={404: {"description": "Not found"}},
# )

# @router.websocket("/ws")#####################routerに変更する
# async def websocket_endpoint(websocket: WebSocket):
#     print("WebSocket: 接続要求を受け取りました")
#     await websocket.accept()
#     print("WebSocket: 接続が確立しました")
#     try:
#         while True:
#             message = await websocket.receive_text()
#             print(f"受信したメッセージ: {message}")
#             await websocket.send_text(f"受信: {message}")
#     except Exception as e:
#         print(f"WebSocketエラー: {e}")
#     finally:
#         print("WebSocket: 接続を終了しました")

##正常に動作しているかの確認
# import asyncio

# async def test_websocket():
#     uri = "ws://localhost:8000/ws/test/ws"
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("Hello, Server!")
#         response = await websocket.recv()
#         print(f"サーバーからの応答: {response}")

# asyncio.run(test_websocket())
