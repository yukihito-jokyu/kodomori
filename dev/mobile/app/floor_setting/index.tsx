import React, { useEffect, useRef, useState } from 'react';
import { View, Text, TextInput ,StyleSheet, Image, Pressable, Animated, TouchableWithoutFeedback } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import CustomHeader from '@/components/CostomHeader';
import { fetchFrame, postPinAndDistance } from '@/api/Frame';
import { SettingField } from '@/components/FloorSetting/SettingField';

// import { Home, Map, PlayCircle, Settings } from 'lucide-react-native';

interface Distance {
    p1_p2: number;
    p1_p3: number;
    p1_p4: number;
    p2_p3: number;
    p2_p4: number;
    p3_p4: number;
}

interface Point {
    x: number;
    y: number;
}

export default function FloorSetting() {
    const [edit, setEdit] = useState<boolean>(true);
    const [imageData, setImageData] = useState<string | null>(null);
    const [resultImageData, setResultImageData] = useState<string | null>(null);

    const [distance, setDistance] = useState<Distance>({
        p1_p2: 0,
        p1_p3: 0,
        p1_p4: 0,
        p2_p3: 0,
        p2_p4: 0,
        p3_p4: 0,
    });

    const initialPins: Point[] = [
        { x: 50, y: 50 },
        { x: 200, y: 50 },
        { x: 200, y: 150 },
        { x: 50, y: 150 },
    ];
    
    const [pins, setPins] = useState<Point[]>(initialPins);

    const leftPosition = useRef(new Animated.Value(0)).current;

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
    };

    // distanceの値を変更する
    const changeDistance = (key: keyof Distance, text: string): void => {
        const value = parseFloat(text) || 0;
        setDistance(prevState => ({
            ...prevState,
            [key]: value,
        }));
    };

    // distanceの保存
    const handleSave = async () => {
        console.log('Save button clicked');
        const pinAndDistance = {
            p1_p2: distance.p1_p2,
            p1_p3: distance.p1_p3,
            p1_p4: distance.p1_p4,
            p2_p3: distance.p2_p3,
            p2_p4: distance.p2_p4,
            p3_p4: distance.p3_p4,
            pin_1_x: pins[0].x,
            pin_1_y: pins[0].y,
            pin_2_x: pins[1].x,
            pin_2_y: pins[1].y,
            pin_3_x: pins[2].x,
            pin_3_y: pins[2].y,
            pin_4_x: pins[3].x,
            pin_4_y: pins[3].y,
        }
        const result = await postPinAndDistance(pinAndDistance);
        if (result.warped_base64) {
            console.log("成功");
            setResultImageData(`data:image/jpeg;base64,${result.warped_base64}`);
        } else {
            console.log("失敗");
        }
    };

    useEffect(() => {
        const fetchImage = async () => {
            const result = await fetchFrame();
            if (result.frame_base64) {
                setImageData(`data:image/jpeg;base64,${result.frame_base64}`);
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
                <View style={styles.pointBoxLeft}>
                    <View style={styles.pointInputBox}>
                        <Text style={styles.pointInputText}>Distance P1 to P2</Text>
                        <TextInput
                            style={styles.pointInput}
                            value={distance.p1_p2.toString()}
                            onChangeText={(text) => changeDistance("p1_p2", text)}
                            placeholder="Enter distance p1_p2"
                            keyboardType="numeric"
                        />
                    </View>
                    <View style={styles.pointInputBox}>
                        <Text style={styles.pointInputText}>Distance P1 to P3</Text>
                        <TextInput
                            style={styles.pointInput}
                            value={distance.p1_p3.toString()}
                            onChangeText={(text) => changeDistance("p1_p3", text)}
                            placeholder="Enter distance p1_p3"
                            keyboardType="numeric"
                        />
                    </View>
                    <View style={styles.pointInputBox}>
                        <Text style={styles.pointInputText}>Distance P1 to P4</Text>
                        <TextInput
                            style={styles.pointInput}
                            value={distance.p1_p4.toString()}
                            onChangeText={(text) => changeDistance("p1_p4", text)}
                            placeholder="Enter distance p1_p4"
                            keyboardType="numeric"
                        />
                    </View>
                    <View style={styles.pointInputBox}>
                        <Text style={styles.pointInputText}>Distance P2 to P3</Text>
                        <TextInput
                            style={styles.pointInput}
                            value={distance.p2_p3.toString()}
                            onChangeText={(text) => changeDistance("p2_p3", text)}
                            placeholder="Enter distance p2_p3"
                            keyboardType="numeric"
                        />
                    </View>
                    <View style={styles.pointInputBox}>
                        <Text style={styles.pointInputText}>Distance P2 to P4</Text>
                        <TextInput
                            style={styles.pointInput}
                            value={distance.p2_p4.toString()}
                            onChangeText={(text) => changeDistance("p2_p4", text)}
                            placeholder="Enter distance p2_p4"
                            keyboardType="numeric"
                        />
                    </View>
                    <View style={styles.pointInputBox}>
                        <Text style={styles.pointInputText}>Distance P3 to P4</Text>
                        <TextInput
                            style={styles.pointInput}
                            value={distance.p3_p4.toString()}
                            onChangeText={(text) => changeDistance("p3_p4", text)}
                            placeholder="Enter distance p3_p4"
                            keyboardType="numeric"
                        />
                    </View>
                </View>
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
        flexDirection: "row",
        width: "100%",
        height: 400,
    },
    pointBoxLeft: {
        width: "40%",
    },
    pointBoxRight: {
        width: "60%",
        backgroundColor: "#D9D9D9",
    },
    pointInputBox: {
        marginLeft: 30,
        marginBottom: 25,
    },
    pointInputText: {
        color: "#202E78",
        fontSize: 16,
    },
    pointInput: {
        width: "70%",
        backgroundColor: "#D9D9D9",
        borderRadius: 10,
    },
    pointImage: {
        width: "100%",
        height: "100%",
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
        width: 500,
        height: 500,
    }
});
