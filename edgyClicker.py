import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time
import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("edgyClicker")
        self.root.geometry("300x300")  # Adjusted size for better UI
        self.root.resizable(False, False)

        # Set dark theme
        self.root.configure(bg="#1E1E1E")

        # Apply modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', padding=6, font=('Helvetica', 10), borderwidth=1, relief="flat", background="white", foreground="black", focuscolor="none")
        self.style.map('TButton', background=[('active', '#D3D3D3')], relief=[('pressed', '!focus', 'sunken')])
        self.style.configure('TLabel', font=('Helvetica', 12), background="black", foreground="white")
        self.style.configure('TEntry', padding=5, font=('Helvetica', 10), fieldbackground="white", foreground="black", borderwidth=2, relief="flat", focuscolor="none")
        self.style.configure('TCombobox', padding=5, font=('Helvetica', 10), fieldbackground="white", foreground="black", borderwidth=2, relief="flat", focuscolor="none")

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.clicking = False
        self.cps = 10  # Default clicks per second
        self.hotkey = 'ALT + 1'  # Default hotkey to activate auto-clicking

        # Hotkey options
        self.hotkey_options = [f'ALT + {i}' for i in range(1, 11)]

        # Hotkey Label and Dropdown
        self.hotkey_label = ttk.Label(self.main_frame, text="Select Hotkey:")
        self.hotkey_label.pack(pady=(10, 0))

        self.hotkey_dropdown = ttk.Combobox(self.main_frame, values=self.hotkey_options, state="readonly", width=12)
        self.hotkey_dropdown.pack(pady=(5, 10))
        self.hotkey_dropdown.set(self.hotkey)

        # CPS Label and Entry
        self.cps_label = ttk.Label(self.main_frame, text="Clicks Per Second:")
        self.cps_label.pack(pady=(10, 0))

        self.cps_entry = ttk.Entry(self.main_frame)
        self.cps_entry.pack(pady=(5, 10))
        self.cps_entry.insert(0, str(self.cps))

        # Apply Settings Button
        self.apply_button = ttk.Button(self.main_frame, text="Apply Settings", command=self.apply_settings)
        self.apply_button.pack(pady=(10, 0))

        # Clicking Status Indicator
        self.status_label = ttk.Label(self.main_frame, text="Status: Inactive", foreground="red", font=('Helvetica', 12))
        self.status_label.pack(pady=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize hotkey
        self.current_hotkey = None

    def apply_settings(self):
        """Apply selected options."""
        self.hotkey = self.hotkey_dropdown.get()
        self.cps = float(self.cps_entry.get())

        if self.current_hotkey is not None:
            keyboard.unhook(self.current_hotkey)

        self.current_hotkey = keyboard.add_hotkey(self.hotkey, self.toggle_clicking)

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.status_label.config(text="Status: Active", foreground="green")
            threading.Thread(target=self.auto_click).start()

    def stop_clicking(self):
        self.clicking = False
        self.status_label.config(text="Status: Inactive", foreground="red")

    def auto_click(self):
        interval = 1.0 / self.cps
        next_click_time = time.time()

        while self.clicking:
            current_time = time.time()
            if current_time >= next_click_time:
                pyautogui.click()
                next_click_time += interval

    def on_closing(self):
        self.stop_clicking()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
