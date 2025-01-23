import React, { useEffect, useRef, useState } from 'react'
import { Button, Image, PanResponder, StyleSheet, Text, TouchableWithoutFeedback, View } from 'react-native'
import Svg, { Polygon } from 'react-native-svg'

interface Point {
    x: number;
    y: number;
}

const IMAGE_WIDTH = 440;
const IMAGE_HEIGHT = 330;

function fixPoint(x: number, y: number): {pointX: number, pointY: number} {
    let pointX = x
    let pointY = y
    if (x < 0) {
        pointX = 0
    } else if (x > IMAGE_WIDTH) {
        pointX = IMAGE_WIDTH
    }
    if (y < 0) {
        pointY = 0
    } else if (y > IMAGE_HEIGHT) {
        pointY = IMAGE_HEIGHT
    }
    return { pointX: pointX, pointY: pointY }
}

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
            const points = fixPoint(pin.x + gestureState.dx, pin.y + gestureState.dy)
            updatePinPosition(index, points.pointX, points.pointY);
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

interface SettingFieldProps {
    pins: Point[];
    setPins: React.Dispatch<React.SetStateAction<Point[]>>;
    imageData: string;
}


export function SettingField({pins, setPins, imageData}: SettingFieldProps) {
    const imageRef = useRef<View>(null);

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
    

    return (
        <View style={styles.container}>
            <View ref={imageRef} style={styles.imageContainer}>
            <TouchableWithoutFeedback>
                {imageData ? (
                <Image
                    source={{ uri: imageData }}
                    style={styles.image}
                    testID="image"
                />
                ) : (
                <Text>Waiting for data...</Text>
                )}
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
        </View>
    )
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
        width: IMAGE_WIDTH,
        height: IMAGE_HEIGHT,
        resizeMode: 'stretch',
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
})
