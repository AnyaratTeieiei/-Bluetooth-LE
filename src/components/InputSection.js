import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';

export default function InputSection({
  yourName,
  setYourName,
  buddyName,
  setBuddyName,
  teacherDeviceName,
  setTeacherDeviceName,
}) {
  return (
    <View style={styles.container}>
      <Text style={styles.sectionHeader}>STUDENT & DEVICE INFORMATION</Text>

      {/* Teacher's BLE Device Name */}
      <View style={styles.inputGroup}>
        <Text style={[styles.label, { color: '#38bdf8' }]}>
          📡 Teacher's BLE Device Name (ชื่ออุปกรณ์ที่สแกนเจอใน Bluetooth)
        </Text>
        <TextInput
          style={[styles.input, { borderColor: '#0284c7' }]}
          placeholder="e.g. ESP32-Classroom, BLE_GRADE, etc."
          placeholderTextColor="#64748b"
          value={teacherDeviceName}
          onChangeText={setTeacherDeviceName}
        />
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Your Name & Student ID</Text>
        <TextInput
          style={styles.input}
          placeholder="e.g. NongKook (65012345)"
          placeholderTextColor="#64748b"
          value={yourName}
          onChangeText={setYourName}
        />
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Buddy's Name & Student ID</Text>
        <TextInput
          style={styles.input}
          placeholder="e.g. Alex (65054321)"
          placeholderTextColor="#64748b"
          value={buddyName}
          onChangeText={setBuddyName}
        />
      </View>

      <Text style={styles.previewText}>
        Payload Preview: <Text style={styles.previewHighlight}>"{yourName.trim() || 'Name'} & {buddyName.trim() || 'Buddy'}"</Text>
      </Text>
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
  sectionHeader: {
    fontSize: 12,
    fontWeight: '700',
    color: '#818cf8',
    letterSpacing: 1,
    marginBottom: 12,
  },
  inputGroup: {
    marginBottom: 12,
  },
  label: {
    fontSize: 13,
    color: '#cbd5e1',
    marginBottom: 6,
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#475569',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    color: '#f8fafc',
    fontSize: 14,
  },
  previewText: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 4,
    fontStyle: 'italic',
  },
  previewHighlight: {
    color: '#38bdf8',
    fontWeight: 'bold',
    fontStyle: 'normal',
  },
});
