import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    LargeBinary,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase

# 環境変数の取得
load_dotenv()
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# データベースの設定
DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@localhost:5432/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# テーブル名に対応するクラスを取得
class User(Base):
    __tablename__ = "users"

    # カラム定義
    user_id = Column(String(255), primary_key=True)
    nursery_school_id = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', nursery_school_id='{self.nursery_school_id}', is_admin={self.is_admin})>"


class Danger(Base):
    __tablename__ = "dangers"

    # カラム定義
    danger_id = Column(String(255), primary_key=True)
    camera_id = Column(String(255), ForeignKey("cameras.camera_id"), nullable=False)
    coordinate_p1 = Column(Integer, nullable=False)
    coordinate_p2 = Column(Integer, nullable=False)
    coordinate_p3 = Column(Integer, nullable=False)
    coordinate_p4 = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Danger(danger_id='{self.danger_id}', camera_id='{self.camera_id}')>"


class Camera(Base):
    __tablename__ = "cameras"

    # カラム定義
    camera_id = Column(String(255), primary_key=True)
    nursery_school_id = Column(String(255), ForeignKey("users.user_id"), nullable=False)
    is_setting_floor_area = Column(Boolean, nullable=False)
    picture = Column(LargeBinary, nullable=False)
    distance_p1_p2 = Column(Integer, nullable=False)
    distance_p1_p3 = Column(Integer, nullable=False)
    distance_p1_p4 = Column(Integer, nullable=False)
    distance_p2_p3 = Column(Integer, nullable=False)
    distance_p2_p4 = Column(Integer, nullable=False)
    distance_p3_p4 = Column(Integer, nullable=False)
    coordinate_p1 = Column(Integer, nullable=False)
    coordinate_p2 = Column(Integer, nullable=False)
    coordinate_p3 = Column(Integer, nullable=False)
    coordinate_p4 = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Camera(camera_id='{self.camera_id}', nursery_school_id='{self.nursery_school_id}')>"


class Alert(Base):
    __tablename__ = "alerts"

    # カラム定義
    alert_id = Column(String(255), primary_key=True)
    nursery_school_id = Column(String(255), ForeignKey("users.user_id"), nullable=False)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Alert(alert_id='{self.alert_id}', nursery_school_id='{self.nursery_school_id}', message='{self.message}')>"


# テーブルの作成
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


# テーブルの存在を確認する関数
def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        print("Tables in the database:")
        for table in tables:
            print(f"- {table}")
    else:
        print("No tables found in the database.")


def init_database():
    # データベースを初期化（既存テーブルをドロップして再作成）
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database re-initialized.")


def create_testdata():
    session = SessionLocal()
    try:
        # ユーザーデータの作成
        test_users = [
            User(user_id="school1", nursery_school_id="school1", is_admin=True)
        ]
        session.add_all(test_users)
        session.commit()

        # アラートデータの作成
        test_alerts = [
            Alert(
                alert_id="alert1",
                nursery_school_id="school1",  # user_idからnursery_school_idに修正
                message="Test alert message 1",
                is_read=False,
                time="2024-01-16 00:00:00",
            )
        ]
        session.add_all(test_alerts)
        session.commit()

        test_cameras = [
            Camera(
                camera_id="camera1",
                nursery_school_id="school1",
                is_setting_floor_area=True,
                picture=b"test_picture",
                distance_p1_p2=10,
                distance_p1_p3=20,
                distance_p1_p4=30,
                distance_p2_p3=40,
                distance_p2_p4=50,
                distance_p3_p4=60,
                coordinate_p1=10,
                coordinate_p2=20,
                coordinate_p3=30,
                coordinate_p4=40,
            )
        ]
        session.add_all(test_cameras)
        session.commit()

        test_dangers = [
            Danger(
                danger_id="danger1",
                camera_id="camera1",
                coordinate_p1=10,
                coordinate_p2=20,
                coordinate_p3=30,
                coordinate_p4=40,
            )
        ]
        session.add_all(test_dangers)
        session.commit()

        print("テストデータの作成に成功しました")
    except Exception as e:
        print(f"テストデータの作成に失敗しました: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    init_database()
    create_tables()
    check_tables()
    create_testdata()
