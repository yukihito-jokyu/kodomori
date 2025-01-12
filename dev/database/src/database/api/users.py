from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.type import Login, UserCreate, UserResponse

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


# ユーザー一覧の取得
@router.get("/all_users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(USERS).all()
    return users


# ユーザーの作成
@router.post("/add_user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = USERS(
        user_id=user.user_id,
        is_admin=user.is_admin,
        nursery_school_id=user.nursery_school_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ログインページ（全員）post
@router.post("/login", response_model=Login)
def login(user: Login, db: Session = Depends(get_db)):
    users = db.query(USERS).filter(USERS.user_id == user.user_id).all()
    if users == []:
        return False
    return True
