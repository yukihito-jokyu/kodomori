import os

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

# 環境変数の取得
load_dotenv()
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# データベースの設定
DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@localhost:5432/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = automap_base()

# 既存のデータベース構造を反映
Base.prepare(autoload_with=engine)

# テーブル名に対応するクラスを取得
USERS = Base.classes.users
DANGERS = Base.classes.dangers
CAMERAS = Base.classes.cameras
ALERTS = Base.classes.alerts


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


# テストの実行
check_db_connection()
