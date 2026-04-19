import ctypes
import tkinter as tk

# --- Windows API ---
user32 = ctypes.windll.user32

ENUM_CURRENT_SETTINGS = -1
DM_DISPLAYORIENTATION = 0x80
DM_PELSWIDTH = 0x80000
DM_PELSHEIGHT = 0x100000

DMDO_DEFAULT = 0
DMDO_90 = 1
DMDO_180 = 2
DMDO_270 = 3

CDS_UPDATEREGISTRY = 0x01
CDS_RESET = 0x40000000


class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),

        ("dmPositionX", ctypes.c_long),
        ("dmPositionY", ctypes.c_long),
        ("dmDisplayOrientation", ctypes.c_ulong),
        ("dmDisplayFixedOutput", ctypes.c_ulong),

        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.c_ushort),

        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
    ]


def rotate(angle):
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)

    if not user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(dm)):
        set_status("❌ Failed to read display")
        return

    mapping = {0: DMDO_DEFAULT, 90: DMDO_270, 180: DMDO_180, 270: DMDO_90}
    new_orient = mapping.get(angle)

    if (dm.dmDisplayOrientation + new_orient) % 2 == 1:
        dm.dmPelsWidth, dm.dmPelsHeight = dm.dmPelsHeight, dm.dmPelsWidth

    dm.dmDisplayOrientation = new_orient
    dm.dmFields = DM_DISPLAYORIENTATION | DM_PELSWIDTH | DM_PELSHEIGHT

    user32.ChangeDisplaySettingsExW(
        None, ctypes.byref(dm), None,
        CDS_UPDATEREGISTRY | CDS_RESET, None
    )

    highlight_active(angle)
    set_status(f"✔ Rotated to {angle}°")


# --- UI helpers ---
def set_status(text):
    status_label.config(text=text)


def highlight_active(angle):
    for a, btn in buttons.items():
        if a == angle:
            btn.config(bg="#4a90e2")
        else:
            btn.config(bg="#2b2b2b")


def on_hover(btn, enter):
    btn.config(bg="#3a3a3a" if enter else "#2b2b2b")


def create_card(parent, text, angle, row, col):
    btn = tk.Label(
        parent,
        text=text,
        bg="#2b2b2b",
        fg="white",
        font=("Segoe UI", 12),
        width=12,
        height=4,
        bd=0,
        relief="flat"
    )

    btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    btn.bind("<Button-1>", lambda e: rotate(angle))
    btn.bind("<Enter>", lambda e: on_hover(btn, True))
    btn.bind("<Leave>", lambda e: on_hover(btn, False))

    buttons[angle] = btn


# --- Main Window ---
app = tk.Tk()
app.title("Screen Rotator")
app.geometry("360x300")
app.configure(bg="#1e1e1e")

buttons = {}

# Title
tk.Label(app, text="Screen Rotator", fg="white", bg="#1e1e1e",
         font=("Segoe UI", 16, "bold")).pack(pady=10)

# Grid container
frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(expand=True)

frame.grid_rowconfigure((0, 1), weight=1)
frame.grid_columnconfigure((0, 1), weight=1)

# Cards (directional layout)
create_card(frame, "⬆\nNormal\n0°", 0, 0, 0)
create_card(frame, "➡\nRight\n270°", 270, 0, 1)
create_card(frame, "⬅\nLeft\n90°", 90, 1, 0)
create_card(frame, "⬇\nUpside\n180°", 180, 1, 1)

# Status bar
status_label = tk.Label(app, text="Ready", fg="#aaaaaa",
                        bg="#1e1e1e", font=("Segoe UI", 10))
status_label.pack(pady=8)


# --- Keyboard shortcuts (UX boost) ---
app.bind("<Up>", lambda e: rotate(0))
app.bind("<Left>", lambda e: rotate(90))
app.bind("<Down>", lambda e: rotate(180))
app.bind("<Right>", lambda e: rotate(270))

app.mainloop()
