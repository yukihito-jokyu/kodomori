import React from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';

type Props = {
    checked: boolean;
    name: string;
    time: string;
}

const AlertTileEnd: React.FC<Props> = ({ checked, name, time }) => {
    return (
        <View style={styles.tilePearent}>
            <View style={styles.tileChildren}>
                <Text style={styles.alertTileText}>{time}</Text>
                <View style={styles.alertTile}>
                    <View style={styles.alertTileSVGWrapper}>
                        {checked ? (
                            <Image
                                source={require("../../assets/svgs/open_main.svg")}
                                style={styles.alertTileSVG}
                            />
                        ) : (
                            <Image
                                source={require("../../assets/svgs/close_mail.svg")}
                                style={styles.alertTileSVG}
                            />
                        )}
                        
                    </View>
                    <View style={styles.alertTileTextContent}>
                        <Text style={styles.alertTileText}>{name}の場所で園児が危険エリアに入りそうです</Text>
                    </View>
                </View>
                <View style={styles.tileLeftBox}>
                    <View style={styles.tileLeft}>
                        <View style={styles.slant}></View>
                        <View style={styles.vertical}></View>
                        <View style={styles.vertical2}></View>
                        <View style={styles.vertical3}></View>
                        <View style={styles.vertical4}></View>
                    </View>
                </View>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    tilePearent: {
        width: "100%",
        height: 200,
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    tileChildren: {
        position: "relative",
        width: "80%"
    },
    tileLeftBox: {
        position: "absolute",
        width: "10%",
        height: 200,
        left: "-10%",
        top: "55%"
    },
    slant: {
        position: "absolute",
        width: "100%",
        borderStyle: "solid",
        borderWidth: 3,
        borderColor: "#202E78",
        transform: "rotate(-45deg)",
        right: -10,
        top: 18
    },
    vertical: {
        position: "absolute",
        height: 50,
        borderStyle: "solid",
        borderWidth: 3,
        borderColor: "#202E78",
        right: 40,
        top: 40,
    },
    vertical2: {
        position: "absolute",
        height: 15,
        borderStyle: "solid",
        borderWidth: 3,
        borderColor: "#202E78",
        right: 40,
        top: 92,
    },
    vertical3: {
        position: "absolute",
        height: 10,
        borderStyle: "solid",
        borderWidth: 3,
        borderColor: "#202E78",
        right: 40,
        top: 109,
    },
    vertical4: {
        position: "absolute",
        height: 5,
        borderStyle: "solid",
        borderWidth: 3,
        borderColor: "#202E78",
        right: 40,
        top: 121,
    },
    tileLeft: {
        position: "relative",
        width: "100%",
        height: "100%",
    },
    alertTimeText: {},
    alertTile: {
        display: "flex",
        flexDirection: "row",
        width: "100%",
        height: 100,
        borderStyle: "solid",
        borderWidth: 3,
        borderColor: "#202E78",
        borderRadius: 15,
        backgroundColor: "rgba(227, 232, 203, 0.3)"
    },
    alertTileSVGWrapper: {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        width: 90,
        height: 90,
    },
    alertTileSVG: {
        width: 50,
        height: 50,
    },
    alertTileTextContent: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: 90
    },
    alertTileText: {
        color: "#202E78"
    }
})

export default AlertTileEnd;