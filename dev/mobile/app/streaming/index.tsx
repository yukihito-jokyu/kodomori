// import React, { useState, useEffect } from 'react';
// import { View, Text, StyleSheet } from 'react-native';

// const WebSocketExample = () => {
//   const [number, setNumber] = useState(null); // サーバーから取得したデータ

//   useEffect(() => {
//     // WebSocketの初期化
//     const ws = new WebSocket('ws://127.0.0.1:8000/ws/streaming/test');

//     // 接続が開いた時の処理
//     ws.onopen = () => {
//       console.log('WebSocket connection opened');
//     };

//     // メッセージを受信した時の処理
//     ws.onmessage = (event) => {
//       try {
//         const data = JSON.parse(event.data); // JSONをパース
//         console.log('Received:', data);
//         setNumber(data.number); // 取得した数値をステートに設定
//       } catch (error) {
//         console.error('Error parsing message:', error);
//       }
//     };

//     // 接続が閉じた時の処理
//     ws.onclose = () => {
//       console.log('WebSocket connection closed');
//     };

//     // エラーが発生した時の処理
//     ws.onerror = (error) => {
//       console.error('WebSocket error:', error);
//     };

//     // クリーンアップ処理
//     return () => {
//       ws.close();
//     };
//   }, []);

//   return (
//     <View style={styles.container}>
//       <Text style={styles.title}>Received Number:</Text>
//       <Text style={styles.number}>{number !== null ? number : 'Waiting...'}</Text>
//     </View>
//   );
// };

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#f5f5f5',
//   },
//   title: {
//     fontSize: 24,
//     marginBottom: 20,
//   },
//   number: {
//     fontSize: 48,
//     fontWeight: 'bold',
//   },
// });

// export default WebSocketExample;

// import React, { useState, useEffect, useRef } from 'react';
// import { View, Text, StyleSheet } from 'react-native';

// const WebSocketExample = () => {
//   const [number, setNumber] = useState<number | null>(null); // サーバーから取得したデータ
//   const wsRef = useRef<WebSocket | null>(null); // WebSocket型またはnullを許容

//   useEffect(() => {
//     // WebSocketの初期化
//     wsRef.current = new WebSocket('ws://127.0.01:8000/ws/streaming/test');

//     // 接続が開いた時の処理
//     wsRef.current.onopen = () => {
//       console.log('WebSocket connection opened');
//     };

//     // メッセージを受信した時の処理
//     wsRef.current.onmessage = (event) => {
//       try {
//         const data = JSON.parse(event.data); // JSONをパース
//         console.log('Received:', data);
//         setNumber(data.number); // 取得した数値をステートに設定
//       } catch (error) {
//         console.error('Error parsing message:', error);
//       }
//     };

//     // 接続が閉じた時の処理
//     wsRef.current.onclose = () => {
//       console.log('WebSocket connection closed');
//     };

//     // エラーが発生した時の処理
//     wsRef.current.onerror = (error) => {
//       console.error('WebSocket error:', error);
//     };

//     // クリーンアップ処理
//     return () => {
//       if (wsRef.current) {
//         wsRef.current.close();
//         console.log('WebSocket connection closed during cleanup');
//       }
//     };
//   }, []);

//   return (
//     <View style={styles.container}>
//       <Text style={styles.title}>Received Number:</Text>
//       <Text style={styles.number}>{number !== null ? number : 'Waiting...'}</Text>
//     </View>
//   );
// };

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#f5f5f5',
//   },
//   title: {
//     fontSize: 24,
//     marginBottom: 20,
//   },
//   number: {
//     fontSize: 48,
//     fontWeight: 'bold',
//   },
// });

// export default WebSocketExample;

/////////////////////////////////////12月18日//////////////////////////////

// import React, { useEffect, useState } from 'react';
// import { SafeAreaView, Text, StyleSheet } from 'react-native';

// const StreamingScreen: React.FC = () => {
//   const [receivedMessage, setReceivedMessage] = useState<string>('Disconnected');

//   useEffect(() => {
//     // WebSocket接続
//     const ws = new WebSocket('ws://127.0.0.1:8000/ws'); // IPに合わせて変更

//     ws.onopen = () => {
//       console.log('WebSocket connection opened');
//     };

//     ws.onmessage = (event: MessageEvent) => {
//       setReceivedMessage(event.data); // サーバーから受け取ったメッセージを表示
//     };

//     ws.onerror = (error: Event) => {
//       console.error('WebSocket Error:', error);
//     };

//     ws.onclose = () => {
//       console.log('WebSocket connection closed');
//     };

//     // コンポーネントがアンマウントされた際に接続を閉じる
//     return () => {
//       ws.close();
//     };
//   }, []);

//   return (
//     <SafeAreaView style={styles.container}>
//       <Text style={styles.title}>WebSocket Streaming</Text>
//       <Text style={styles.message}>Received: {receivedMessage}</Text>
//     </SafeAreaView>
//   );
// };

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#fff',
//   },
//   title: {
//     fontSize: 24,
//     fontWeight: 'bold',
//     marginBottom: 20,
//   },
//   message: {
//     fontSize: 20,
//     color: 'blue',
//   },
// });

// export default StreamingScreen;

////////////////////////////////////////////////////

import React, { useEffect, useState } from 'react';
import { SafeAreaView, Text, StyleSheet,Image,View } from 'react-native';

const StreamingScreen: React.FC = () => {
  const [status, setStatus] = useState<string>('Disconnected'); // 接続状態
  const [imageData, setImageData] = useState<string | null>('null'); // サーバーからのメッセージ

  console.log('Component rendering started');

  useEffect(() => {

    console.log('WebSocket initializing...');
    // WebSocket接続
    // const ws = new WebSocket('ws://localhost:8000/ws'); // バックエンドのURL
    const ws = new WebSocket('ws://localhost:8000/ws/streaming/ws'); // バックエンドのURL

    ws.onopen = () => {
      setStatus('Connected');
      console.log('WebSocket connection opened');
    };

    ws.onmessage = (event: MessageEvent) => {
      setImageData(`data:image/jpeg;base64,${event.data}`); // Base64データをImageに変換
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
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Camera Streaming</Text>
      <Text>Status: {status}</Text>
      <View style={styles.imageContainer}>
        {imageData ? (
          <Image style={styles.image} source={{ uri: imageData }} />
        ) : (
          <Text>Waiting for data...</Text>
        )}
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  imageContainer: {
    width: 300,
    height: 300,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
});
export default StreamingScreen;



