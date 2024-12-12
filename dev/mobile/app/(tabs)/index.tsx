import { View, Text, StyleSheet } from 'react-native';
import { Link } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Home, Map, PlayCircle, Settings } from 'lucide-react-native';

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>ホーム画面</Text>
        <Text style={styles.description}>アプリのメイン画面です。</Text>
      </View>
      <View style={styles.footer}>
        <Link href="/" style={styles.navItem}>
          <Home size={24} color="#007AFF" />
          <Text style={styles.navText}>ホーム</Text>
        </Link>
        <Link href="/area" style={styles.navItem}>
          <Map size={24} color="#007AFF" />
          <Text style={styles.navText}>エリア指定</Text>
        </Link>
        <Link href="/log" style={styles.navItem}>
          <PlayCircle size={24} color="#007AFF" />
          <Text style={styles.navText}>ログ再生</Text>
        </Link>
        <Link href="/settings" style={styles.navItem}>
          <Settings size={24} color="#007AFF" />
          <Text style={styles.navText}>設定</Text>
        </Link>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  description: {
    fontSize: 16,
    color: '#666',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingVertical: 8,
  },
  navItem: {
    alignItems: 'center',
  },
  navText: {
    fontSize: 12,
    marginTop: 4,
    color: '#007AFF',
  },
});

