import subprocess
import time
import json
import os
from datetime import datetime

SCREENSHOT_DIR = os.path.expanduser("~/wayland_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

GET_ACTIVE_JS = """
var win = global.display.get_focus_window();
if (!win) null;
else ({
    title: win.get_title(),
    pid: win.get_pid(),
    wm_class: win.get_wm_class()
});
"""

def get_active_window():
    try:
        result = subprocess.run(
            [
                "gdbus", "call",
                "--session",
                "--dest", "org.gnome.Shell",
                "--object-path", "/org/gnome/Shell",
                "--method", "org.gnome.Shell.Eval",
                GET_ACTIVE_JS
            ],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        json_str = output.split(", ", 1)[1].rsplit(")", 1)[0]
        return json.loads(json_str)

    except Exception:
        return None

def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

    # grim is Wayland-native
    subprocess.run(["grim", path], check=False)

def main():
    print("Tracking active window on GNOME Wayland...")
    print("Taking screenshots every 10 seconds (permission prompt expected).")

    last_window = None
    last_screenshot = 0

    while True:
        now = time.time()

        # Checks active window
        window = get_active_window()
        if window and window != last_window:
            print("Active window changed:", window)
            last_window = window

        # every 10 seconds.
        if now - last_screenshot >= 10:
            take_screenshot()
            last_screenshot = now

        time.sleep(0.5)

if __name__ == "__main__":
    main()
