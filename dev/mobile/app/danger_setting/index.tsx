import React, { useEffect, useRef, useState } from 'react';
import { View, Text, TextInput ,StyleSheet, Image, Pressable, Animated, TouchableWithoutFeedback } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import CustomHeader from '@/components/CostomHeader';
import { SettingField } from '@/components/FloorSetting/SettingField';
import { fetchWrap, postPin } from '@/api/Frame';
import { useRouter } from 'expo-router';

interface Point {
    x: number;
    y: number;
}

const IMAGE_WIDTH = 440;
const IMAGE_HEIGHT = 330;

export default function FloorSetting() {
    const [edit, setEdit] = useState<boolean>(true);
    const leftPosition = useRef(new Animated.Value(0)).current;
    const [imageData, setImageData] = useState<string | null>(null);
    const [height, setHeight] = useState<number | null> (null);
    const [width, setWidth] = useState<number | null> (null);
    const [resultImageData, setResultImageData] = useState<string | null>(null);

    const initialPins: Point[] = [
        { x: 50, y: 50 },
        { x: 200, y: 50 },
        { x: 200, y: 150 },
        { x: 50, y: 150 },
    ];
    
    const [pins, setPins] = useState<Point[]>(initialPins);
    const router = useRouter();

    const handleMenuPress = (): void => {
        alert('メニューがタップされました');
      };

    const handleChangeEdit = () => {
        Animated.timing(leftPosition, {
            toValue: edit ? 50 : 0,
            duration: 300, // アニメーションの長さ（ミリ秒）
            useNativeDriver: false,
        }).start();

        setEdit(!edit);
    }

    const handleSave = async () => {
        if (width && height) {
            const pin = {
                pin_1_x: pins[0].x * width / IMAGE_WIDTH,
                pin_1_y: pins[0].y * height / IMAGE_HEIGHT,
                pin_2_x: pins[1].x * width / IMAGE_WIDTH,
                pin_2_y: pins[1].y * height / IMAGE_HEIGHT,
                pin_3_x: pins[2].x * width / IMAGE_WIDTH,
                pin_3_y: pins[2].y * height / IMAGE_HEIGHT,
                pin_4_x: pins[3].x * width / IMAGE_WIDTH,
                pin_4_y: pins[3].y * height / IMAGE_HEIGHT,
            }
            const result = await postPin(pin);
            if (result.warped_with_zone) {
                setResultImageData(`data:image/jpeg;base64,${result.warped_with_zone}`);
                console.log(result.warped_with_zone)
            }
        }
    }

    useEffect(() => {
        const fetchImage = async () => {
            const result = await fetchWrap();
            if (result.wrap_base64) {
                setImageData(`data:image/jpeg;base64,${result.wrap_base64}`);
                console.log(result.height);
                console.log(result.width);
                setHeight(result.height);
                setWidth(result.width);
            } else {
                console.log("失敗");
            }
        }

        fetchImage();
    }, []);
    return (
        <SafeAreaView>
            <CustomHeader onMenuPress={handleMenuPress} />
            <View style={styles.changeButtonParent}>
                <View style={styles.changeButtonWrapper}>
                    <Animated.View style={[
                        styles.changeButton,
                        {
                            left: leftPosition,
                            backgroundColor: edit ? "#06D6A0" : "#FF5D99"
                        }
                    ]}>
                        <Pressable
                            style={{
                                width: "100%",
                                height: "100%",
                                justifyContent: "center",
                                alignItems: "center"
                            }}
                            onPress={handleChangeEdit}
                        >
                            <Text
                                style={{
                                    color: "#FFFFFF"
                                }}
                            >
                                { edit ? "ポイント編集モード" : "ポイント追加モード" }
                            </Text>
                        </Pressable>
                    </Animated.View>
                </View>
            </View>
            <View style={styles.pointBox}>
                {/* <Image style={styles.pointImage}></Image> */}
                {imageData && (
                    <SettingField pins={pins} setPins={setPins} imageData={imageData} />
                )}
            </View>
            <View style={styles.saveButtonWrapper}>
                <TouchableWithoutFeedback onPress={handleSave}>
                    <View style={styles.saveButton}>
                        <Text style={styles.saveButtonText}>保存</Text>
                    </View>
                </TouchableWithoutFeedback>
            </View>
            <View style={styles.resultImageWrapper}>
                <Text style={styles.resultText}>結果</Text>
                <View>
                    {resultImageData && (
                        <Image
                            source={{ uri: resultImageData }}
                            style={styles.resultImage}
                            testID="image"
                        />
                    )}
                </View>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    changeButtonParent: {
        width: "100%",
        height: 100,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    changeButtonWrapper: {
        position: "relative",
        width: 200,
        height: 30,
        backgroundColor: "#D9D9D9",
        borderRadius: 20,
    },
    changeButton: {
        position: "absolute",
        left: 50,
        width: 150,
        height: 30,
        backgroundColor: "#FF5D99",
        borderRadius: 20,
    },
    pointBox: {
        display: "flex",
        width: "100%",
        // height: 450,
        justifyContent: "center",
        alignItems: "center",
    },
    pointImage: {
        width: "80%",
        height: "100%",
        backgroundColor: "#D9D9D9",
    },
    saveButtonWrapper: {
        width: "100%",
        marginTop: 50,
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    saveButton: {
        width: 150,
        height: 30,
        backgroundColor: "#202E78",
        borderRadius: 20,
        justifyContent: "center",
        alignItems: "center"
    },
    saveButtonText: {
        color: "#FFFFFF",
        fontSize: 16,
    },
    resultImageWrapper: {
        display: "flex",
        // justifyContent: "center",
        alignItems: "center",
        width: "100%",
        height: 600,
    },
    resultText: {
        marginTop: 20,
    },
    resultImage: {
        width: 440,
        height: 330,
    }
});
