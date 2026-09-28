import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Platform } from 'react-native';

export default function LogConsole({ logs, onClear }) {
  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.headerTitle}>REAL-TIME LOG CONSOLE</Text>
        <TouchableOpacity style={styles.clearBtn} onPress={onClear}>
          <Text style={styles.clearBtnText}>Clear Logs</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.scrollArea} nestedScrollEnabled={true}>
        {logs.length === 0 ? (
          <Text style={styles.emptyText}>Logs will appear here as Bluetooth actions execute...</Text>
        ) : (
          logs.map((item, index) => (
            <View key={index} style={styles.logItem}>
              <Text style={styles.timestamp}>[{item.timestamp}]</Text>
              <Text style={[styles.logText, item.isError && styles.errorText]}>
                {item.message}
              </Text>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#0f172a',
    padding: 14,
    borderRadius: 12,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#334155',
    maxHeight: 220,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  headerTitle: {
    fontSize: 11,
    fontWeight: '700',
    color: '#f43f5e',
    letterSpacing: 1,
  },
  clearBtn: {
    backgroundColor: '#334155',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  clearBtnText: {
    color: '#cbd5e1',
    fontSize: 10,
    fontWeight: '600',
  },
  scrollArea: {
    backgroundColor: '#020617',
    padding: 8,
    borderRadius: 6,
    maxHeight: 160,
  },
  emptyText: {
    color: '#475569',
    fontSize: 11,
    fontStyle: 'italic',
  },
  logItem: {
    flexDirection: 'row',
    marginBottom: 4,
    flexWrap: 'wrap',
  },
  timestamp: {
    color: '#64748b',
    fontSize: 10,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    marginRight: 6,
  },
  logText: {
    color: '#e2e8f0',
    fontSize: 11,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    flex: 1,
  },
  errorText: {
    color: '#f87171',
    fontWeight: 'bold',
  },
});
