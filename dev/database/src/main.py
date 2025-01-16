from database.api import users as users_router
from database.setup import ALERTS, CAMERAS, DANGERS, USERS
from fastapi import FastAPI

# FastAPIアプリケーションの初期化
app = FastAPI()

app.include_router(users_router.router)

print(ALERTS, CAMERAS, DANGERS, USERS)
