import React from 'react';
import { View, Text, StyleSheet, Platform } from 'react-native';
import { SERVICE_UUID, CHAR_UUID } from '../services/bleService';

export default function Header({ status, deviceName }) {
  const getStatusColor = () => {
    switch (status) {
      case 'Connected':
        return '#10b981'; // Green
      case 'Scanning':
      case 'Connecting':
        return '#f59e0b'; // Amber
      case 'Error':
        return '#ef4444'; // Red
      default:
        return '#64748b'; // Slate gray
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bluetooth LE Grade Predictor</Text>
      <Text style={styles.subtitle}>Classroom Device Connection App</Text>

      {/* Status Badge */}
      <View style={styles.statusRow}>
        <View style={[styles.statusDot, { backgroundColor: getStatusColor() }]} />
        <Text style={styles.statusText}>
          Status: <Text style={{ color: getStatusColor(), fontWeight: 'bold' }}>{status}</Text>
          {deviceName ? ` (${deviceName})` : ''}
        </Text>
      </View>

      {/* UUID Information Cards */}
      <View style={styles.uuidContainer}>
        <View style={styles.uuidCard}>
          <Text style={styles.uuidLabel}>SERVICE UUID</Text>
          <Text style={styles.uuidValue}>{SERVICE_UUID}</Text>
        </View>

        <View style={styles.uuidCard}>
          <Text style={styles.uuidLabel}>CHARACTERISTIC UUID</Text>
          <Text style={styles.uuidValue}>{CHAR_UUID}</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
    color: '#38bdf8',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 13,
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: 12,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0f172a',
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 20,
    alignSelf: 'center',
    marginBottom: 14,
  },
  statusDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 8,
  },
  statusText: {
    color: '#f8fafc',
    fontSize: 14,
  },
  uuidContainer: {
    gap: 8,
  },
  uuidCard: {
    backgroundColor: '#0f172a',
    padding: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#38bdf8',
  },
  uuidLabel: {
    fontSize: 10,
    color: '#64748b',
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  uuidValue: {
    fontSize: 11,
    color: '#e2e8f0',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    marginTop: 2,
  },
});
