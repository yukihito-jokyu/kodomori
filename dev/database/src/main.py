from database.api import users as users_router
from database.api import alerts as alerts_router
from database.api import cameras as cameras_router
from database.api import dangers as dangers_router
from database.setup import ALERTS, CAMERAS, DANGERS, USERS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# FastAPIアプリケーションの初期化
app = FastAPI()


app.include_router(users_router.router, prefix="/api", tags=["users"])
app.include_router(alerts_router.router, prefix="/api", tags=["alerts"])
app.include_router(cameras_router.router, prefix="/api", tags=["cameras"])
app.include_router(dangers_router.router, prefix="/api", tags=["dangers"])

print(ALERTS, CAMERAS, DANGERS, USERS)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
