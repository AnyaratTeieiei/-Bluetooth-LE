import { encode as btoa, decode as atob } from 'base-64';

/**
 * Encodes a standard UTF-8 string to a Base64 string for react-native-ble-plx write operations.
 * @param {string} str - Plain text string e.g. "John Doe & Jane Smith"
 * @returns {string} Base64 encoded string
 */
export function stringToBase64(str) {
  try {
    // Standard UTF-8 to Base64
    const utf8Bytes = encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (match, p1) => {
      return String.fromCharCode('0x' + p1);
    });
    return btoa(utf8Bytes);
  } catch (error) {
    console.error('stringToBase64 error:', error);
    return btoa(str);
  }
}

/**
 * Decodes a Base64 string received from react-native-ble-plx read operations to plain UTF-8 text.
 * @param {string} base64Str - Base64 string received from BLE read
 * @returns {string} Plain text UTF-8 string
 */
export function base64ToString(base64Str) {
  if (!base64Str) return '';
  try {
    const rawBinary = atob(base64Str);
    const utf8Str = decodeURIComponent(
      Array.from(rawBinary)
        .map(char => '%' + ('00' + char.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return utf8Str;
  } catch (error) {
    console.error('base64ToString decoding fallback:', error);
    try {
      return atob(base64Str);
    } catch (e) {
      return base64Str;
    }
  }
}

/**
 * Converts a Base64 string to a human-readable Hex string representation (e.g. "0x41 0x42 0x43").
 * @param {string} base64Str - Base64 string
 * @returns {string} Space-separated hex string
 */
export function base64ToHex(base64Str) {
  if (!base64Str) return 'N/A';
  try {
    const rawBinary = atob(base64Str);
    const hexArray = [];
    for (let i = 0; i < rawBinary.length; i++) {
      const hex = rawBinary.charCodeAt(i).toString(16).padStart(2, '0').toUpperCase();
      hexArray.push(`0x${hex}`);
    }
    return hexArray.join(' ');
  } catch (error) {
    return 'Invalid Hex';
  }
}
