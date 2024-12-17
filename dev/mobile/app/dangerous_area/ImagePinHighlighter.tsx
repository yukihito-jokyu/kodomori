import React, { useState, useRef} from 'react';
import { View, Text, Image, TouchableWithoutFeedback, StyleSheet, PanResponder, Button} from 'react-native';
import { useRoute } from '@react-navigation/native';
import Svg, { Polygon } from 'react-native-svg';

interface Point {
  x: number;
  y: number;
}

const IMAGE_WIDTH = 300;
const IMAGE_HEIGHT = 200;

const IMAGE_BASE_URL = 'http://127.0.0.1:8000/get-image/';

const DraggablePin = ({
  index,
  pin,
  updatePinPosition,
}: {
  index: number;
  pin: Point;
  updatePinPosition: (index: number, x: number, y: number) => void;
}) => {
  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onPanResponderGrant: () => {},
      onPanResponderMove: (evt, gestureState) => {
        updatePinPosition(index, pin.x + gestureState.dx, pin.y + gestureState.dy);
      },
      onPanResponderRelease: () => {},
    })
  ).current;

  return (
    <View
      style={[
        styles.pin,
        {
          left: pin.x - 10,
          top: pin.y - 10,
        },
      ]}
      {...panResponder.panHandlers}
    >
      <View style={styles.pinInner} />
      <Text style={styles.pinText}>
        ({pin.x.toFixed(2)}, {pin.y.toFixed(2)})
      </Text>
    </View>
  );
};

export default function ImagePinHighlighter(): JSX.Element {
  const route = useRoute();
  const { imageName } = route.params as { imageName: string };
  const imageRef = useRef<View>(null);

  const initialPins: Point[] = [
    { x: 50, y: 50 },
    { x: 200, y: 50 },
    { x: 200, y: 150 },
    { x: 50, y: 150 },
  ];

  const [pins, setPins] = useState<Point[]>(initialPins);
  const [savedPins, setSavedPins] = useState<Point[] | null>(null);

  const updatePinPosition = (index: number, x: number, y: number) => {
    setPins((prevPins) => {
      const newPins = [...prevPins];
      newPins[index] = { x, y };
      return newPins;
    });
  };

  const getPolygonPoints = () => {
    return pins.map((pin) => `${pin.x},${pin.y}`).join(' ');
  };

  const savePinPositions = () => {
    setSavedPins(pins);
  };

  return (
    <View style={styles.container}>
      <View ref={imageRef} style={styles.imageContainer}>
        <TouchableWithoutFeedback>
          <Image
            source={{ uri: `${IMAGE_BASE_URL}${imageName}` }}
            style={styles.image}
            testID="image"
          />
        </TouchableWithoutFeedback>
        {/* 以下、ピンやSVGのコード */}
        {pins.length >= 3 && (
          <Svg
            width={IMAGE_WIDTH}
            height={IMAGE_HEIGHT}
            style={StyleSheet.absoluteFill}
          >
            <Polygon
              points={getPolygonPoints()}
              fill="rgba(0, 0, 255, 0.3)"
              stroke="blue"
              strokeWidth={1}
            />
          </Svg>
        )}
        {pins.map((pin, index) => (
          <DraggablePin key={index} index={index} pin={pin} updatePinPosition={updatePinPosition} />
        ))}
      </View>
      {/* ボタンを追加 */}
      <View style={styles.buttonContainer}>
        <Button title="ピンの座標を保存" onPress={savePinPositions} />
      </View>
      {/* 保存されたピンの座標を表示 */}
      {savedPins && (
        <View style={styles.savedPinsContainer}>
          <Text>保存されたピンの座標:</Text>
          {savedPins.map((pin, index) => (
            <Text key={index}>
              ピン {index + 1}: x: {pin.x.toFixed(2)}, y: {pin.y.toFixed(2)}
            </Text>
          ))}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
  imageContainer: {
    width: IMAGE_WIDTH,
    height: IMAGE_HEIGHT,
    backgroundColor: 'rgba(0, 255, 0, 0.2)', // 薄い緑色
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
  },
  pin: {
    position: 'absolute',
    width: 20,
    height: 20,
    alignItems: 'center', // テキストを中央揃え
  },
  pinInner: {
    width: '100%',
    height: '100%',
    backgroundColor: 'red',
    borderRadius: 10,
  },
  pinText: {
    position: 'absolute',
    top: 22, // ピンのすぐ下に表示
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    paddingHorizontal: 4,
    paddingVertical: 2,
    borderRadius: 4,
    fontSize: 12,
  },
  buttonContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
  savedPinsContainer: {
    flexDirection: 'row',  // 横並びに設定
    padding: 10,
    backgroundColor: '#f0f0f0',
    gap: 10,  // ピン間の間隔
    alignItems: 'center',  // 縦方向の中央揃え
  },
});
