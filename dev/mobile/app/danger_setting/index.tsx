import React, { useRef, useState } from 'react';
import { View, Text, TextInput ,StyleSheet, Image, Pressable, Animated } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

// import { Home, Map, PlayCircle, Settings } from 'lucide-react-native';

export default function FloorSetting() {
    const [edit, setEdit] = useState<boolean>(true);
    const leftPosition = useRef(new Animated.Value(0)).current;

    const handleChangeEdit = () => {
        Animated.timing(leftPosition, {
            toValue: edit ? 50 : 0,
            duration: 300, // アニメーションの長さ（ミリ秒）
            useNativeDriver: false,
        }).start();

        setEdit(!edit);
    }
    return (
        <SafeAreaView>
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
                <Image style={styles.pointImage}></Image>
            </View>
            <View style={styles.saveButtonWrapper}>
                <View style={styles.saveButton}>
                    <Text style={styles.saveButtonText}>保存</Text>
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
        height: 450,
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
});
