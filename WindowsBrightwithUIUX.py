import sys
import screen_brightness_control as sbc

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDial
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor


def get_current_brightness():
    """
    Get current brightness on Windows using screen_brightness_control
    """
    try:
        brightness = sbc.get_brightness(display=0)

        if isinstance(brightness, list):
            return int(brightness[0])

        return int(brightness)
    except Exception:
        return -1


def set_brightness(val):
    """
    Set brightness on Windows using screen_brightness_control
    """
    try:
        brightness = int(val)
        sbc.set_brightness(brightness, display=0)
        return f"Brightness set to {brightness}%"
    except Exception:
        return "Failed to set brightness."


class BrightnessUI(QWidget):
    def __init__(self, initial_brightness):
        super().__init__()

        self.setWindowTitle("Brightness Control")
        self.setFixedSize(300, 220)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.label = QLabel("...", self)
        self.label.setFont(QFont("Consolas", 24))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")

        self.info = QLabel("Brightness Controller", self)
        self.info.setFont(QFont("Consolas", 10))
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setStyleSheet("color: white;")

        self.status = QLabel("", self)
        self.status.setFont(QFont("Consolas", 10))
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
            self.dial.setValue(50)
            self.label.setText("50%")

        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        layout.addWidget(self.info)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def change_brightness(self, value):
        result = set_brightness(value)
        self.label.setText(f"{value}%")
        self.status.setText(result)


def check_cursor_and_close(app, window):
    cursor_pos = QCursor.pos()

    if not window.geometry().contains(cursor_pos):
        app.quit()


if __name__ == "__main__":
    current = get_current_brightness()

    if current == -1:
        initial_brightness = 50
    else:
        initial_brightness = min(current + 5, 100)

    app = QApplication(sys.argv)

    window = BrightnessUI(initial_brightness)
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: check_cursor_and_close(app, window))
    timer.start(500)

    sys.exit(app.exec())
