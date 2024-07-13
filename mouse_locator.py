import pyautogui
import tkinter as tk
import threading
import time
import ctypes

class MouseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.label = tk.Label(self, text="", font=("Arial", 12), bg="yellow")
        self.label.pack()
        self.overrideredirect(True)  # Remove window decorations
        self.wm_attributes("-topmost", True)  # Keep the window on top
        self.update_position()
        self.make_window_clickthrough()
    
    def make_window_clickthrough(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        styles = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, styles | 0x80000 | 0x20)

    def update_position(self):
        # Get the current position of the mouse
        x, y = pyautogui.position()
        # Update label text
        self.label.config(text=f"({x}, {y})")
        # Position the window near the mouse cursor
        self.geometry(f"+{x+20}+{y+20}")
        # Call this method again after a short delay
        self.after(5, self.update_position)

def run_tracker():
    app = MouseTracker()
    app.mainloop()

# Run the tracker in a separate thread
thread = threading.Thread(target=run_tracker)
thread.daemon = True
thread.start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Tracking stopped by user.")
