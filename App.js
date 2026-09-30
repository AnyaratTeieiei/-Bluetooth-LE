import React, { useState, useEffect } from 'react';
import { StyleSheet, SafeAreaView, ScrollView, View, Alert, StatusBar } from 'react-native';
import Header from './src/components/Header';
import InputSection from './src/components/InputSection';
import StepCard from './src/components/StepCard';
import LogConsole from './src/components/LogConsole';
import { bleService } from './src/services/bleService';

export default function App() {
  const [status, setStatus] = useState('Disconnected');
  const [deviceName, setDeviceName] = useState('');
  const [teacherDeviceName, setTeacherDeviceName] = useState('ESP32-Classroom-BLE');
  const [yourName, setYourName] = useState('Student Name');
  const [buddyName, setBuddyName] = useState('Buddy Name');
  const [isLoading, setIsLoading] = useState(false);

  const [step1Result, setStep1Result] = useState(null);
  const [step2Result, setStep2Result] = useState(null);
  const [step3Result, setStep3Result] = useState(null);
  const [logs, setLogs] = useState([]);

  const addLog = (message, isError = false) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs((prevLogs) => [{ timestamp, message, isError }, ...prevLogs]);
  };

  useEffect(() => {
    addLog('App initialized. Ready to connect to classroom BLE device.');
    return () => {
      bleService.disconnect();
    };
  }, []);

  // Handle Scanning & Connecting
  const handleConnectPress = async () => {
    if (status === 'Connected') {
      addLog('Disconnecting from BLE device...');
      await bleService.disconnect();
      setStatus('Disconnected');
      setDeviceName('');
      addLog('Disconnected successfully.');
      return;
    }

    setIsLoading(true);
    setStatus('Scanning');
    addLog('Scanning for BLE devices matching target Service UUID...');

    let targetFound = false;
    bleService.setTargetDeviceName(teacherDeviceName);

    bleService.scanForDevices(
      async (device) => {
        if (!targetFound) {
          targetFound = true;
          bleService.stopScan();
          const devName = device.name || device.localName || teacherDeviceName || device.id;
          setDeviceName(devName);
          setTeacherDeviceName(devName);
          setStatus('Connecting');
          addLog(`Device discovered: ${devName}. Connecting...`);

          try {
            await bleService.connectToDevice(device);
            setStatus('Connected');
            addLog(`Successfully connected & discovered services for ${devName}!`);
          } catch (err) {
            setStatus('Error');
            addLog(`Connection failed: ${err.message}`, true);
          } finally {
            setIsLoading(false);
          }
        }
      },
      (errorMsg) => {
        setStatus('Error');
        addLog(`Scan Error: ${errorMsg}`, true);
        setIsLoading(false);
      }
    );

    // Timeout scan after 10 seconds
    setTimeout(() => {
      if (!targetFound && status === 'Scanning') {
        bleService.stopScan();
        setStatus('Disconnected');
        setIsLoading(false);
        addLog('Scan timeout: Device not found. Ensure Bluetooth is ON & device is in range.', true);
      }
    }, 10000);
  };

  // Step 1: Read Characteristic Value
  const handleStep1 = async () => {
    setIsLoading(true);
    addLog('STEP 1: Reading Characteristic value...');
    try {
      const result = await bleService.readCharacteristic();
      setStep1Result(result);
      addLog(`STEP 1 Success -> Text: "${result.textValue}", Hex: ${result.hexValue}`);
      return result;
    } catch (err) {
      addLog(`STEP 1 Error: ${err.message}`, true);
      Alert.alert('Step 1 Failed', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Step 2: Write Name & Buddy
  const handleStep2 = async () => {
    if (!yourName.trim() || !buddyName.trim()) {
      Alert.alert('Missing Names', 'Please fill in both your name and your buddy\'s name.');
      return;
    }

    setIsLoading(true);
    addLog(`STEP 2: Writing values -> "${yourName.trim()} & ${buddyName.trim()}"`);
    try {
      const result = await bleService.writeCharacteristic(yourName, buddyName);
      setStep2Result(result);
      addLog(`STEP 2 Success -> Written Base64: ${result.writtenBase64}, Hex: ${result.writtenHex}`);
      return result;
    } catch (err) {
      addLog(`STEP 2 Error: ${err.message}`, true);
      Alert.alert('Step 2 Failed', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Step 3: Read Characteristic Value Again (Grade Prediction)
  const handleStep3 = async () => {
    setIsLoading(true);
    addLog('STEP 3: Reading Characteristic value again (Predicted Grade)...');
    try {
      const result = await bleService.readCharacteristic();
      setStep3Result(result);
      addLog(`STEP 3 Success -> PREDICTED GRADE: "${result.textValue}", Hex: ${result.hexValue}`);
      return result;
    } catch (err) {
      addLog(`STEP 3 Error: ${err.message}`, true);
      Alert.alert('Step 3 Failed', err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Auto Run Steps 1-3 sequentially
  const handleAutoRun = async () => {
    addLog('--- STARTING AUTOMATED WORKFLOW (STEPS 1 to 3) ---');
    const step1 = await handleStep1();
    if (!step1) return;

    await new Promise((resolve) => setTimeout(resolve, 600));

    const step2 = await handleStep2();
    if (!step2) return;

    await new Promise((resolve) => setTimeout(resolve, 600));

    await handleStep3();
    addLog('--- COMPLETED AUTOMATED WORKFLOW ---');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0f172a" />
      <ScrollView contentContainerStyle={styles.container}>
        <Header status={status} deviceName={deviceName} />

        <InputSection
          yourName={yourName}
          setYourName={setYourName}
          buddyName={buddyName}
          setBuddyName={setBuddyName}
          teacherDeviceName={teacherDeviceName}
          setTeacherDeviceName={setTeacherDeviceName}
        />

        <StepCard
          isConnected={status === 'Connected'}
          isLoading={isLoading}
          onConnectPress={handleConnectPress}
          onStep1Press={handleStep1}
          onStep2Press={handleStep2}
          onStep3Press={handleStep3}
          onAutoRunPress={handleAutoRun}
          step1Result={step1Result}
          step2Result={step2Result}
          step3Result={step3Result}
        />

        <LogConsole logs={logs} onClear={() => setLogs([])} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  container: {
    padding: 16,
    backgroundColor: '#0f172a',
  },
});
