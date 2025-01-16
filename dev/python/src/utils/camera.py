import cv2

# カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

# 繰り返しのためのwhile文
while True:
    # カメラからの画像取得
    ret, frame = cap.read()

    if ret:
        # カメラの画像の出力
        cv2.imshow("camera", frame)
    else:
        break

    # 繰り返し分から抜けるためのif文
    key = cv2.waitKey(10)
    if key == 27:
        break

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()
