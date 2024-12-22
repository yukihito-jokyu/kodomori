# from fastapi import FastAPI
# from websocket.socket_import import router as streaming_router
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import APIRouter, WebSocketDisconnect ,WebSocket

# app = FastAPI()


# #WebSocketのエントリーポイント
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 必要に応じて適切なオリジンを指定
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # app.include_router(routers_test.router)
# app.include_router(streaming_router)

# #ルートエンドポイント
# @app.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}

###################################12月17日#####################################

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from websocket.socket_import import router as websocket_router

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 必要に応じて特定のオリジンに制限
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.middleware("http")
# async def add_security_headers(request, call_next):
#     response = await call_next(request)
#     # Content Security Policyの設定
#     response.headers["Content-Security-Policy"] = (
#         "default-src 'self'; "
#         "connect-src 'self' ws://127.0.0.1:8000; "
#         "script-src 'self'; "
#         "style-src 'self'; "
#         "img-src 'self';"
#     )
#     return response

# # WebSocketルーターをアプリケーションに追加
# app.include_router(websocket_router)

# @app.get("/")
# async def root():
#     return {"message": "WebSocket Test Application"}


####################################12月18日 成功#####################################
# from fastapi import FastAPI, WebSocket
# from websocket import socket_import
# import asyncio

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "WebSocket Backend Ready"}


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     # await socket_import.websocket_send_numbers(websocket)
#     await websocket.accept()  # WebSocket接続を承認
#     try:
#         for i in range(10):  # 0～9を順に送信
#             await websocket.send_text(str(i))
#             await asyncio.sleep(1)  # 1秒間隔
#             print(i)
#     except Exception as e:
#         print(f"WebSocket Error: {e}")
#     finally:
#         await websocket.close()

###########################################12月19日##############################

from fastapi import FastAPI
from websocket.socket_import import router as websocket_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "WebSocket Backend Ready"}


app.include_router(websocket_router)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     # await socket_import.websocket_send_numbers(websocket)
#     await websocket.accept()  # WebSocket接続を承認
#     try:
#         for i in range(10):  # 0～9を順に送信
#             await websocket.send_text(str(i))
#             await asyncio.sleep(1)  # 1秒間隔
#             print(i)
#     except Exception as e:
#         print(f"WebSocket Error: {e}")
#     finally:
#         await websocket.close()
