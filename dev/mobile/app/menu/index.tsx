import React, { useState } from 'react';
import CustomHeader from '@/components/CostomHeader';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  FlatList,
  Image,
  ListRenderItem,
} from 'react-native';

interface DropdownItem {
  id: string;
  label: string;
}

interface Camera {
  id: string;
  name: string;
  status: string;
  set_button: string;
  dropdownItems: DropdownItem[];
}


const CameraCard: React.FC = () => {
  const [dropdownStates, setDropdownStates] = useState<Record<string, boolean>>({});


  // カメラ場所のデータとそれぞれのプルダウンアイテム
  const [cameras] = useState<Camera[]>([
    {
      id: '1',
      name: 'カメラ場所の名前',
      status: '危険エリア n 箇所設定中',
      set_button: 'カメラ確認',
      dropdownItems: [
        { id: '1-1', label: '危険エリアA' },
        { id: '1-2', label: '危険エリアB' },
      ],
    },
    {
      id: '2',
      name: 'カメラ場所の名前',
      status: '危険エリア n 箇所設定中',
      set_button: '危険エリア追加',
      dropdownItems: [
        { id: '2-1', label: '危険エリアC' },
        { id: '2-2', label: '危険エリアD' },
      ],
    },
    {
      id: '3',
      name: 'カメラ場所の名前',
      status: '危険エリア n 箇所設定中',
      set_button: '床エリア追加',
      dropdownItems: [
        // { id: '3-1', label: '床エリア1' },
        // { id: '3-2', label: '床エリア2' },
      ],
    },
  ]);

  // プルダウンの表示切り替え関数
  const toggleDropdown = (id: string) => {
    setDropdownStates((prevStates) => ({
      ...prevStates,
      [id]: !prevStates[id],
    }));
  };

  const handleMenuPress = (): void => {
    alert('メニューがタップされました');
  };

  // プルダウンメニューのアイテムをレンダリングする関数
  const renderDropdownItem: ListRenderItem<DropdownItem> = ({ item }) => (
    <View style={styles.dropdownItem}>
      <View style={styles.imageContainer}>
        <Image
          source={{ uri: 'https://via.placeholder.com/100' }} //textにして、'画像'と文字を表示することも可能
          style={styles.image}
        />
      </View>
      <View style={styles.textContainer}>
        <Text style={styles.itemLabel}>{item.label}</Text>
        <View style={styles.actionButtons}>
          <TouchableOpacity style={styles.editButton}>
            <Text style={styles.buttonText}>編集</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.deleteButton}>
            <Text style={styles.buttonText}>削除</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );

  return (
    <View style={{ flex: 1 }}>
      {/* ヘッダーを追加 */}
      <CustomHeader onMenuPress={handleMenuPress} />
      {cameras.map((camera) => (
        <View key={camera.id}>
          {/* 各カード */}
          <TouchableOpacity
            style={styles.container}
            onPress={() => toggleDropdown(camera.id)}
          >
            <View style={styles.imageContainer}>
              <Image
                source={{ uri: 'https://via.placeholder.com/100' }} //textにして、'画像'と文字を表示することも可能
                style={styles.image}
              />
            </View>
            <View style={styles.textContainer}>
              <Text style={styles.cameraName}>{camera.name}</Text>
              {/* 未設定の場合、statusを更新して'エリア未設定！'と表示 */}
              {camera.dropdownItems.length === 0 ? (
                  <Text style={[styles.status, styles.unsetStatus]}>エリア未設定！</Text>
                ) : (
                  <Text style={styles.status}>
                    危険エリア{' '}
                    <Text style={styles.number}>{camera.dropdownItems.length}</Text> 箇所設定中
                  </Text>
                )}
              <TouchableOpacity
                style={
                  camera.set_button === 'カメラ確認'
                    ? styles.check_button
                    : camera.set_button === '危険エリア追加'
                    ? styles.danger_button
                    : styles.floor_button
                }
              >
                <Text style={styles.buttonText}>{camera.set_button}</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.arrowContainer}>
              <Text style={styles.arrow}>
                {dropdownStates[camera.id] ? '▼' : '▶'}
              </Text>
            </View>
          </TouchableOpacity>

          {/* プルダウンメニュー */}
          {dropdownStates[camera.id] && (
            <View style={styles.dropdown}>
              <FlatList
                data={camera.dropdownItems} // カメラごとのデータを利用
                keyExtractor={(item) => item.id}
                renderItem={renderDropdownItem}
              />
            </View>
          )}
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row', 
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 0,
    paddingVertical: 10, 
    borderWidth: 1,
    borderColor: '#001D6C',
    borderRadius: 10,
    backgroundColor: '#F8F8F4',
    width: '90%',
    alignSelf: 'center',
    marginVertical: 10,
  },
  imageContainer: {
    width: '25%',
    height: '120%',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#E6E6E6',
    borderRadius: 10,
  },
  image: {
    width: 60,
    height: 60,
    borderRadius: 5,
  },  
  textContainer: {
    flex: 3,
    marginHorizontal: 10,
  },
  statusAndArrow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 5,
  },
  cameraName: {
    fontSize: 13,
    color: '#000000',
    alignSelf: 'center',
    padding:7,
  },
  status: {
    fontSize: 14,
    color: '#555',
    flex: 1, 
    alignSelf: 'center',
    padding:7,
  },
  unsetStatus: {
    color: '#FF0000', 
  },
  number:{
    color: '#FF0000', 
  },
  check_button:{
    backgroundColor: '#06D6A0',
    paddingHorizontal: 1,
    paddingVertical: 5,
    borderRadius: 10,
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 10,
    textAlign: 'center',
    width: 90,
    alignSelf: 'center', 
  },
  danger_button:{
    backgroundColor: '#FC1F23',
    paddingHorizontal: 1,
    paddingVertical: 5,
    borderRadius: 10,
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 10,
    textAlign: 'center',
    width: 90,
    alignSelf: 'center', 
  },
  floor_button:{
    backgroundColor: '#202E78',
    paddingHorizontal: 1,
    paddingVertical: 5,
    borderRadius: 10,
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 10,
    textAlign: 'center',
    width: 90,
    alignSelf: 'center',
  },
  arrowContainer: {
    justifyContent: 'center',
    alignItems: 'center', 
  },
  arrow: {
    fontSize: 18,
    color: '#001D6C',
    marginBottom: 5, 
    marginRight:10,
  },
  
  dropdown: {
    width: '90%',
    alignSelf: 'center',
    marginVertical: 10,
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: 'transparent',
    borderRadius: 10,
    padding: 10,
  },
  dropdownItem: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#001D6C',
    borderRadius: 0,
    padding: 10,
    marginVertical: 5,
  },
  itemLabel: {
    fontSize: 13,
    color: '#000000',
    fontWeight: 'bold',
    alignSelf: 'center',
    marginBottom: 5,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    width: '50%',
    alignSelf: 'center',
    marginTop: 5,
  },
  editButton: {
    backgroundColor: '#06D6A0',
    height:25,
    paddingHorizontal: 20,
    borderRadius: 5,
    marginRight: 10,
  },
  deleteButton: {
    backgroundColor: '#FC1F23',
    height:25,
    paddingHorizontal: 20,
    borderRadius: 5,
  }, 
  buttonText: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 10,
    textAlign: 'center',
    lineHeight:25,
  },
  
});

export default CameraCard;

