import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDial
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QGuiApplication, QCursor


def get_current_brightness():
    try:
        output = subprocess.check_output(
            ["ddcutil", "getvcp", "10"],
            stderr=subprocess.DEVNULL
        ).decode()

        for line in output.splitlines():
            if "current value" in line:
                return int(line.split("current value = ")[1].split(",")[0])
    except Exception:
        return -1


def set_brightness(val):
    try:
        val = int(val)
        subprocess.run(
            ["ddcutil", "setvcp", "10", str(val)],
            stderr=subprocess.DEVNULL
        )
        return f"{val}%"
    except Exception:
        return "Error"


class BrightnessOSD(QWidget):
    def __init__(self, initial_brightness):
        super().__init__()

        self.setFixedSize(300, 180)

        # 🔥 KEEP YOUR UI/UX STYLE
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()

        # Main label (your original UI feel)
        self.label = QLabel("...", self)
        self.label.setFont(QFont("Monospace", 26))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        # Dial (your UX core)
        self.dial = QDial(self)
        self.dial.setRange(0, 100)
        self.dial.setNotchesVisible(True)
        self.dial.setStyleSheet("""
            QDial {
                background-color: rgba(166, 124, 82, 180);
                border-radius: 60px;
            }
        """)
        layout.addWidget(self.dial)

        # Info text
        self.info = QLabel("Brightness Controller", self)
        self.info.setFont(QFont("Monospace", 10))
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setStyleSheet("color: white;")
        layout.addWidget(self.info)

        # Status
        self.status = QLabel("", self)
        self.status.setFont(QFont("Monospace", 10))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: lightgreen;")
        layout.addWidget(self.status)

        self.setLayout(layout)

        # 📍 Top-right position (your OSD style)
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 20)

        # Init brightness
        if initial_brightness != -1:
            self.dial.setValue(initial_brightness)
            self.label.setText(f"{initial_brightness}%")
        else:
            self.dial.setValue(50)
            self.label.setText("50%")

        self.dial.valueChanged.connect(self.change_brightness)

        # ⏱ cursor check
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_cursor)
        self.timer.start(200)

    # ---------- BRIGHTNESS ----------
    def change_brightness(self, value):
        result = set_brightness(value)
        self.label.setText(f"{value}%")
        self.status.setText(result)

    # ---------- FIXED CLOSE LOGIC ----------
    def check_cursor(self):
        cursor = QCursor.pos()

        # simple correct UX rule
        if not self.geometry().contains(cursor):
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    current = get_current_brightness()
    if current == -1:
        current = 50

    window = BrightnessOSD(current)
    window.show()

    sys.exit(app.exec())
