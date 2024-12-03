# kodomori

# Project setup(windows)

## 1, nvm のインストール

windows 用の nvm をインストールするには[リンク](https://github.com/coreybutler/nvm-windows/releases)から nvm-windows の github repository へ移動し、**nvm-setup.exe**ファイルをダウンロードする。
ダウンロードした nvm-setup.exe から nvm をインストールする。
[参考サイト](https://qiita.com/akipon0821/items/eaeffe79221cfcd4d258)

## 2, node のインストール

インストールした nvm から node をインストールする。今回使う node のバージョンは 20.18.0 である。

```bash
nvm install v20.18.0
```

インストールしたバージョンを適応させる。バージョンを適応することで初めてインストールした node のバージョンを使用することができる。

```bash
nvm use 20.18.0
```

node のバージョン確認をする。

```bash
node -v
```

これで`20.18.0`と出力されれば、node のインストールは完了！

## 3, Expo にサインイン

今回のプロジェクトで使うのは React Native で、Expo は React Native の開発を便利にするツールである。
[リンク](https://expo.dev/)から Expo の公式ページに移動し、サインインする。

## 4, Android Studio のダウンロード

今回のプロジェクトでは emulator を起動して開発を進めるので、[リンク](https://developer.android.com/studio?hl=ja&_gl=1*786oak*_up*MQ..*_ga*MTU1MzM2NzQyLjE3MzMxOTE4MTc.*_ga_6HH9YJMN9M*MTczMzE5MTgxNy4xLjAuMTczMzE5MTgxNy4wLjAuMTIwMDEyODM0Ng..)からダウンロードする。

### 4-1, Android Studio の Setup の手順

- ダウンロード完了後、Android Studio を起動する。Projects のタブを選択したまま、真ん中にある**More Actions**をクリックする。
- プルダウンで表示された中から**Virtual Device Manager**をクリックする。
- 別ウィンドウで Device Manager が開く。左上の+ボタン(ホバー時に**Creat Virtual Device**が表示される)をクリックする。
- 再び別ウィンドウで Virtual Device Configuration が表示される。ここでタブレットを選択する。
- 選択するタブレットは**Tablet**の**Pixel Tablet**で、選択したのちに**Next**ボタンを押す。
- Select a system image で**Recommendede**を**VanillalceCream**と選択し、**Next**ボタンを押す。
- Verify Configuration で**Startup orientation**を**Portrait**に選択し、**Finish**ボタンを押す。

### 4-2, emulator の起動

Device Manager ウィンドウで**Pixel Tablet**のスタートボタンを押すことで emulator が起動する。

## 5, レポジトリのクローン

ターミナルから以下のコマンドを実行し、このレポジトリをクローンする。

```bahs
git clone https://github.com/yukihito-jokyu/kodomori.git
```

## 6, 環境の同期

cd コマンドで mobile ディレクトリに移動し、以下のコマンドを実行する。

```bash
npm i
```

このコマンドから環境を同期することができる。
