from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.type import UserResponse

from ..session_db import get_db
from ..setup import USERS

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    return {"message": "here is users!"}


# ログインAPI
@router.post("/login", response_model=UserResponse)
def login(user_id: str, db: Session = Depends(get_db)):
    users = (
        db.query(USERS.user_id, USERS.is_admin).filter(USERS.user_id == user_id).all()
    )
    return users


# ---------------------------------------------------------------------
# 以下変更前のAPIコード、参考までに残しておきます

# ユーザーの作成
# @router.post("/add_user", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = USERS(
#         user_id=user.user_id,
#         is_admin=user.is_admin,
#         nursery_school_id=user.nursery_school_id,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
