import { Stack } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function Layout() {
  return (
    <SafeAreaProvider>
      <Stack>
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="dangerous_area" options={{ title: 'エリア指定' }} />
        <Stack.Screen name="log" options={{ title: 'ログ再生' }} />
        <Stack.Screen name="settings" options={{ title: '設定' }} />
        <Stack.Screen name="test" options={{ title: 'テスト' }} />
      </Stack>
    </SafeAreaProvider>
  );
}