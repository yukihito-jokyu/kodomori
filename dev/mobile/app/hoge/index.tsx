import { View, Text, StyleSheet } from 'react-native';
import React from 'react'

export default function index() {
    return (
    <View style={styles.parent}>
        <View style={styles.children1}></View>
        <View style={styles.children2}></View>
    </View>
    )
}

const styles = StyleSheet.create({
    parent: {
        position: "relative",
        width: "100%",
        height: "100%",
    },
    children1: {
        position: "absolute",
        left: 0,
        top: 0,
        width: 10,
        height: 10,
        borderRadius: 5,
        backgroundColor: "black",
    },
    children2: {
        position: "absolute",
        left: 1590,
        top: 0,
        width: 10,
        height: 10,
        borderRadius: 5,
        backgroundColor: "black",
    },
});
