from pydbus import SessionBus
import json
import time

# JavaScript to run inside GNOME Shell
GET_ACTIVE_JS = """
var win = global.display.get_focus_window();
if (!win) null;
else ({
    title: win.get_title(),
    pid: win.get_pid(),
    wm_class: win.get_wm_class()
});
"""

def get_active_window(shell):
    ok, result = shell.Eval(GET_ACTIVE_JS)
    if not ok:
        return None
    try:
        return json.loads(result)
    except Exception:
        return None

def main():
    bus = SessionBus()
    shell = bus.get("org.gnome.Shell")

    last = None
    print("Tracking active window on GNOME Wayland...")

    while True:
        current = get_active_window(shell)
        if current != last:
            print("Active window:", current)
            last = current
        time.sleep(0.2)

if __name__ == "__main__":
    main()
