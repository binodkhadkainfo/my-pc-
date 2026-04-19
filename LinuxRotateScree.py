import tkinter as tk
import subprocess


MONITOR = "DP-1"   # Your monitor from xrandr output

def rotate(angle):
   transform_map = {
       0: 0,   # normal
       90: 1,  # rotate left
       180: 2,
       270: 3
   }

   transform = transform_map[angle]

   try:
       cmd = f"hyprctl keyword monitor {MONITOR},preferred,auto,1,transform,{transform}"
       subprocess.run(cmd, shell=True, check=True)

       highlight_active(angle)
       set_status(f"✔ Rotated to {angle}°")

   except Exception as e:
       set_status("❌ Rotation failed")


# UI Helpers

def set_status(text):
   status_label.config(text=text)


def highlight_active(angle):
   for a, btn in buttons.items():
       if a == angle:
           btn.config(bg="#4a90e2")
       else:
           btn.config(bg="#2b2b2b")


def hover(btn, state):
   btn.config(bg="#3a3a3a" if state else "#2b2b2b")


def create_btn(parent, text, angle, row, col):
   btn = tk.Label(
       parent,
       text=text,
       bg="#2b2b2b",
       fg="white",
       font=("Arial", 12),
       width=12,
       height=4,
       cursor="hand2"
   )

   btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

   btn.bind("<Button-1>", lambda e: rotate(angle))
   btn.bind("<Enter>", lambda e: hover(btn, True))
   btn.bind("<Leave>", lambda e: hover(btn, False))

   buttons[angle] = btn


# Window
app = tk.Tk()
app.title("Hyprland Screen Rotator")
app.geometry("380x330")
app.configure(bg="#1e1e1e")
app.resizable(False, False)

buttons = {}

# Title
tk.Label(
   app,
   text="Hyprland Screen Rotator",
   fg="white",
   bg="#1e1e1e",
   font=("Arial", 16, "bold")
).pack(pady=12)

# Grid
frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(expand=True)

frame.grid_rowconfigure((0, 1), weight=1)
frame.grid_columnconfigure((0, 1), weight=1)

# Buttons
create_btn(frame, "⬆\nNormal\n0°", 0, 0, 0)
create_btn(frame, "➡\nRight\n270°", 270, 0, 1)
create_btn(frame, "⬅\nLeft\n90°", 90, 1, 0)
create_btn(frame, "⬇\nUpside\n180°", 180, 1, 1)

# Info
tk.Label(
   app,
   text=f"Monitor: {MONITOR} | Hyprland",
   fg="#bbbbbb",
   bg="#1e1e1e",
   font=("Arial", 10)
).pack()

# Status
status_label = tk.Label(
   app,
   text="Ready",
   fg="#aaaaaa",
   bg="#1e1e1e",
   font=("Arial", 10)
)
status_label.pack(pady=8)

# Keyboard shortcuts
app.bind("<Up>", lambda e: rotate(0))
app.bind("<Left>", lambda e: rotate(90))
app.bind("<Down>", lambda e: rotate(180))
app.bind("<Right>", lambda e: rotate(270))

app.mainloop()
