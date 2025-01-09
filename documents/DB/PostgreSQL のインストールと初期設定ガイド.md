# PostgreSQL のインストールと初期設定ガイド

## インストール

PostgreSQL[公式サイト](https://www.postgresql.org/download/)にアクセスします。
「Packages and Installers」セクションで Windows をクリックします。
Download the installer をクリックします。
Windows x86-64 用のバージョン 17.2 をダウンロードします。

## インストール手順

こちらの[Qiita 記事](https://qiita.com/waokitsune/items/3a27b7d0ca75bc06b7c0)に従い、インストールウィザードで基本的にデフォルトのオプションを選択して進めます。
Pre Installation Summary 画面が表示されたら、インストールディレクトリのパスをコピーして控えておきます。
Stack Builder の選択を求められた場合は、リモートサーバーを必要としないオプションを選びます。
インストールを完了します。

## 初期設定（Windows 11）

コマンドラインから PostgreSQL を使用するためには、PostgreSQL のバイナリディレクトリをシステムの PATH 環境変数に追加する必要があります。
設定 > システム > バージョン情報 > システムの詳細設定 を開きます。
システムのプロパティダイアログで、環境変数 をクリックします。
ユーザー環境変数 から Path を選択し、編集 をクリックします。
新規 をクリックし、PostgreSQL のインストールディレクトリ内の bin ディレクトリのパスを追加します（先ほど控えたパス）。
OK をクリックして変更を保存します。

## データベースへのアクセス

Windows PowerShell を開きます。
cd コマンドで「kodomori/dev/database/SQL」ディレクトリに移動します。
次のコマンドを使用して postgres データベースに接続します。

```
psql -h localhost -p 5432 -U postgres -d postgres
```

## データベースの作成

次のコマンドから PostgreSQL に新しいデータベースを作成します。

```
CREATE DATABASE kodomori;
```

## テーブルの作成

次のコマンドから postgres データベースの接続を切ります。

```
\q
```

次のコマンドから kodomori データベースに接続します。

```
psql -h localhost -p 5432 -U postgres -d kodomori
```

次のコマンドを一行ずつ実行し、kodomori データベースに必要なテーブルを作成する。

```
\i users.sql
\i cameras.sql
\i dangers.sql
\i alerts.sql
```
## 今回使用しているデータベースのDATABASE_URL情報
データベース"postgres"にユーザー"postgres"として、ホスト"localhost"(アドレス"::1")上のポート"5432"で接続しています。

## 基本的なデータベースコマンド

### データベース一覧の表示:

```
\l
```

### 新しいデータベースの作成:

```
CREATE DATABASE <データベース名>;
```

### データベースからの退出:

```
\q
```

### 現在のデータベース内のテーブル一覧を表示:

```
\dt
```
