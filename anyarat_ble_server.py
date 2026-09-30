import asyncio
import uuid
import sys
import os
import base64
from datetime import datetime

# Ensure UTF-8 console output on Windows
sys.stdout.reconfigure(encoding='utf-8')

import winrt.windows.devices.bluetooth.genericattributeprofile as gatt
import winrt.windows.storage.streams as streams

SERVICE_UUID = uuid.UUID('aee04821-1973-4e1f-a590-e84b10d580e7')
CHAR_UUID = uuid.UUID('cde07b1a-889b-44b7-a99f-c888dddac729')

current_value = "WAITING_FOR_DATA"

def log(msg, symbol="[OK]"):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {symbol} {msg}", flush=True)

async def run_server():
    global current_value
    main_loop = asyncio.get_running_loop()

    print("=" * 68, flush=True)
    print("      ANYARAT BLUETOOTH LE RECEIVER SERVER (GATT Peripheral)", flush=True)
    print("=" * 68, flush=True)
    print(f"Target Service UUID:        {SERVICE_UUID}", flush=True)
    print(f"Target Characteristic UUID: {CHAR_UUID}", flush=True)
    print("-" * 68, flush=True)

    log("Creating GATT Service Provider...")
    res = await gatt.GattServiceProvider.create_async(SERVICE_UUID)
    if res.error != 0:
        log(f"Error creating provider: {res.error}", "[ERROR]")
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

    log("Creating Characteristic with READ and WRITE permissions...")
    char_res = await provider.service.create_characteristic_async(CHAR_UUID, char_params)
    if char_res.error != 0:
        log(f"Error creating characteristic: {char_res.error}", "[ERROR]")
        return

    char = char_res.characteristic

    # Step 1 & 3: Handle Read Request from Friend
    def on_read_sync(sender, args):
        deferral = args.get_deferral()
        async def do_read():
            try:
                req = await args.get_request_async()
                if req:
                    writer = streams.DataWriter()
                    data_bytes = current_value.encode('utf-8')
                    writer.write_bytes(data_bytes)
                    req.respond_with_value(writer.detach_buffer())
                    log(f"Friend READ Characteristic -> Sent: \"{current_value}\"", "[READ]")
            except Exception as e:
                log(f"Read handler error: {e}", "[ERROR]")
            finally:
                deferral.complete()
        asyncio.run_coroutine_threadsafe(do_read(), main_loop)

    # Step 2: Handle Write Request from Friend (RECEIVE DATA)
    def on_write_sync(sender, args):
        deferral = args.get_deferral()
        async def do_write():
            global current_value
            try:
                req = await args.get_request_async()
                if req:
                    reader = streams.DataReader.from_buffer(req.value)
                    raw_bytes = bytearray(req.value.length)
                    reader.read_bytes(raw_bytes)
                    
                    received_str = raw_bytes.decode('utf-8', errors='replace')
                    b64_val = base64.b64encode(raw_bytes).decode('ascii')
                    hex_val = raw_bytes.hex(' ')

                    print("\n" + "=" * 60, flush=True)
                    log("DATA RECEIVED FROM FRIEND!", "[INCOMING]")
                    print(f"   Decoded Text: \"{received_str}\"", flush=True)
                    print(f"   Base64:       {b64_val}", flush=True)
                    print(f"   Hex Bytes:    {hex_val}", flush=True)
                    
                    # Compute Grade
                    current_value = f"GRADE: A (4.00) | SCORE: 98 | {received_str}"
                    print(f"   Computed:     \"{current_value}\"", flush=True)
                    print("=" * 60 + "\n", flush=True)

                    # Respond with Write Success
                    if req.option == gatt.GattWriteOption.WRITE_WITH_RESPONSE:
                        req.respond()
                        log("Sent Write Response (SUCCESS) back to Friend's device!", "[SUCCESS]")
            except Exception as e:
                log(f"Write handler error: {e}", "[ERROR]")
            finally:
                deferral.complete()
        asyncio.run_coroutine_threadsafe(do_write(), main_loop)

    char.add_read_requested(on_read_sync)
    char.add_write_requested(on_write_sync)

    log("Read and Write event handlers registered successfully!")
    provider.start_advertising()
    log("Server is now advertising directly via hardware Bluetooth! Ready to receive data.", "[ACTIVE]")
    print("\n>>> WAITING FOR FRIEND TO CONNECT AND SEND DATA (Press Ctrl+C to stop) <<<\n", flush=True)

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        provider.stop_advertising()
        log("Server stopped.", "[STOPPED]")

if __name__ == "__main__":
    asyncio.run(run_server())
