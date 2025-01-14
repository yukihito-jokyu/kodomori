
import React, { useState } from 'react';
import { View, Text, TextInput ,StyleSheet, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link,Stack } from 'expo-router';
import CameraTile from '@/components/CameraList/CameraTile';

// import { Home, Map, PlayCircle, Settings } from 'lucide-react-native';

export default function CameraListScreen() {
    const [tiles, SetTiles] = useState([{
        name: "a",
        picture: "",
        dangerous: false,
    },
    {
        name: "b",
        picture: "",
        dangerous: true,
    }])
    return (
        <SafeAreaView>
            {tiles.map((tile, index) => (
                <CameraTile key={index} name={tile.name} picture={tile.picture} dangerous={tile.dangerous} />
            ))}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({});
