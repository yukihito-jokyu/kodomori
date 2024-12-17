# ルール

## ブランチ名

ブランチの名前は基本的に`issue/番号`にする。

## 不要なブランチは削除する

作業完了(リモートブランチが main にマージされた)後、不要になったブランチは削除するようにする。
まず、main に移動する。

```bash
git checkout main
```

リモートの変更点と同期する。

```bash
git pull origin main
```

不要なブランチを削除する。

```bash
git branch -D issue/番号
```
