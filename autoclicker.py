import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key
import tkinter as tk
from tkinter import ttk

# Global vars
delay = 1.0 / 50
button = Button.left
start_stop_key = KeyCode(char='s')
stop_key = KeyCode(char='k')
time_unit = 'minute'  # Default unit

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.01)

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

ctrl_pressed = False

def on_press(key):
    global ctrl_pressed
    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = True
    if key == start_stop_key and ctrl_pressed:
        if click_thread.running:
            click_thread.stop_clicking()
            update_status("Stopped")
        else:
            click_thread.start_clicking()
            update_status("Clicking")
    elif key == stop_key:
        click_thread.exit()
        listener.stop()

def on_release(key):
    global ctrl_pressed
    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False

listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

# GUI setup
def start_clicking():
    click_thread.start_clicking()
    update_status("Clicking")

def stop_clicking():
    click_thread.stop_clicking()
    update_status("Stopped")

def exit_program():
    click_thread.exit()
    root.destroy()

def update_status(status):
    status_var.set(f"Status: {status}")

def set_speed(clicks, unit):
    global delay
    if unit == 'second':
        delay = 1.0 / clicks
    elif unit == 'minute':
        delay = 60.0 / clicks
    elif unit == 'hour':
        delay = 3600.0 / clicks
    click_thread.delay = delay
    update_status(f"Speed set to {clicks} clicks per {unit}")

def set_time_unit(unit):
    global time_unit
    time_unit = unit
    update_status(f"Time unit set to {unit}")

root = tk.Tk()
root.title("Autoclicker")

# Load and set the icon
icon_path = "/home/mute/Desktop/code/random_python/autoclicker/icon.gif"

root.iconphoto(False, tk.PhotoImage(file=icon_path))

root.configure(bg='black')
style = ttk.Style()
style.configure("TButton", foreground="black", background="grey", font=("Helvetica", 12), padding=10)
style.configure("TLabel", foreground="black", background="grey", font=("Helvetica", 14))

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
frame.configure(style="TFrame", borderwidth=2, relief="sunken")

start_button = ttk.Button(frame, text="Start", command=start_clicking)
start_button.grid(row=0, column=0, padx=5, pady=5)

stop_button = ttk.Button(frame, text="Stop", command=stop_clicking)
stop_button.grid(row=0, column=1, padx=5, pady=5)

exit_button = ttk.Button(frame, text="Exit", command=exit_program)
exit_button.grid(row=0, column=2, padx=5, pady=5)

status_var = tk.StringVar()
status_label = ttk.Label(frame, textvariable=status_var)
status_label.grid(row=1, column=0, columnspan=3, pady=10)

shortcuts_label = ttk.Label(frame, text="Shortcuts: Start/Stop: Ctrl+S | Exit: Ctrl+K", foreground="black", background="light grey", font=("Helvetica", 10))
shortcuts_label.grid(row=2, column=0, columnspan=3, pady=10)

update_status("Stopped")

menu_bar = tk.Menu(root, bg='grey', fg='black')
menu_speed = tk.Menu(menu_bar, tearoff=0, bg='grey', fg='black')
menu_unit = tk.Menu(menu_bar, tearoff=0, bg='grey', fg='black')
menu_4 = tk.Menu(menu_bar, tearoff=0, bg='grey', fg='black')

menu_speed.add_command(label="100 clicks per selected unit", command=lambda: set_speed(100, time_unit))
menu_speed.add_command(label="200 clicks per selected unit", command=lambda: set_speed(200, time_unit))
menu_speed.add_command(label="300 clicks per selected unit", command=lambda: set_speed(300, time_unit))
menu_speed.add_command(label="400 clicks per selected unit", command=lambda: set_speed(400, time_unit))
menu_speed.add_command(label="500 clicks per selected unit", command=lambda: set_speed(500, time_unit))
menu_speed.add_command(label="600 clicks per selected unit", command=lambda: set_speed(600, time_unit))
menu_speed.add_command(label="700 clicks per selected unit", command=lambda: set_speed(700, time_unit))
menu_speed.add_command(label="800 clicks per selected unit", command=lambda: set_speed(800, time_unit))
menu_speed.add_command(label="900 clicks per selected unit", command=lambda: set_speed(900, time_unit))
menu_speed.add_command(label="1000 clicks per selected unit", command=lambda: set_speed(1000, time_unit))

menu_unit.add_command(label="Per Second", command=lambda: set_time_unit('second'))
menu_unit.add_command(label="Per Minute", command=lambda: set_time_unit('minute'))
menu_unit.add_command(label="Per Hour", command=lambda: set_time_unit('hour'))

menu_4.add_command(label="10000 clicks per selected unit", command=lambda: set_speed(10000, time_unit))

menu_bar.add_cascade(label="Speed Settings", menu=menu_speed)
menu_bar.add_cascade(label="Time Unit", menu=menu_unit)
menu_bar.add_cascade(label="THE BIG ONE", menu=menu_4)

root.config(menu=menu_bar)

root.mainloop()
