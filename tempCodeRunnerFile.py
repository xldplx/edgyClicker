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
        self.root.geometry("250x350")  # Set a taller window size
        self.root.resizable(False, False)  # Disable resizing

        # Set dark theme
        self.root.configure(bg="#1E1E1E")  # Dark background for the window
        
        # Apply modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', padding=6, font=('Helvetica', 10), borderwidth=1, relief="flat", background="#4B4B4B", foreground="white")
        self.style.map('TButton', background=[('active', '#6B6B6B')])
        self.style.configure('TLabel', font=('Helvetica', 12), background="#1E1E1E", foreground="white")
        self.style.configure('TEntry', padding=5, font=('Helvetica', 10), fieldbackground="#4B4B4B", foreground="white")
        self.style.configure('TCombobox', fieldbackground="#4B4B4B", foreground="white")  # Style for Combobox

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10", relief="flat", style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.clicking = False
        self.cps = 10  # Default clicks per second
        self.hotkey = 'ALT + 1'  # Default hotkey to activate auto-clicking

        # Limited list of hotkey options (ALT + 1 to ALT + 0)
        self.hotkey_options = [
            'ALT + 1', 'ALT + 2', 'ALT + 3', 'ALT + 4', 'ALT + 5',
            'ALT + 6', 'ALT + 7', 'ALT + 8', 'ALT + 9', 'ALT + 0'
        ]

        # Hotkey Label and Dropdown
        self.hotkey_label = ttk.Label(self.main_frame, text="Select Hotkey:")
        self.hotkey_label.pack(pady=(10, 0))  # Add some top padding

        self.hotkey_dropdown = ttk.Combobox(self.main_frame, values=self.hotkey_options, state="readonly", width=12)
        self.hotkey_dropdown.pack(pady=(5, 10))  # Add some padding between elements
        self.hotkey_dropdown.set(self.hotkey)  # Set default hotkey in dropdown

        # CPS Label and Entry
        self.cps_label = ttk.Label(self.main_frame, text="Clicks Per Second:")
        self.cps_label.pack(pady=(10, 0))

        self.cps_entry = ttk.Entry(self.main_frame)
        self.cps_entry.pack(pady=(5, 10))
        self.cps_entry.insert(0, str(self.cps))  # Set default CPS in entry

        # Apply Settings Button
        self.apply_button = ttk.Button(self.main_frame, text="Apply Settings", command=self.apply_settings)
        self.apply_button.pack(pady=(10, 0))

        # Clicking Status Indicator
        self.status_label = ttk.Label(self.main_frame, text="Status: Inactive", foreground="red", font=('Helvetica', 12))
        self.status_label.pack(pady=(10, 0))

        # Ensure proper cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the hotkey
        self.current_hotkey = None

    def apply_settings(self):
        """Apply selected options."""
        self.hotkey = self.hotkey_dropdown.get()
        self.cps = float(self.cps_entry.get())

        # If there's an active hotkey, unhook it before re-assigning
        if self.current_hotkey is not None:
            keyboard.unhook(self.current_hotkey)

        # Assign new hotkey
        self.current_hotkey = keyboard.add_hotkey(self.hotkey, self.toggle_clicking)  # Assign new hotkey

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if not self.clicking:  # Start clicking only if it's not already clicking
            self.clicking = True
            self.status_label.config(text="Status: Active", foreground="green")
            threading.Thread(target=self.auto_click).start()

    def stop_clicking(self):
        self.clicking = False
        self.status_label.config(text="Status: Inactive", foreground="red")

    def auto_click(self):
        interval = 1.0 / self.cps  # Calculate the interval based on CPS
        next_click_time = time.time()  # Start time

        while self.clicking:
            current_time = time.time()
            if current_time >= next_click_time:  # Check if it's time to click
                pyautogui.click()  # Click at the current mouse position
                next_click_time += interval  # Schedule the next click

    def on_closing(self):
        self.stop_clicking()  # Stop clicking
        self.root.destroy()   # Close the application

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
