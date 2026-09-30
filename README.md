# Bluetooth LE Grade Predictor & Professor Transmission System

A comprehensive, multi-platform Bluetooth Low Energy (BLE) application designed for native hardware communication, classroom assignments, and direct transmission with the Professor's BLE device. Built with strict direct hardware Bluetooth operation (no third-party apps required like nRF Connect) and a 100% English interface.

---

## 📌 Configured Target BLE Specifications

- **Target Service UUID**: `aee04821-1973-4e1f-a590-e84b10d580e7`
- **Target Characteristic UUID**: `cde07b1a-889b-44b7-a99f-c888dddac729`
- **Characteristic Permissions**: `READ`, `WRITE`, `WRITE_WITHOUT_RESPONSE`, `NOTIFY`

---

## 🌟 Included Platforms & Tools

This repository contains 4 specialized platforms designed for testing, evaluating, and classroom presentation:

### 1. 🌐 Web Bluetooth Dashboard (Recommended)
- **Path**: `web/index.html` (Served via `run_web.py`)
- **URL**: `http://localhost:3000`
- **Features**:
  - **🎓 Professor Interface**: Dedicated view for connecting to the Professor's device, transmitting student data, and receiving the predicted grade in real-time.
  - **⚡ 1-Click Complete Flow**: Automated execution of Connect ➔ Read Initial ➔ Write Names ➔ Read Return Grade.
  - **📋 Assignment 3-Step Workflow**: Individual Step 1, Step 2, and Step 3 controls with live Base64 and Hexadecimal byte decoding.
  - **📡 Server Status**: Visual telemetry of the active GATT peripheral.
  - **🔧 Live Data Encoder**: Real-time UTF-8 string to Base64 and Hexadecimal converter.
- **Quick Launch**: Double-click `open_web_app.bat` or run:
  ```bash
  python run_web.py
  ```

---

### 2. 🖥️ Python Native Desktop BLE App
- **Script**: `ble_desktop_app.py`
- **Engine**: Python 3 + `bleak` + `tkinter`
- **Features**:
  - Direct scanning using your laptop's physical Bluetooth radio.
  - Dropdown device selector with auto-selection of classroom BLE devices.
  - Interactive Step 1, Step 2, and Step 3 buttons.
  - Auto-run sequence with complete GATT activity log.
- **Quick Launch**: Double-click `start_desktop_app.bat` or run:
  ```bash
  python ble_desktop_app.py
  ```

---

### 3. 📡 Native Windows GATT Server (Peripheral Mode)
- **Script**: `anyarat_ble_server.py`
- **Engine**: Windows WinRT API (`winrt.windows.devices.bluetooth.genericattributeprofile`)
- **Features**:
  - Broadcasts directly in the air as **`AnyaratBluetooth`** (`LAPTOP-00P88UUF`).
  - Configured with `is_discoverable = True` and `is_connectable = True`.
  - Automatically handles inbound `READ` and `WRITE` requests from the Professor or classmates.
  - Computes `GRADE: A (4.00) | SCORE: 98` dynamically when student payloads are received.
- **Quick Launch**: Double-click `start_server_receive.bat` or run:
  ```bash
  python anyarat_ble_server.py
  ```

---

### 4. 📱 Mobile Application (React Native / Expo)
- **Framework**: Expo SDK 57, React Native 0.86, React 19
- **BLE Library**: `react-native-ble-plx`
- **How to Run**:
  ```bash
  npm install
  npx expo start
  ```

---

## 📋 Assignment 3-Step Workflow Explanation

| Step | Action | Description | Expected Output |
| :--- | :--- | :--- | :--- |
| **STEP 1** | **Read Initial Value** | Read the characteristic before writing data. | Returns initial status: `"WAITING_FOR_DATA"` (Base64: `V0FJVElOR19GT1JfREFUQQ==`) |
| **STEP 2** | **Write Student Names** | Write student name & buddy name into the characteristic. | Writes payload: `"Anyarat (65012345) & Buddy (65054321)"` (Encoded in UTF-8 bytes) |
| **STEP 3** | **Read Predicted Grade** | Read characteristic again to obtain prediction result. | Returns predicted grade: `"GRADE: A (4.00) \| SCORE: 98 \| <Payload>"` |

---

## 🎓 How to Use for Professor Evaluation

1. Launch the Web Dashboard by running `open_web_app.bat` or opening `http://localhost:3000`.
2. On the **Professor Interface** tab:
   - Click **`Connect to Professor's Device`** and select the Professor's Bluetooth beacon/device.
   - Enter your Student Name and Buddy Name.
   - Click **`🚀 Send Data to Professor's Device`** (Transmits data via Write).
   - Click **`🔄 Read Response from Professor Now`** (or let real-time BLE notifications capture the return grade).
   - Alternatively, click **`⚡ 1-Click Auto: Send & Receive Grade`** to execute the entire cycle seamlessly!

---

## 📁 Repository Directory Structure

```
.
├── web/
│   └── index.html               # Web Bluetooth Dashboard (Professor Interface & 3-Step Workflow)
├── anyarat_ble_server.py        # Native Windows GATT Server (AnyaratBluetooth)
├── ble_desktop_app.py           # Native PC Desktop BLE GUI Application (Bleak)
├── run_web.py                   # Lightweight Local Web Server
├── open_web_app.bat             # 1-Click launcher for Web Dashboard
├── start_desktop_app.bat        # 1-Click launcher for Desktop GUI App
├── start_server_receive.bat     # 1-Click launcher for GATT Server
├── App.js                       # React Native Root Component
├── src/
│   ├── components/              # Header, StepCard, InputSection, LogConsole
│   ├── services/bleService.js   # Mobile BLE PLX service
│   └── utils/base64Utils.js     # Base64 and Hex byte encoders
├── package.json                 # Node dependencies
└── README.md                    # Project documentation
```

---

## 📄 License
This project is developed for educational purposes in Bluetooth Low Energy (BLE) systems engineering.
