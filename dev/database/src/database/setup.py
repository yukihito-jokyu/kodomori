import os

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect, text


# ## 今回使用しているデータベースのDATABASE_URL情報
# データベース"postgres"にユーザー"postgres"として、ホスト"localhost"(アドレス"::1")上のポート"5432"で接続しています。

# ## 今回使用しているデータベースのパスワード
# kodomori_0110

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


def inspect_tables():
    print("\n=== テーブル一覧 ===")
    for class_name in Base.classes.keys():
        print(f"\n--- {class_name} テーブル ---")
        table_class = Base.classes[class_name]
        table = table_class.__table__

        # カラム情報の取得
        for column in table.columns:
            print(f"\nカラム名: {column.name}")
            print(f"型: {column.type}")
            print(f"主キー?: {column.primary_key}")
            print(f"Null許可?: {column.nullable}")

            # デフォルト値の確認
            if column.default:
                print(f"デフォルト値: {column.default}")

            # 外部キー制約の確認
            for fk in column.foreign_keys:
                print(f"外部キー: {fk.target_fullname}")

            # その他の制約の確認
            constraints = []
            if column.unique:
                constraints.append("UNIQUE")
            if column.index:
                constraints.append("INDEX")
            if constraints:
                print(f"制約: {', '.join(constraints)}")

            print("---")

        # テーブルの制約情報
        print("\nテーブルの制約:")
        for constraint in table.constraints:
            print(f"- {constraint}")


# データベース接続の確認
def check_db_connection():
    conn = None

    try:
        # データベースに接続する
        conn = psycopg2.connect(DATABASE_URL)

        # ここでデータベース操作を行う
        cur = conn.cursor()
        cur.execute("SELECT * FROM *")
        rows = cur.fetchall()
        for row in rows:
            print(row)

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

inspect_tables()


def display_all_tables():
    session = SessionLocal()
    try:
        # テーブル一覧を取得
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        for table_name in table_names:
            print(f"\n=== {table_name} テーブルの内容 ===")
            # 動的にSQLクエリを実行
            result = session.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()

            if not rows:
                print("データがありません")
                continue

            # カラム名を取得
            columns = result.keys()
            print("カラム:", ", ".join(columns))

            # データを表示
            for row in rows:
                print(row)

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    display_all_tables()
