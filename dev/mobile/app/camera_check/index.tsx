import React, { useEffect, useState } from 'react'
import { Image, SafeAreaView, StyleSheet, Text, View } from 'react-native'
import CustomHeaderNursery from '@/components/ContomHeaerNursery';
import Popup from '@/components/Popup';

export default function CameraCheckScreen() {
    const handleMenuPress = (): void => {
        alert('メニューがタップされました');
    };
    const [status, setStatus] = useState<string>('Disconnected'); // 接続状態
    const [imageData, setImageData] = useState<string | null>('null'); // サーバーからのメッセージ

    const [popupVisible, setPopupVisible] = useState(false);
    const [message, setMessage] = useState("");

    const showPopup = () => {
        setPopupVisible(true);
    };

    const closePopup = () => {
        setPopupVisible(false);
    };

    console.log('Component rendering started');

    useEffect(() => {

        console.log('WebSocket initializing...');
        // WebSocket接続
        // const ws = new WebSocket('ws://localhost:8000/ws'); // バックエンドのURL
        const ws = new WebSocket('ws://localhost:8000/ws/camera/get'); // バックエンドのURL

        ws.onopen = () => {
        setStatus('Connected');
        console.log('WebSocket connection opened');
        };

        ws.onmessage = (event: MessageEvent) => {
            if (event.data !== "") {
                const data = JSON.parse(event.data);
                // console.log(data.is_hit)
                setImageData(`data:image/jpeg;base64,${data.image}`); // Base64データをImageに変換
                // console.log(data.is_pred_hit)
                if (data.is_pred_hit === true) {
                    if (!popupVisible) {
                        showPopup()
                        setMessage(`子供 id: ${data.is_pred_hit_id} が危険エリアに入りそうです`)
                    }
                }
                // if (data.is_hit === true) {
                //     if (!popupVisible) {
                //         showPopup()
                //         setMessage(`子供${data.is_pred_hit_id}が危険エリアに入りました`)
                //     }
                // }
            }
        };

        ws.onerror = () => {
        setStatus('Error: Unable to connect');
        console.error('WebSocket Error');
        };

        ws.onclose = () => {
        setStatus('Disconnected');
        console.log('WebSocket connection closed');
        };

        return () => {
        console.log('WebSocket cleanup');
        ws.close(); // コンポーネントがアンマウントされた時に接続を閉じる
        };
    }, []);

    return (
        <SafeAreaView style={styles.pearent}>
            <CustomHeaderNursery onMenuPress={handleMenuPress} />
            <View style={styles.children}>
                <Text style={styles.cameraName}>カメラの場所の名前</Text>
                <View style={styles.cameraImageFrame}>
                    {imageData ? (
                        <Image style={styles.image} source={{ uri: imageData }} />
                    ) : (
                        <Text>Waiting for data...</Text>
                    )}
                </View>
                <View style={styles.backButtonWrapper}>
                    <View style={styles.backButton}>
                        <Text style={styles.backButtonText}>戻る</Text>
                    </View>
                </View>
            </View>
            <Popup
                visible={popupVisible}
                message={message}
                onClose={closePopup}
            />
        </SafeAreaView>
    )
}

const styles = StyleSheet.create({
    pearent: {
        display: "flex",
        width: "100%",
        justifyContent: "center",
    },
    children: {
        width: "80%",
        marginTop: 40,
        alignItems:'center',
        left:75
    },
    cameraName: {
        fontSize: 30,
        fontWeight: 600
    },
    cameraImageFrame: {
        width: "100%",
        height: 450,
        borderColor: "#D9D9D9",
        borderWidth: 8,
    },
    backButtonWrapper: {
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        marginTop: 30
    },
    backButton: {
        width: 120,
        height: 25,
        backgroundColor: "#202E78",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 10,
    },
    backButtonText: {
        color: "#FFFFFF"
    },
    image: {
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    },
});