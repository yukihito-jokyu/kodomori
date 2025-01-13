import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

interface CustomHeaderProps {
  onMenuPress: () => void; // メニューアイコンを押したときの処理
}

const CustomHeader: React.FC<CustomHeaderProps> = ({ onMenuPress }) => {
  return (
    <View style={styles.header}>
      {/* メニューデザイン */}
      <TouchableOpacity style={styles.menuIcon} onPress={onMenuPress}>
        <MaterialIcons name="menu" size={24} color="white" />
      </TouchableOpacity>
      {/* ヘッダー中央のテキスト（必要に応じて追加可能） */}
      <Text style={styles.headerText}></Text>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    height: 60,
    backgroundColor: '#202E78', 
    flexDirection: 'row', 
    alignItems: 'center',
    paddingHorizontal: 10, 
  },
  menuIcon: {
    marginRight: 15, 
  },
  headerText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default CustomHeader;
