import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

interface CustomHeaderNurseryProps {
  onMenuPress: () => void; // メニューアイコンを押したときの処理
}

const CustomHeaderNursery: React.FC<CustomHeaderNurseryProps> = ({ onMenuPress }) => {
  return (
    <View style={styles.header}>
      {/* メニューデザイン */}
      <TouchableOpacity style={styles.menuIcon} onPress={onMenuPress}>
        <MaterialIcons name="menu" size={24} color="white" />
      </TouchableOpacity>
      {/* ヘッダー中央のテキスト（必要に応じて追加可能） */}
      <Text style={styles.headerText}></Text>
      {/* メールアイコン */}
      <View style={styles.rightIcons}>
        <View style={styles.notificationDot} />
        <Image
          source={require('../assets/images/mail_32dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.png')} // アイコンの相対パス
          style={styles.mailIcon}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    height: 60,
    backgroundColor: '#202E78', 
    flexDirection: 'row', 
    alignItems: 'center',
    justifyContent: 'space-between',
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
  rightIcons: {
    flexDirection: 'row',
    alignItems: 'center',
    position: 'relative',
  },
  notificationDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#06D6A0',
    position: 'absolute',
    top: -5,
    right: -5,
    zIndex: 1,
  },
  mailIcon: {
    width: 34,
    height: 34,
    marginLeft: 10,
  },
});

export default CustomHeaderNursery;
