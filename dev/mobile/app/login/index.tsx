
import React, { useState} from 'react';
import { View, Text, TextInput ,StyleSheet, TouchableOpacity,Alert} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import {Stack,useRouter } from 'expo-router';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';

export default function LoginScreen() {
    const[loginID,setLoginID] = useState('');
    const router = useRouter();

    const handleLogin = () => {
      if (loginID === "0") {
        router.push("/menu"); // loginIDが"0"なら"/menu"に遷移
      } else if (loginID === "1") {
        router.push("/"); // loginIDが"1"なら"/"に遷移
      } else {
        alert("Invalid Login ID"); // 無効なIDの場合はアラート表示
      }
    };
  
    return (
        
        <SafeAreaView style={styles.container}>
          <View style={styles.box}>
            <Text style={styles.title}>kodomori</Text>
            <Text style={styles.label}>LOGIN ID</Text>
            <TextInput
              style={styles.input}
              value={loginID}
              onChangeText={setLoginID}
              placeholder="Enter Login ID"
              placeholderTextColor="#888"
              keyboardType="numeric" // 数字入力を強制
            />
            <TouchableOpacity style={styles.button} onPress={handleLogin} activeOpacity={1}>
                <Text style={styles.buttonText}>LOGIN</Text>
            </TouchableOpacity>
            <Stack>
                <Stack.Screen name="login" options={{ headerShown: false }} />
            </Stack>

          </View>
          
        </SafeAreaView>
        
      );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
        padding: 16,
      },
      box: {
        width: '65%',
        padding: 100,
        borderWidth: 2,
        borderColor: '#001D6C',
        borderRadius: 10,
        alignItems: 'center',
        backgroundColor: '#fff',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.3,
        shadowRadius: 4,
        elevation: 5,
      },
      title: {
        fontSize: 40,
        fontWeight: 'bold',
        color: '#001D6C',
        marginBottom: 50,
      },
      label: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#001D6C',
        alignSelf: 'flex-start',
        marginBottom: 8,
      },
      input: {
        width: '105%',
        height: 40,
        borderColor: '#ccc',
        borderWidth: 1,
        borderRadius: 5,
        paddingHorizontal: 10,
        marginBottom: 50,
        backgroundColor: '#f9f9f9',
      },
      button: {
        backgroundColor: '#001D6C',
        paddingVertical: 10,
        paddingHorizontal: 20,
        borderRadius: 20,
        alignItems: 'center',
        width: '50%',
      },
      buttonText: {
        color: '#fff',
        fontWeight: 'bold',
        textAlign: 'center',
      },
});
