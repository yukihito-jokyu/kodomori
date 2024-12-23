-- usersテーブルの作成
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    is_admin BOOLEAN NOT NULL,
    nursery_school_id VARCHAR(255) NOT NULL
)