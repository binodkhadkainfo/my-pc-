import subprocess
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDial
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor


def get_current_brightness():
    try:
        output = subprocess.check_output(["ddcutil", "getvcp", "10"], stderr=subprocess.DEVNULL)
        for line in output.decode().splitlines():
            if "current value" in line:
                return int(line.split("current value = ")[1].split(",")[0])
    except Exception:
        return -1


def set_brightness(val):
    try:
        brightness = int(val)
        subprocess.run(["ddcutil", "setvcp", "10", str(brightness)], stderr=subprocess.DEVNULL)
        return f"Brightness set to {brightness}%"
    except Exception:
        return "Failed to set brightness."


class BrightnessUI(QWidget):
    def __init__(self, initial_brightness):
        super().__init__()
        self.setWindowTitle("Brightness Control")
        self.setFixedSize(300, 180)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.label = QLabel("...", self)
        self.label.setFont(QFont("Monospace", 24))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")

        self.info = QLabel("Brightness Controller", self)
        self.info.setFont(QFont("Monospace", 10))
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setStyleSheet("color: white;")

        self.status = QLabel("", self)  # New label for status messages
        self.status.setFont(QFont("Monospace", 10))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: lightgreen;")

        self.dial = QDial(self)
        self.dial.setRange(0, 100)
        self.dial.setNotchesVisible(True)
        self.dial.setStyleSheet("""
            QDial {
                background-color: rgba(166, 124, 82, 180);
                border-radius: 60px;
            }
        """)
        self.dial.valueChanged.connect(self.change_brightness)

        if initial_brightness != -1:
            self.dial.setValue(initial_brightness)
            self.label.setText(f"{initial_brightness}%")
        else:
            self.label.setText("N/A")

        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        layout.addWidget(self.info)
        layout.addWidget(self.status)  # Add status label
        self.setLayout(layout)

    def change_brightness(self, value):
        result = set_brightness(value)
        self.label.setText(f"{value}%")
        self.status.setText(result)


def check_cursor_and_close(app, window):
    cursor_pos = QCursor.pos()
    if window.geometry().contains(cursor_pos):
        pass
    else:
        app.quit()


if __name__ == "__main__":
    current = get_current_brightness()
    if current == -1:
        initial_brightness = 50
    else:
        initial_brightness = min(current + 5, 100)
        # You can update the UI label instead of printing here
        # No print statement!

    app = QApplication(sys.argv)
    window = BrightnessUI(initial_brightness)
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: check_cursor_and_close(app, window))
    timer.start(500)

    sys.exit(app.exec())
