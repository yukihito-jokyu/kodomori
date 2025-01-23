import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link } from 'expo-router';
import CustomHeaderNursery from '@/components/ContomHeaerNursery';

const IMAGE_BASE_URL = 'http://127.0.0.1:8000/get-image/'; // 画像取得エンドポイントのベースURL

export default function AreaScreen() {
  const [images, setImages] = useState<string[]>([]);

  useEffect(() => {
    // 画像リストを取得する関数
    const fetchImages = async () => {
      console.log('fetchImages started');
      try {
        const response = await fetch('http://127.0.0.1:8000/list-images/');
        console.log('response', response);
        const data = await response.json();
        console.log('data', data);
        setImages(data.images);
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

  const handleMenuPress = (): void => {
    alert('メニューがタップされました');
  };

  return (
    <SafeAreaView style={styles.container}>
      <CustomHeaderNursery onMenuPress={handleMenuPress} />
      <FlatList
        data={images}
        renderItem={renderItem}
        keyExtractor={(item) => item}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  imageItem: {
    padding: 10,
    fontSize: 18,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
});
