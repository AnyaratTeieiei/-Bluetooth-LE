import sys
import base64
import asyncio
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from bleak import BleakScanner, BleakClient

SERVICE_UUID = "aee04821-1973-4e1f-a590-e84b10d580e7"
CHAR_UUID = "cde07b1a-889b-44b7-a99f-c888dddac729"

class BleDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluetooth LE Grade Predictor - PC Native Bluetooth")
        self.root.geometry("860x950")
        self.root.configure(bg="#0f172a")

        self.client = None
        self.is_connected = False
        self.is_busy = False
        self.discovered_devices = []

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.thread.start()

        self._build_ui()
        self.add_log("PC Bluetooth Desktop App ready. Using native Windows Bluetooth hardware.")

    def _run_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_async(self, coro):
        asyncio.run_coroutine_threadsafe(coro, self.loop)

    def _build_ui(self):
        # Configure styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#0f172a", background="#1e293b", foreground="#f8fafc")

        # Scrollable canvas
        canvas = tk.Canvas(self.root, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#0f172a")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=840)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 1. Header Frame
        header = tk.Frame(self.scroll_frame, bg="#1e293b", bd=1, relief="solid", padx=18, pady=12)
        header.pack(fill="x", padx=16, pady=10)

        title = tk.Label(header, text="Bluetooth LE Grade Predictor", font=("Segoe UI", 16, "bold"), fg="#f8fafc", bg="#1e293b")
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="PC Hardware Edition — Running with Laptop's Real Bluetooth Antenna", font=("Segoe UI", 9), fg="#38bdf8", bg="#1e293b")
        subtitle.pack(anchor="w", pady=(0, 6))

        # Status row
        status_row = tk.Frame(header, bg="#1e293b")
        status_row.pack(fill="x", pady=4)

        self.status_dot = tk.Label(status_row, text="●", font=("Segoe UI", 14), fg="#64748b", bg="#1e293b")
        self.status_dot.pack(side="left", padx=(0, 6))

        self.status_label = tk.Label(status_row, text="Status: Disconnected", font=("Segoe UI", 11, "bold"), fg="#64748b", bg="#1e293b")
        self.status_label.pack(side="left")

        # UUID display
        uuid_frame = tk.Frame(header, bg="#0f172a", padx=10, pady=8, bd=1, relief="solid")
        uuid_frame.pack(fill="x", pady=(8, 0))

        u1 = tk.Label(uuid_frame, text=f"SERVICE UUID:  {SERVICE_UUID}", font=("Consolas", 9), fg="#38bdf8", bg="#0f172a")
        u1.pack(anchor="w")
        u2 = tk.Label(uuid_frame, text=f"CHAR UUID:     {CHAR_UUID}", font=("Consolas", 9), fg="#a78bfa", bg="#0f172a")
        u2.pack(anchor="w")

        # 2. Scanner & Connection Controls
        scan_frame = tk.Frame(self.scroll_frame, bg="#1e293b", bd=1, relief="solid", padx=18, pady=12)
        scan_frame.pack(fill="x", padx=16, pady=6)

        tk.Label(scan_frame, text="REAL BLUETOOTH HARDWARE SCANNER", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w", pady=(0, 6))

        scan_btn_row = tk.Frame(scan_frame, bg="#1e293b")
        scan_btn_row.pack(fill="x", pady=4)

        self.scan_btn = tk.Button(scan_btn_row, text="🔍 Scan Real Devices", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="#fff", activebackground="#0369a1", bd=0, padx=12, pady=6, cursor="hand2", command=self.on_scan)
        self.scan_btn.pack(side="left", padx=(0, 8))

        self.device_combo = ttk.Combobox(scan_btn_row, font=("Segoe UI", 9), state="readonly", width=42)
        self.device_combo.set("Click 'Scan Real Devices' to search...")
        self.device_combo.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.connect_btn = tk.Button(scan_btn_row, text="Connect Selected", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="#fff", activebackground="#059669", bd=0, padx=14, pady=6, cursor="hand2", command=self.on_connect_toggle)
        self.connect_btn.pack(side="left")

        # 3. Student Information Frame
        info_frame = tk.Frame(self.scroll_frame, bg="#1e293b", bd=1, relief="solid", padx=18, pady=12)
        info_frame.pack(fill="x", padx=16, pady=6)

        tk.Label(info_frame, text="STUDENT INFORMATION", font=("Segoe UI", 10, "bold"), fg="#818cf8", bg="#1e293b").pack(anchor="w", pady=(0, 8))

        tk.Label(info_frame, text="Your Name & Student ID:", font=("Segoe UI", 9, "bold"), fg="#cbd5e1", bg="#1e293b").pack(anchor="w")
        self.name_entry = tk.Entry(info_frame, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#fff", bd=1, relief="solid")
        self.name_entry.insert(0, "Anyarat (65012345)")
        self.name_entry.pack(fill="x", pady=(2, 6))
        self.name_entry.bind("<KeyRelease>", self._update_preview)

        tk.Label(info_frame, text="Buddy's Name & Student ID:", font=("Segoe UI", 9, "bold"), fg="#cbd5e1", bg="#1e293b").pack(anchor="w")
        self.buddy_entry = tk.Entry(info_frame, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#fff", bd=1, relief="solid")
        self.buddy_entry.insert(0, "Buddy Name (65054321)")
        self.buddy_entry.pack(fill="x", pady=(2, 6))
        self.buddy_entry.bind("<KeyRelease>", self._update_preview)

        self.preview_label = tk.Label(info_frame, text="", font=("Segoe UI", 9, "italic"), fg="#38bdf8", bg="#1e293b")
        self.preview_label.pack(anchor="w")
        self._update_preview()

        # 4. Action Steps Frame
        flow_frame = tk.Frame(self.scroll_frame, bg="#1e293b", bd=1, relief="solid", padx=18, pady=12)
        flow_frame.pack(fill="x", padx=16, pady=6)

        tk.Label(flow_frame, text="ASSIGNMENT WORKFLOW STEPS", font=("Segoe UI", 10, "bold"), fg="#34d399", bg="#1e293b").pack(anchor="w", pady=(0, 8))

        self.autorun_btn = tk.Button(flow_frame, text="⚡ Run Steps 1-3 Auto in Sequence", font=("Segoe UI", 10, "bold"), bg="#7c3aed", fg="#ffffff", activebackground="#6d28d9", bd=0, padx=16, pady=8, cursor="hand2", command=self.on_auto_run)
        self.autorun_btn.pack(anchor="w", pady=(0, 10))

        # Step 1 Box
        step1_box = tk.Frame(flow_frame, bg="#0f172a", bd=1, relief="solid", padx=12, pady=10)
        step1_box.pack(fill="x", pady=5)
        s1_head = tk.Frame(step1_box, bg="#0f172a")
        s1_head.pack(fill="x")
        tk.Label(s1_head, text="STEP 1: Read Characteristic Initial Value", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#0f172a").pack(side="left")
        self.s1_btn = tk.Button(s1_head, text="Read Initial", font=("Segoe UI", 9, "bold"), bg="#3b82f6", fg="#fff", bd=0, padx=12, pady=4, cursor="hand2", command=self.on_step1)
        self.s1_btn.pack(side="right")
        self.s1_res = tk.Label(step1_box, text="Click 'Read Initial' to perform Step 1.", font=("Consolas", 9), fg="#94a3b8", bg="#0f172a", justify="left")
        self.s1_res.pack(anchor="w", pady=(6, 0))

        # Step 2 Box
        step2_box = tk.Frame(flow_frame, bg="#0f172a", bd=1, relief="solid", padx=12, pady=10)
        step2_box.pack(fill="x", pady=5)
        s2_head = tk.Frame(step2_box, bg="#0f172a")
        s2_head.pack(fill="x")
        tk.Label(s2_head, text="STEP 2: Write Name & Buddy Value", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#0f172a").pack(side="left")
        self.s2_btn = tk.Button(s2_head, text="Write Values", font=("Segoe UI", 9, "bold"), bg="#10b981", fg="#fff", bd=0, padx=12, pady=4, cursor="hand2", command=self.on_step2)
        self.s2_btn.pack(side="right")
        self.s2_res = tk.Label(step2_box, text="Click 'Write Values' to perform Step 2.", font=("Consolas", 9), fg="#94a3b8", bg="#0f172a", justify="left")
        self.s2_res.pack(anchor="w", pady=(6, 0))

        # Step 3 Box
        step3_box = tk.Frame(flow_frame, bg="#0f172a", bd=1, relief="solid", padx=12, pady=10)
        step3_box.pack(fill="x", pady=5)
        s3_head = tk.Frame(step3_box, bg="#0f172a")
        s3_head.pack(fill="x")
        tk.Label(s3_head, text="STEP 3: Read Grade Prediction", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#0f172a").pack(side="left")
        self.s3_btn = tk.Button(s3_head, text="Read Grade", font=("Segoe UI", 9, "bold"), bg="#f59e0b", fg="#fff", bd=0, padx=12, pady=4, cursor="hand2", command=self.on_step3)
        self.s3_btn.pack(side="right")
        self.s3_res = tk.Label(step3_box, text="Click 'Read Grade' to perform Step 3 and reveal grade.", font=("Consolas", 9), fg="#94a3b8", bg="#0f172a", justify="left")
        self.s3_res.pack(anchor="w", pady=(6, 0))

        # 5. Log Console
        log_frame = tk.Frame(self.scroll_frame, bg="#1e293b", bd=1, relief="solid", padx=18, pady=10)
        log_frame.pack(fill="both", expand=True, padx=16, pady=8)

        l_head = tk.Frame(log_frame, bg="#1e293b")
        l_head.pack(fill="x", pady=(0, 6))
        tk.Label(l_head, text="REAL-TIME LOG CONSOLE", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#1e293b").pack(side="left")
        tk.Button(l_head, text="Clear Logs", font=("Segoe UI", 8), bg="#334155", fg="#e2e8f0", bd=0, padx=8, pady=2, command=self._clear_logs).pack(side="right")

        self.log_text = scrolledtext.ScrolledText(log_frame, height=9, bg="#090d16", fg="#e2e8f0", font=("Consolas", 9), insertbackground="#fff", bd=0)
        self.log_text.pack(fill="both", expand=True)

    def _update_preview(self, event=None):
        p1 = self.name_entry.get().strip() or "Name"
        p2 = self.buddy_entry.get().strip() or "Buddy"
        self.preview_label.config(text=f'Payload Preview: "{p1} & {p2}"')

    def add_log(self, msg, is_error=False):
        now = datetime.now().strftime("%H:%M:%S")
        prefix = "❌ " if is_error else "✓ "
        def _append():
            self.log_text.insert(tk.END, f"[{now}] {prefix}{msg}\n")
            self.log_text.see(tk.END)
        self.root.after(0, _append)

    def _clear_logs(self):
        self.log_text.delete("1.0", tk.END)

    def set_status(self, text, color):
        def _update():
            self.status_label.config(text=f"Status: {text}", fg=color)
            self.status_dot.config(fg=color)
        self.root.after(0, _update)

    # 1. Scanning
    def on_scan(self):
        if self.is_busy:
            return
        self.run_async(self._scan_async())

    async def _scan_async(self):
        self.is_busy = True
        self.set_status("Scanning...", "#f59e0b")
        self.add_log("Scanning with PC Bluetooth antenna (5 seconds)...")

        try:
            discovered = await BleakScanner.discover(timeout=5.0, return_adv=True)
            self.discovered_devices = []
            display_items = []
            target_idx = -1

            for idx, (d, adv) in enumerate(discovered.values()):
                name = d.name or adv.local_name or "Unnamed"
                uuids = [u.lower() for u in adv.service_uuids]
                item_str = f"{name} ({d.address}) | RSSI: {adv.rssi} dBm"
                self.discovered_devices.append((d, name, uuids))
                display_items.append(item_str)

                # Check if matches target UUID or teacher names
                if SERVICE_UUID.lower() in uuids:
                    target_idx = idx
                elif target_idx == -1 and any(k in name.lower() for k in ["esp", "grade", "ble", "teacher", "classroom"]):
                    target_idx = idx

            def _update_combo():
                self.device_combo['values'] = display_items
                if target_idx != -1:
                    self.device_combo.current(target_idx)
                    self.add_log(f"Auto-selected target device: {display_items[target_idx]}")
                elif display_items:
                    self.device_combo.current(0)
                else:
                    self.device_combo.set("No devices found nearby")
            self.root.after(0, _update_combo)

            self.add_log(f"Discovered {len(display_items)} real Bluetooth devices around PC.")
            self.set_status("Scan Complete", "#38bdf8")

        except Exception as e:
            self.add_log(f"Scan error: {str(e)}", is_error=True)
            self.set_status("Scan Error", "#ef4444")
        finally:
            self.is_busy = False

    # 2. Connection
    def on_connect_toggle(self):
        if self.is_connected:
            self.run_async(self._disconnect_async())
        else:
            self.run_async(self._connect_async())

    async def _disconnect_async(self):
        self.add_log("Disconnecting...")
        if self.client:
            try:
                await self.client.disconnect()
            except Exception:
                pass
        self.is_connected = False
        self.client = None
        self.set_status("Disconnected", "#64748b")
        self.root.after(0, lambda: self.connect_btn.config(text="Connect Selected", bg="#10b981"))
        self.add_log("Disconnected.")

    async def _connect_async(self):
        sel_idx = self.device_combo.current()
        if sel_idx < 0 or sel_idx >= len(self.discovered_devices):
            self.root.after(0, lambda: messagebox.showwarning("Select Device", "Please scan and select a device from the dropdown first."))
            return

        target_dev, dev_name, _ = self.discovered_devices[sel_idx]
        self.is_busy = True
        self.set_status(f"Connecting to {dev_name}...", "#f59e0b")
        self.add_log(f"Connecting to: {dev_name} ({target_dev.address})...")

        try:
            client = BleakClient(target_dev)
            await client.connect()
            self.client = client
            self.is_connected = True

            self.set_status(f"Connected ({dev_name})", "#10b981")
            self.root.after(0, lambda: self.connect_btn.config(text="Disconnect Device", bg="#dc2626"))
            self.add_log(f"Connected to {dev_name} successfully via PC Bluetooth!")

        except Exception as e:
            self.set_status("Connection Failed", "#ef4444")
            self.add_log(f"Connect error: {str(e)}", is_error=True)
            self.root.after(0, lambda: messagebox.showerror("Connection Error", f"Could not connect:\n{str(e)}"))
        finally:
            self.is_busy = False

    # 3. Step 1
    def on_step1(self):
        if not self.is_connected or not self.client:
            messagebox.showwarning("Not Connected", "Please connect to the BLE device first.")
            return
        self.run_async(self._step1_async())

    async def _step1_async(self):
        self.add_log("STEP 1: Reading Characteristic initial value...")
        try:
            val_bytes = await self.client.read_gatt_char(CHAR_UUID)
            val_text = val_bytes.decode('utf-8', errors='replace')
            val_b64 = base64.b64encode(val_bytes).decode('ascii')
            val_hex = val_bytes.hex(' ')

            def _show():
                self.s1_res.config(
                    text=f'Decoded Text: "{val_text}"\nBase64:       {val_b64}\nHex Bytes:    {val_hex}',
                    fg="#38bdf8"
                )
            self.root.after(0, _show)
            self.add_log(f'STEP 1 Success -> Text: "{val_text}", Hex: {val_hex}')
            return True
        except Exception as e:
            self.add_log(f"STEP 1 Error: {str(e)}", is_error=True)
            self.root.after(0, lambda: messagebox.showerror("Step 1 Error", str(e)))
            return False

    # 4. Step 2
    def on_step2(self):
        if not self.is_connected or not self.client:
            messagebox.showwarning("Not Connected", "Please connect to the BLE device first.")
            return
        self.run_async(self._step2_async())

    async def _step2_async(self):
        p1 = self.name_entry.get().strip()
        p2 = self.buddy_entry.get().strip()
        if not p1 or not p2:
            self.root.after(0, lambda: messagebox.showwarning("Missing Names", "Please enter both names."))
            return False

        payload_str = f"{p1} & {p2}"
        self.add_log(f'STEP 2: Writing values -> "{payload_str}"')

        payload_bytes = payload_str.encode('utf-8')
        payload_b64 = base64.b64encode(payload_bytes).decode('ascii')
        payload_hex = payload_bytes.hex(' ')

        try:
            try:
                await self.client.write_gatt_char(CHAR_UUID, payload_bytes, response=True)
            except Exception:
                await self.client.write_gatt_char(CHAR_UUID, payload_bytes, response=False)

            def _show():
                self.s2_res.config(
                    text=f'Written Payload: "{payload_str}"\nBase64:          {payload_b64}\nWritten Hex:     {payload_hex}',
                    fg="#34d399"
                )
            self.root.after(0, _show)
            self.add_log(f"STEP 2 Success -> Written Base64: {payload_b64}")
            return True
        except Exception as e:
            self.add_log(f"STEP 2 Error: {str(e)}", is_error=True)
            self.root.after(0, lambda: messagebox.showerror("Step 2 Error", str(e)))
            return False

    # 5. Step 3
    def on_step3(self):
        if not self.is_connected or not self.client:
            messagebox.showwarning("Not Connected", "Please connect to the BLE device first.")
            return
        self.run_async(self._step3_async())

    async def _step3_async(self):
        self.add_log("STEP 3: Reading Characteristic value (Predicted Grade)...")
        try:
            await asyncio.sleep(0.5)
            val_bytes = await self.client.read_gatt_char(CHAR_UUID)
            val_text = val_bytes.decode('utf-8', errors='replace')
            val_b64 = base64.b64encode(val_bytes).decode('ascii')
            val_hex = val_bytes.hex(' ')

            def _show():
                self.s3_res.config(
                    text=f'🎓 PREDICTED GRADE RESULT: "{val_text}"\nBase64:                    {val_b64}\nHex Bytes:                 {val_hex}',
                    fg="#facc15"
                )
            self.root.after(0, _show)
            self.add_log(f'STEP 3 Success -> PREDICTED GRADE: "{val_text}"')
            return True
        except Exception as e:
            self.add_log(f"STEP 3 Error: {str(e)}", is_error=True)
            self.root.after(0, lambda: messagebox.showerror("Step 3 Error", str(e)))
            return False

    # 6. Auto Run
    def on_auto_run(self):
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect to a device first.")
            return
        self.run_async(self._auto_run_async())

    async def _auto_run_async(self):
        self.add_log("--- STARTING AUTO WORKFLOW (STEPS 1 to 3) ---")
        ok1 = await self._step1_async()
        if not ok1:
            return
        await asyncio.sleep(0.8)
        ok2 = await self._step2_async()
        if not ok2:
            return
        await asyncio.sleep(0.8)
        await self._step3_async()
        self.add_log("--- COMPLETED AUTO WORKFLOW SUCCESSFULLY ---")

def main():
    root = tk.Tk()
    app = BleDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
