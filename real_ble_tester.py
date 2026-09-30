import asyncio
import base64
import sys
from bleak import BleakScanner, BleakClient

SERVICE_UUID = "aee04821-1973-4e1f-a590-e84b10d580e7"
CHAR_UUID = "cde07b1a-889b-44b7-a99f-c888dddac729"

print("=" * 65)
print("     REAL BLUETOOTH LE TESTER (USING PC BLUETOOTH HARDWARE)")
print("=" * 65)

async def scan_and_test():
    print(f"\n[1] Scanning for devices using real PC Bluetooth adapter...")
    print(f"    Target Service UUID: {SERVICE_UUID}")
    
    discovered = await BleakScanner.discover(timeout=5.0, return_adv=True)
    
    target_device = None
    devices_list = []
    
    for d, adv in discovered.values():
        name = d.name or adv.local_name or "Unnamed"
        uuids = [u.lower() for u in adv.service_uuids]
        devices_list.append((d, name, adv.rssi))
        if SERVICE_UUID.lower() in uuids:
            target_device = d
            break

    if not target_device and devices_list:
        print("\nCould not find device broadcasting the exact Service UUID automatically.")
        print("Discovered real Bluetooth devices nearby:")
        for idx, (d, name, rssi) in enumerate(devices_list[:15]):
            print(f"  [{idx + 1}] {name} ({d.address}) | RSSI: {rssi} dBm")
        return devices_list

    if target_device:
        print(f"\nFound teacher device: {target_device.name} ({target_device.address})")

asyncio.run(scan_and_test())
