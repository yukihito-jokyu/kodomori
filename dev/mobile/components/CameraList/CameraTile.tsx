import React from 'react'
import { Image, Text, View, StyleSheet } from 'react-native'

type Props = {
    name: string;
    picture: string;
    dangerous: boolean;
};

const CameraTile: React.FC<Props> = ({ name, picture, dangerous }) => {
    return (
        <View style={styles.tilePearent}>
            <View style={styles.tileChildren}>
                <Image style={styles.tileImage}></Image>
                <View style={styles.tileCommentContent}>
                    <View style={styles.tileCommentContentTop}>
                        <Text style={styles.tileCommentContentTopText}>カメラの場所</Text>
                        <Text style={styles.tileCommentContentTopText}>
                            現在このカメラの場所は
                            <Text style={{ color: dangerous ? "#FC1F23" : "#202E78" }}>
                                {dangerous ? "危険" : "安全"}
                            </Text>
                            です！
                        </Text>
                    </View>
                    <View style={styles.tileCommentContentBottom}>
                        <View style={[styles.tileContentButton, { backgroundColor: dangerous ? "#FF0000" : "#06D6A0"}]}>
                            <Text style={styles.tileContentButtonText}>カメラ確認</Text>
                        </View>
                    </View>
                </View>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    tilePearent: {
        width: "100%",
        height: 250,
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    tileChildren: {
        display: "flex",
        flexDirection: "row",
        width: "80%",
        height: 200,
        borderStyle: "solid",
        borderWidth: 5,
        borderColor: "#202E78",
        borderRadius: 20,
    },
    tileImage: {
        width: "30%",
        height: "100%",
        backgroundColor: "#D9D9D9",
        borderTopLeftRadius: 17,
        borderBottomLeftRadius: 17,
    },
    tileCommentContent: {
        width: "70%",
        backgroundColor: "rgba(227, 232, 203, 0.38)",
        borderTopRightRadius: 17,
        borderBottomRightRadius: 17,
    },
    tileCommentContentTop: {
        width: "100%",
        height: 140,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 20,
    },
    tileCommentContentTopText: {
        fontSize: 20
    },
    tileCommentContentBottom: {
        width: "100%",
        height: 40,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
    tileContentButton: {
        width: 120,
        height: 25,
        backgroundColor: "#06D6A0",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 10,
    },
    tileContentButtonText: {
        fontSize: 15,
        color: "#FFFFFF"
    }
});

export default CameraTile;