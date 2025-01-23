import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link } from 'expo-router';
import { fetchFrame } from '@/api/Frame';
import ImagePinHighlighter from './ImagePinHighlighter';

const IMAGE_BASE_URL = 'http://127.0.0.1:8000/get-image/'; // 画像取得エンドポイントのベースURL

export default function AreaScreen() {
  const [images, setImages] = useState<string>();

  useEffect(() => {
    // 画像リストを取得する関数
    const fetchImages = async () => {
      console.log('fetchImages started');
      try {
        // const response = await fetch('http://127.0.0.1:8000/list-images/');
        const response = await fetchFrame();
        console.log('response', response.frame_base64);
        // const data = await response.json();
        // console.log('data', data);
        setImages(`data:image/jpeg;base64,${response.frame_base64}`);
      } catch (error) {
        console.error('Error fetching images:', error);
      } finally {
        console.log('fetchImages finished');
      }
    };

    fetchImages();
  }, []);

  const renderItem = ({ item }: { item: string }) => (
    <TouchableOpacity>
      <Link href={{ pathname: '/dangerous_area/area_select', params: { imageName: item } }}>
        <Text style={styles.imageItem}>{item}</Text>
      </Link>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      {/* <FlatList
        data={images}
        renderItem={renderItem}
        keyExtractor={(item) => item}
      /> */}
      {/* <View>
        {images ? (
          <Image
            style={styles.pointImage} 
            source={{ uri: images }}
          />
          // <Text>Waiting for image...</Text>
        ) : (
          <Text>Waiting for data...</Text>
        )}
      </View> */}
      <ImagePinHighlighter />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  imageItem: {
    padding: 10,
    fontSize: 18,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  pointImage: {
    width: "100%",
    height: 500,
    borderColor: "#D9D9D9",
    borderWidth: 8,
  }
});
