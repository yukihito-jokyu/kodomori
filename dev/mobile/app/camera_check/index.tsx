import React from 'react'
import { Image, SafeAreaView, StyleSheet, Text, View } from 'react-native'
import CustomHeaderNursery from '@/components/ContomHeaerNursery';

export default function CameraCheckScreen() {
    const handleMenuPress = (): void => {
        alert('メニューがタップされました');
      };
    return (
        <SafeAreaView style={styles.pearent}>
            <CustomHeaderNursery onMenuPress={handleMenuPress} />
            <View style={styles.children}>
                <Text style={styles.cameraName}>カメラの場所の名前</Text>
                <Image style={styles.cameraImage}></Image>
                <View style={styles.backButtonWrapper}>
                    <View style={styles.backButton}>
                        <Text style={styles.backButtonText}>戻る</Text>
                    </View>
                </View>
            </View>
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
    cameraImage: {
        width: "100%",
        height: 450,
        backgroundColor: "#D9D9D9"
        
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
});