from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from datetime import datetime
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
    camera_id: str
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


class CameraResponse(BaseModel):
    camera_id: str
    picture: bool

    class Config:
        from_attributes = True


class AlertsResponse(BaseModel):
    alert_id: str
    message: str
    time: datetime

    class Config:
        from_attributes = True


class DangersResponse(BaseModel):
    danger_id: int
    camera_id: str
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int

    class Config:
        from_attributes = True


class DangersCreate(BaseModel):
    danger_id: int
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int


class CamerasFloorResponse(BaseModel):
    camera_id: str
    is_setting_floor_area: bool
    picture: bool

    distance_p1_p2: int
    distance_p1_p3: int
    distance_p1_p4: int
    distance_p2_p3: int
    distance_p2_p4: int
    distance_p3_p4: int

    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int


class CamerasFloorCreate(BaseModel):
    camera_id: str
    coordinate_p1: int
    coordinate_p2: int
    coordinate_p3: int
    coordinate_p4: int

    class Config:
        from_attributes = True


class AdminResponse(BaseModel):
    camera_id: str
    picture: bool
    denger_id: str
    is_setting_floor_area: bool

    class Config:
        from_attributes = True


class Rogin(BaseModel):
    user_id: int


class CameraALLView(BaseModel):
    camera_id: int
    picture: bool
    camera_id: str
    denge_id: str
    alert_id: str
    message: str


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


# 通知詳細ページ（保育士）get
@app.get("/view_camera", response_model=CameraResponse)
def view_camera(camera: Camera, db: Session = Depends(get_db)):
    camera = db.query(Cameras).filter(Cameras.camera_id == camera.camera_id).first()
    return camera


# 通知一覧ページ（保育士）get
@app.get("/alerts", response_model=list[AlertsResponse])
def get_alerts(db: Session = Depends(get_db)):
    new_message = Alerts(message=make_massage_alerts())
    db.add(new_message)
    db.commit()

    alerts = db.query(Alerts).all()
    return alerts


def make_massage_alerts(db: Session = Depends(get_db)):
    nursery_school = (
        db.query(User.nursery_school_id).filter(User.user_id == 1).first()
    )  # 保育園IDを取得
    camera_name = (
        db.query(Cameras.camera_id).filter(Cameras.nursery_school_id == 1).first()
    )  # カメラIDを取得
    danger_name = (
        db.query(Dangers.danger_id).filter(Dangers.nursery_school_id == 1).first()
    )  # 危険エリアIDを取得
    return f"{nursery_school}の{camera_name}で園児が{danger_name}に入りそうです"


# 危険エリアの設定ページ（管理者）post
@app.post("/add_danger", response_model=DangersResponse)
def create_danger(danger: DangersCreate, db: Session = Depends(get_db)):
    db_danger = Dangers(
        danger_id=danger.danger_id,
        coordinate_p1=danger.coordinate_p1,
        coordinate_p2=danger.coordinate_p2,
        coordinate_p3=danger.coordinate_p3,
        coordinate_p4=danger.coordinate_p4,
    )
    db.add(db_danger)
    db.commit()
    db.refresh(db_danger)
    return db_danger


# 床エリアの設定ページ（管理者）post
@app.post("/add_floor", response_model=CamerasFloorResponse)
def create_floor(floor: CamerasFloorCreate, db: Session = Depends(get_db)):
    (
        new_distance_p1_p2,
        new_distance_p1_p3,
        new_distance_p1_p4,
        new_distance_p2_p3,
        new_distance_p2_p4,
        new_distance_p3_p4,
    ) = floor_coordinate_distance(
        floor.coordinate_p1,
        floor.coordinate_p2,
        floor.coordinate_p3,
        floor.coordinate_p4,
    )

    db_floor = Cameras(
        camera_id=floor.camera_id,
        coordinate_p1=floor.coordinate_p1,
        coordinate_p2=floor.coordinate_p2,
        coordinate_p3=floor.coordinate_p3,
        coordinate_p4=floor.coordinate_p4,
        distance_p1_p2=new_distance_p1_p2,
        distance_p1_p3=new_distance_p1_p3,
        distance_p1_p4=new_distance_p1_p4,
        distance_p2_p3=new_distance_p2_p3,
        distance_p2_p4=new_distance_p2_p4,
        distance_p3_p4=new_distance_p3_p4,
    )
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)

    return db_floor


def floor_coordinate_distance(p1, p2, p3, p4):
    # 2点間の距離を計算
    p1_p2 = abs(p1 - p2)
    p1_p3 = abs(p1 - p3)
    p1_p4 = abs(p1 - p4)
    p2_p3 = abs(p2 - p3)
    p2_p4 = abs(p2 - p4)
    p3_p4 = abs(p3 - p4)
    return p1_p2, p1_p3, p1_p4, p2_p3, p2_p4, p3_p4


# 管理者ページ（管理者）get
@app.get("/admin", response_model=AdminResponse)
def get_admin(db: Session = Depends(get_db)):
    cameras = db.query(Cameras).all()  # 要修正
    return cameras


# ログインページ（全員）post
@app.post("/login", response_model=Rogin)
def login(user: Rogin, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.user_id == user.user_id).all()
    if users == []:
        return False
    return True


# カメラ映像確認ページ（全員）get、、、通知詳細ページと同じ？
# カメラ映像一覧ページ（全員）get
@app.get("/view_all_camera", response_model=CameraALLView)
def view_all_camera(db: Session = Depends(get_db)):
    new_message = Alerts(message=make_massage_view_all_camera())
    db.add(new_message)
    db.commit()

    cameras = db.query(Cameras).all()  # 要修正
    return cameras


def make_massage_view_all_camera(db: Session = Depends(get_db)):
    nursery_school = (
        db.query(User.nursery_school_id).filter(User.user_id == 1).first()
    )  # 保育園IDを取得
    camera_name = (
        db.query(Cameras.camera_id).filter(Cameras.nursery_school_id == 1).first()
    )  # カメラIDを取得
    danger_name = (
        db.query(Dangers.danger_id).filter(Dangers.nursery_school_id == 1).first()
    )  # 危険エリアIDを取得
    return f"現在{nursery_school}の{camera_name}は{danger_name}です"


# テストの実行
check_db_connection()
