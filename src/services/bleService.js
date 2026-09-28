import { BleManager } from 'react-native-ble-plx';
import { Platform, PermissionsAndroid } from 'react-native';
import { stringToBase64, base64ToString, base64ToHex } from '../utils/base64Utils';

export const SERVICE_UUID = 'aee04821-1973-4e1f-a590-e84b10d580e7';
export const CHAR_UUID = 'cde07b1a-889b-44b7-a99f-c888dddac729';

class BleService {
  constructor() {
    this.manager = new BleManager();
    this.connectedDevice = null;
  }

  /**
   * Request Bluetooth permissions for Android 12+ and Android 11-
   */
  async requestPermissions() {
    if (Platform.OS === 'android') {
      if (Platform.Version >= 31) {
        const result = await PermissionsAndroid.requestMultiple([
          PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
          PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        ]);
        return (
          result['android.permission.BLUETOOTH_SCAN'] === PermissionsAndroid.RESULTS.GRANTED &&
          result['android.permission.BLUETOOTH_CONNECT'] === PermissionsAndroid.RESULTS.GRANTED
        );
      } else {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION
        );
        return granted === PermissionsAndroid.RESULTS.GRANTED;
      }
    }
    return true; // iOS permissions handled by Info.plist prompt
  }

  /**
   * Scan for BLE devices advertising the target Service UUID
   */
  async scanForDevices(onDeviceFound, onError) {
    const hasPermission = await this.requestPermissions();
    if (!hasPermission) {
      onError('Location/Bluetooth permission denied.');
      return;
    }

    const state = await this.manager.state();
    if (state !== 'PoweredOn') {
      onError(`Bluetooth is not powered on. Current state: ${state}`);
      return;
    }

    this.manager.startDeviceScan([SERVICE_UUID], null, (error, device) => {
      if (error) {
        // Fallback scan with null filters if specific UUID scan fails or device doesn't advertise service UUID in main payload
        this.manager.startDeviceScan(null, null, (err, dev) => {
          if (err) {
            onError(err.message);
            return;
          }
          if (dev && (dev.name || dev.localName)) {
            onDeviceFound(dev);
          }
        });
        return;
      }

      if (device) {
        onDeviceFound(device);
      }
    });
  }

  /**
   * Stop active scan
   */
  stopScan() {
    this.manager.stopDeviceScan();
  }

  /**
   * Connect to a discovered BLE Device & discover services & characteristics
   */
  async connectToDevice(device) {
    this.stopScan();
    
    // Connect
    const connectedDev = await device.connect();
    this.connectedDevice = connectedDev;

    // Discover Services and Characteristics
    await connectedDev.discoverAllServicesAndCharacteristics();
    return connectedDev;
  }

  /**
   * Disconnect from current device
   */
  async disconnect() {
    if (this.connectedDevice) {
      try {
        await this.connectedDevice.cancelConnection();
      } catch (err) {
        console.warn('Disconnect warning:', err);
      }
      this.connectedDevice = null;
    }
  }

  /**
   * Step 1 & 3: Read Characteristic Value
   */
  async readCharacteristic() {
    if (!this.connectedDevice) {
      throw new Error('No device connected. Please connect first.');
    }

    const characteristic = await this.connectedDevice.readCharacteristicForService(
      SERVICE_UUID,
      CHAR_UUID
    );

    const base64Value = characteristic.value;
    const textValue = base64ToString(base64Value);
    const hexValue = base64ToHex(base64Value);

    return {
      rawBase64: base64Value,
      textValue: textValue,
      hexValue: hexValue,
    };
  }

  /**
   * Step 2: Write Name & Buddy Value to Characteristic
   */
  async writeCharacteristic(yourName, buddyName) {
    if (!this.connectedDevice) {
      throw new Error('No device connected. Please connect first.');
    }

    const payloadString = `${yourName.trim()} & ${buddyName.trim()}`;
    const base64Value = stringToBase64(payloadString);

    let charResult;
    try {
      charResult = await this.connectedDevice.writeCharacteristicWithResponseForService(
        SERVICE_UUID,
        CHAR_UUID,
        base64Value
      );
    } catch (e) {
      // Fallback to write without response if writeWithResponse is not supported by target firmware
      charResult = await this.connectedDevice.writeCharacteristicWithoutResponseForService(
        SERVICE_UUID,
        CHAR_UUID,
        base64Value
      );
    }

    return {
      writtenString: payloadString,
      writtenBase64: base64Value,
      writtenHex: base64ToHex(base64Value),
      result: charResult,
    };
  }
}

export const bleService = new BleService();
