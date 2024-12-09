from fastapi import FastAPI
from routers import test as routers_test
from websocket import test as websocket_test

app = FastAPI()

app.include_router(routers_test.router)
app.include_router(websocket_test.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
