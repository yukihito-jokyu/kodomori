from contextlib import asynccontextmanager

from fastapi import FastAPI

from .camera import Camera_Thread

camera_thread = Camera_Thread(buffer_all=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup event")
    camera_thread.start()
    yield
    print("Stopping the server...")
    camera_thread.stop()  # カメラスレッドの停止処理
    print("Server stopped gracefully.")
