import asyncio
import uuid
import sys
import winrt.windows.devices.bluetooth.genericattributeprofile as gatt
import winrt.windows.storage.streams as streams

SERVICE_UUID = uuid.UUID('aee04821-1973-4e1f-a590-e84b10d580e7')
CHAR_UUID = uuid.UUID('cde07b1a-889b-44b7-a99f-c888dddac729')

print("=" * 65)
print("     ANYARAT BLUETOOTH LE SERVER & ADVERTISER")
print("=" * 65)

async def run_server():
    print(f"Initializing GATT Service with UUID: {SERVICE_UUID} ...")
    res = await gatt.GattServiceProvider.create_async(SERVICE_UUID)
    if res.error != 0:
        print(f"Error creating service provider: {res.error}")
        return

    provider = res.service_provider

    char_params = gatt.GattLocalCharacteristicParameters()
    char_params.characteristic_properties = (
        gatt.GattCharacteristicProperties.READ |
        gatt.GattCharacteristicProperties.WRITE |
        gatt.GattCharacteristicProperties.WRITE_WITHOUT_RESPONSE
    )
    char_params.read_protection_level = gatt.GattProtectionLevel.PLAIN
    char_params.write_protection_level = gatt.GattProtectionLevel.PLAIN

    char_res = await provider.service.create_characteristic_async(CHAR_UUID, char_params)
    if char_res.error != 0:
        print(f"Error creating characteristic: {char_res.error}")
        return

    char = char_res.characteristic
    print(f"Characteristic created with UUID: {CHAR_UUID}")

    provider.start_advertising()
    print("\n" + "*" * 60)
    print(" >>> BROADCASTING LIVE BLE GATT SERVER IN AIR <<<")
    print(" Device Name broadcasted: Check your PC Bluetooth Name")
    print(" Press Ctrl + C to stop broadcasting.")
    print("*" * 60 + "\n")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        provider.stop_advertising()
        print("\nStopped advertising.")

if __name__ == "__main__":
    asyncio.run(run_server())
