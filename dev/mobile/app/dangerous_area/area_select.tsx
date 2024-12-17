import React from 'react';
import { SafeAreaView, Text, StyleSheet } from 'react-native';

import ImagePinHighlighter from './ImagePinHighlighter';



export default function ImageScreen() {
  

  return (
    <SafeAreaView style={styles.container}>
      <ImagePinHighlighter />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginVertical: 16,
  },
});