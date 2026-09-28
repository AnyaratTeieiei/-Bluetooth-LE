import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator, Platform } from 'react-native';

export default function StepCard({
  isConnected,
  isLoading,
  onConnectPress,
  onStep1Press,
  onStep2Press,
  onStep3Press,
  onAutoRunPress,
  step1Result,
  step2Result,
  step3Result,
}) {
  return (
    <View style={styles.container}>
      <Text style={styles.sectionHeader}>ASSIGNMENT WORKFLOW STEPS</Text>

      {/* Main Connection & Auto Flow Buttons */}
      <View style={styles.topBtnRow}>
        <TouchableOpacity
          style={[styles.mainBtn, isConnected ? styles.connectedBtn : styles.connectBtn]}
          onPress={onConnectPress}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#ffffff" size="small" />
          ) : (
            <Text style={styles.mainBtnText}>
              {isConnected ? 'Disconnect Device' : '1. Connect BLE Device'}
            </Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.mainBtn, styles.autoRunBtn, !isConnected && styles.disabledBtn]}
          onPress={onAutoRunPress}
          disabled={!isConnected || isLoading}
        >
          <Text style={styles.mainBtnText}>⚡ Run Steps 1-3 Auto</Text>
        </TouchableOpacity>
      </View>

      {/* STEP 1: READ CHARACTERISTIC INITIAL VALUE */}
      <View style={styles.stepBox}>
        <View style={styles.stepHeaderRow}>
          <Text style={styles.stepTitle}>STEP 1: Read Characteristic Value</Text>
          <TouchableOpacity
            style={[styles.stepActionBtn, !isConnected && styles.disabledBtn]}
            onPress={onStep1Press}
            disabled={!isConnected || isLoading}
          >
            <Text style={styles.stepActionBtnText}>Read Initial</Text>
          </TouchableOpacity>
        </View>

        {step1Result ? (
          <View style={styles.resultBox}>
            <Text style={styles.resultLabel}>Decoded Text:</Text>
            <Text style={styles.resultValueText}>"{step1Result.textValue || '<Empty>'}"</Text>
            
            <View style={styles.subDetailRow}>
              <Text style={styles.detailLabel}>Hex Bytes: </Text>
              <Text style={styles.detailValue}>{step1Result.hexValue}</Text>
            </View>
            <View style={styles.subDetailRow}>
              <Text style={styles.detailLabel}>Base64: </Text>
              <Text style={styles.detailValue}>{step1Result.rawBase64}</Text>
            </View>
          </View>
        ) : (
          <Text style={styles.placeholderText}>Tap 'Read Initial' to perform Step 1.</Text>
        )}
      </View>

      {/* STEP 2: WRITE NAME & BUDDY */}
      <View style={styles.stepBox}>
        <View style={styles.stepHeaderRow}>
          <Text style={styles.stepTitle}>STEP 2: Write Name & Buddy Value</Text>
          <TouchableOpacity
            style={[styles.stepActionBtn, styles.step2Btn, !isConnected && styles.disabledBtn]}
            onPress={onStep2Press}
            disabled={!isConnected || isLoading}
          >
            <Text style={styles.stepActionBtnText}>Write Values</Text>
          </TouchableOpacity>
        </View>

        {step2Result ? (
          <View style={styles.resultBox}>
            <Text style={styles.resultLabel}>Written String Payload:</Text>
            <Text style={[styles.resultValueText, { color: '#38bdf8' }]}>"{step2Result.writtenString}"</Text>
            
            <View style={styles.subDetailRow}>
              <Text style={styles.detailLabel}>Base64 Payload: </Text>
              <Text style={styles.detailValue}>{step2Result.writtenBase64}</Text>
            </View>
            <View style={styles.subDetailRow}>
              <Text style={styles.detailLabel}>Written Hex: </Text>
              <Text style={styles.detailValue}>{step2Result.writtenHex}</Text>
            </View>
          </View>
        ) : (
          <Text style={styles.placeholderText}>Tap 'Write Values' to perform Step 2.</Text>
        )}
      </View>

      {/* STEP 3: READ AGAIN - GRADE PREDICTION RESULT */}
      <View style={styles.stepBox}>
        <View style={styles.stepHeaderRow}>
          <Text style={styles.stepTitle}>STEP 3: Read Grade Prediction</Text>
          <TouchableOpacity
            style={[styles.stepActionBtn, styles.step3Btn, !isConnected && styles.disabledBtn]}
            onPress={onStep3Press}
            disabled={!isConnected || isLoading}
          >
            <Text style={styles.stepActionBtnText}>Read Grade</Text>
          </TouchableOpacity>
        </View>

        {step3Result ? (
          <View style={[styles.resultBox, styles.gradeHighlightBox]}>
            <Text style={styles.gradeBadgeHeader}>🎓 PREDICTED GRADE RESULT</Text>
            <Text style={styles.gradeText}>"{step3Result.textValue || 'Grade Received'}"</Text>

            <View style={styles.subDetailRow}>
              <Text style={styles.detailLabel}>Hex Bytes: </Text>
              <Text style={styles.detailValue}>{step3Result.hexValue}</Text>
            </View>
            <View style={styles.subDetailRow}>
              <Text style={styles.detailLabel}>Base64: </Text>
              <Text style={styles.detailValue}>{step3Result.rawBase64}</Text>
            </View>
          </View>
        ) : (
          <Text style={styles.placeholderText}>Tap 'Read Grade' to perform Step 3 and reveal your grade.</Text>
        )}
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
  sectionHeader: {
    fontSize: 12,
    fontWeight: '700',
    color: '#34d399',
    letterSpacing: 1,
    marginBottom: 12,
  },
  topBtnRow: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 16,
  },
  mainBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  connectBtn: {
    backgroundColor: '#2563eb',
  },
  connectedBtn: {
    backgroundColor: '#dc2626',
  },
  autoRunBtn: {
    backgroundColor: '#7c3aed',
  },
  disabledBtn: {
    opacity: 0.5,
  },
  mainBtnText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 13,
  },
  stepBox: {
    backgroundColor: '#0f172a',
    padding: 12,
    borderRadius: 8,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#1e293b',
  },
  stepHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  stepTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#f1f5f9',
    flex: 1,
  },
  stepActionBtn: {
    backgroundColor: '#0284c7',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  step2Btn: {
    backgroundColor: '#d97706',
  },
  step3Btn: {
    backgroundColor: '#059669',
  },
  stepActionBtnText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '700',
  },
  resultBox: {
    backgroundColor: '#182234',
    padding: 10,
    borderRadius: 6,
    marginTop: 6,
  },
  gradeHighlightBox: {
    backgroundColor: '#064e3b',
    borderColor: '#10b981',
    borderWidth: 1,
  },
  gradeBadgeHeader: {
    fontSize: 11,
    fontWeight: '800',
    color: '#34d399',
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  gradeText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fef08a',
    marginVertical: 4,
  },
  resultLabel: {
    fontSize: 11,
    color: '#94a3b8',
  },
  resultValueText: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#f8fafc',
    marginVertical: 4,
  },
  subDetailRow: {
    flexDirection: 'row',
    marginTop: 2,
  },
  detailLabel: {
    fontSize: 11,
    color: '#64748b',
  },
  detailValue: {
    fontSize: 11,
    color: '#cbd5e1',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  placeholderText: {
    fontSize: 12,
    color: '#64748b',
    fontStyle: 'italic',
  },
});
