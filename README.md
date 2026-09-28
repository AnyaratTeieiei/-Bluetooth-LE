# Bluetooth LE Grade Predictor App (React Native)

A React Native mobile application built with Expo and `react-native-ble-plx` for connecting to the classroom Bluetooth LE device, executing the 3 required reading/writing assignment steps, and predicting your grade.

---

## 📌 Configured Target UUIDs

- **Service UUID**: `aee04821-1973-4e1f-a590-e84b10d580e7`
- **Characteristic UUID**: `cde07b1a-889b-44b7-a99f-c888dddac729`

---

## 🚀 How to Run the React Native App

### Prerequisites
1. Install [Node.js](https://nodejs.org/) (version 18 or newer).
2. Install Expo CLI globally or use `npx expo`.
3. Install **Expo Go** app on your iOS device (App Store) or Android device (Google Play Store).

### Step 1: Install Dependencies
Open your terminal inside this project folder (`c:\Users\Nongkookeiei\Desktop\Bluetooth LE`) and run:
```bash
npm install
```

### Step 2: Start the Expo Development Server
Run:
```bash
npx expo start
```
or
```bash
npm start
```

### Step 3: Open App on Mobile Device
- **Android**: Scan the QR code displayed in the terminal using the Expo Go app.
- **iOS**: Scan the QR code using your iOS Camera app to launch Expo Go.

> ⚠️ **Note for physical mobile BLE testing**:
> For full Bluetooth LE hardware access on iOS/Android, ensure Bluetooth and Location services are turned **ON** on your smartphone.

---

## 📱 How to Use for Classroom Submission

1. **Open the App**: Launch the app on your mobile device.
2. **Enter Names**: Enter **Your Name** and **Buddy's Name** in the input section.
3. **Connect**: Tap **"1. Connect BLE Device"**. The app will scan and connect to the classroom BLE device with Service UUID `aee04821-1973-4e1f-a590-e84b10d580e7`.
4. **Step 1 (Read Initial)**: Tap **"Read Initial"** to capture the initial characteristic value before write.
5. **Step 2 (Write Names)**: Tap **"Write Values"** to send your name and buddy's name to the device.
6. **Step 3 (Read Grade)**: Tap **"Read Grade"** to read the updated characteristic value and reveal your predicted grade!
7. **Take Screenshots**: Capture your mobile screen showing:
   - Status badge showing **Connected**
   - Step 1 Result
   - Step 2 Result
   - Step 3 Predicted Grade Badge
   - Real-Time Log Console
8. **Submit**: Upload the captured screenshots to Google Classroom.

---

## 📁 Project Structure

```
Bluetooth LE/
├── App.js                         # Main application component & state manager
├── app.json                       # Expo configuration & iOS/Android BLE permissions
├── package.json                   # Dependencies
├── babel.config.js                # Babel setup
└── src/
    ├── services/
    │   └── bleService.js          # React Native BLE PLX manager (Scan, Connect, Read, Write)
    ├── components/
    │   ├── Header.js              # Connection status & UUID cards
    │   ├── InputSection.js        # Name input fields & payload preview
    │   ├── StepCard.js            # Interactive step buttons & result displays
    │   └── LogConsole.js          # Real-time console log
    └── utils/
        └── base64Utils.js         # Base64 <-> UTF-8 text and Hex byte converters
```
