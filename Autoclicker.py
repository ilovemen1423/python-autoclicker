import tkinter as tk
import threading
import time
import pyautogui
from pynput import keyboard, mouse

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

clicking = False
enabled = True
cps = 10

toggle_key = None
temp_key = None
capturing = False

# clicking loop
def click_loop():
    global clicking
    while True:
        if clicking and enabled:
            pyautogui.click()
            time.sleep(1.0 / cps)
        else:
            time.sleep(0.001)

# keyboard input
def on_key_press(key):
    global clicking, toggle_key, temp_key, capturing

    if capturing:
        if temp_key is None:
            temp_key = key
            key_label.config(text=f"Selected: {key} | ENTER confirm | DELETE redo")
            return

        if key == keyboard.Key.enter:
            toggle_key = temp_key
            capturing = False
            key_label.config(text=f"Keybind set: {toggle_key}")
            return

        if key == keyboard.Key.delete:
            temp_key = None
            key_label.config(text="Redo keybind: press key or mouse button")
            return

    else:
        if key == toggle_key and enabled:
            toggle_click()

# mouse input
def on_mouse_click(x, y, button, pressed):
    global toggle_key, temp_key, capturing

    if not pressed:
        return

    if capturing:
        if temp_key is None:
            temp_key = button
            key_label.config(text=f"Selected: {button} | ENTER confirm | DELETE redo")
            return

    else:
        if button == toggle_key and enabled:
            toggle_click()

def toggle_click():
    global clicking
    clicking = not clicking
    status_label.config(text="Clicking: " + ("ON" if clicking else "OFF"))

def start_listeners():
    keyboard.Listener(on_press=on_key_press).start()
    mouse.Listener(on_click=on_mouse_click).start()

def apply_cps(event=None):
    global cps
    try:
        cps = float(cps_entry.get())
    except:
        cps = 10
    root.focus()

def capture_key():
    global capturing, temp_key
    capturing = True
    temp_key = None
    key_label.config(text="Press a key or mouse button...")

def toggle_enabled():
    global enabled, clicking
    enabled = not enabled
    clicking = False

    if enabled:
        enable_button.config(text="Turn OFF")
        enabled_label.config(text="Autoclicker Enabled", fg="#4cff4c")
    else:
        enable_button.config(text="Turn ON")
        enabled_label.config(text="Autoclicker Disabled", fg="#ff4c4c")
        status_label.config(text="Clicking: OFF")

# UI
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("360x280")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="Auto Clicker", font=("Segoe UI",16,"bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

tk.Label(root,text="Clicks Per Second",bg="#1e1e1e",fg="white").pack()

cps_entry = tk.Entry(root,justify="center",bg="#2b2b2b",fg="white",insertbackground="white")
cps_entry.insert(0,"10")
cps_entry.pack(pady=5)

cps_entry.bind("<Return>",apply_cps)

tk.Label(root,text="(Press ENTER to apply)",bg="#1e1e1e",fg="#aaaaaa").pack()

tk.Button(root,text="Set Keybind",command=capture_key,bg="#3a3a3a",fg="white").pack(pady=10)

key_label = tk.Label(root,text="No keybind set",bg="#1e1e1e",fg="#cccccc")
key_label.pack()

status_label = tk.Label(root,text="Clicking: OFF",bg="#1e1e1e",fg="#ff6b6b",font=("Segoe UI",10,"bold"))
status_label.pack(pady=5)

enable_button = tk.Button(root,text="Turn OFF",command=toggle_enabled,bg="#444444",fg="white")
enable_button.pack(pady=5)

enabled_label = tk.Label(root,text="Autoclicker Enabled",bg="#1e1e1e",fg="#4cff4c")
enabled_label.pack()

threading.Thread(target=click_loop,daemon=True).start()
start_listeners()

root.mainloop()