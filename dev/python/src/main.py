from fastapi import FastAPI

# **********CORS 設定
# from fastapi.middleware.cors import CORSMiddleware
from routers import test as routers_test
from utils.setup import lifespan
from websocket import camera as websocket_camera

app = FastAPI(lifespan=lifespan)

app.include_router(routers_test.router)
app.include_router(websocket_camera.router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # すべてのオリジンを許可
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# **********


# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
