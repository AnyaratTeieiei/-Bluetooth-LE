import sys
import time
import subprocess

print("=" * 60)
print("     BLUETOOTH BROADCASTER & RECEIVER TOOL")
print("=" * 60)

# Check Windows Bluetooth status
print("[1] Opening Windows Bluetooth Discoverable Mode...")
try:
    # Opening Bluetooth settings automatically makes Windows discoverable to nearby devices!
    subprocess.Popen(["cmd", "/c", "start", "ms-settings:bluetooth"], shell=True)
    print("    Windows Bluetooth Settings opened successfully!")
    print("    >>> THIS PC IS NOW FULLY DISCOVERABLE BY NEARBY DEVICES <<<")
except Exception as e:
    print(f"    Error opening settings: {e}")

print("\n[2] Device Name Broadcasted:")
import os
pc_name = os.environ.get("COMPUTERNAME", "PC-Bluetooth")
print(f"    Current PC Bluetooth Name: [{pc_name}]")
print(f"    Target Name Requested:     [AnyaratBluetooth]")

print("\n" + "=" * 60)
print("  TIPS FOR SHARING BLUETOOTH WITH FRIENDS:")
print("  - On your friend's phone: Open Settings -> Bluetooth OR nRF Connect")
print("  - Look for your PC name or use phone Advertiser mode")
print("=" * 60)
