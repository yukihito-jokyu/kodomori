from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import psycopg2

# FastAPIアプリケーションの初期化
app = FastAPI()

# データベースの設定
DATABASE_URL = "postgresql://postgres:kodomori_0110@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = automap_base()

# 既存のデータベース構造を反映
Base.prepare(autoload_with=engine)

# テーブル名に対応するクラスを取得
User = Base.classes.users
Dangers = Base.classes.dangers
Cameras = Base.classes.cameras
Alerts = Base.classes.alerts


# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydanticモデルの定義
class Camera(BaseModel):
    camera_id: int
    camera_name: str


class UserCreate(BaseModel):
    user_id: int
    is_admin: bool
    nursery_school_id: int


class UserResponse(BaseModel):
    user_id: int
    is_admin: bool
    nursery_school_id: int

    class Config:
        from_attributes = True


# データベース接続の確認
def check_db_connection():
    conn = None

    try:
        # データベースに接続する
        conn = psycopg2.connect(DATABASE_URL)

        # ここでデータベース操作を行う
        cur = conn.cursor()
        cur.execute("SELECT 1;")

        # 結果を取得する
        result = cur.fetchone()
        print("Database connection successful, result:", result)

    except psycopg2.Error as e:
        print("データベース接続エラー:", e)

    finally:
        if conn is not None:
            conn.close()


# エンジンの接続を確かめる関数
def check_engine_connection():
    try:
        # エンジンに接続
        with engine.connect():
            # 接続が成功した場合の処理
            print("Database engine connection successful.")
    except Exception as e:
        # 接続が失敗した場合の処理
        print(f"Database engine connection failed: {e}")


# エンジンの接続を確かめる
check_engine_connection()


# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Welcome to the PostgreSQL REST API with FastAPI!"}


# ユーザー一覧の取得
@app.get("/all_users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# ユーザーの作成
@app.post("/add_user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        user_id=user.user_id,
        is_admin=user.is_admin,
        nursery_school_id=user.nursery_school_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# issueとfigmaより想定されるアプリページを列挙、それに対応するエンドポイントを作成する

# 通知詳細ページ（保育士）
# 通知一覧ページ（保育士）
# 危険エリアの設定ページ（管理者）
# 床エリアの設定ページ（管理者）
# 管理者ページ（管理者）
# ログインページ（全員）
# カメラ映像確認ページ（全員）
# カメラ映像一覧ページ（全員）

# テストの実行
check_db_connection()
