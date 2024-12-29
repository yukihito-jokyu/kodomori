
import React, { useState} from 'react';
import { View, Text, TextInput ,StyleSheet, TouchableOpacity} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link,Stack } from 'expo-router';

// import { Home, Map, PlayCircle, Settings } from 'lucide-react-native';

export default function LoginScreen() {
    const[loginID,setLoginID] = useState('');


  
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
            />
            <TouchableOpacity style={styles.button}>
                <Link href="/">
                <Text style={styles.buttonText}>LOGIN</Text>
                </Link>
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
