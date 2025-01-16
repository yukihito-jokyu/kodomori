import os
import threading

from fastapi import FastAPI, File, UploadFile

# **********CORS 設定
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routers import test as routers_test
from utils.test import capture_frames
from websocket import test as websocket_test

app = FastAPI()

app.include_router(routers_test.router)
app.include_router(websocket_test.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# **********

# 画像を保存するディレクトリ
IMAGE_DIR = "../assets/camera_image"


# 画像をアップロードするエンドポイント
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    file_location = os.path.join(IMAGE_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


# 画像を取得するエンドポイント
@app.get("/get-image/{image_name}")
async def get_image(image_name: str):
    file_location = os.path.join(IMAGE_DIR, image_name)
    if os.path.exists(file_location):
        return FileResponse(file_location)
    return {"error": "Image not found"}


# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# 画像ディレクトリ内のファイル一覧を表示するエンドポイント
@app.get("/list-images/")
async def list_images():
    if not os.path.exists(IMAGE_DIR):
        print(f"Image directory not found: {IMAGE_DIR}")
        return {"error": "Image directory not found"}

    files = os.listdir(IMAGE_DIR)
    print(f"files: {files}")
    image_files = [
        file for file in files if os.path.isfile(os.path.join(IMAGE_DIR, file))
    ]
    print(f"image_files: {image_files}")
    return {"images": image_files}


if __name__ == "__main__":
    thread = threading.Thread(target=capture_frames)
    thread.daemon = True
    thread.start()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
