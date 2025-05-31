import sys
import subprocess
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QGridLayout
)
from PyQt5.QtCore import Qt

home_dir = os.path.expanduser("~")

class MyraWindow(QWidget):
    def __init__(self, fullscreen=False):
        super().__init__()
        self.setWindowTitle("Myra Dashboard")
        self.setGeometry(100, 100, 600, 400)

        if fullscreen:
            self.showFullScreen()

        layout = QGridLayout()

        # Title
        title = QLabel("🌟 Myra Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title, 0, 0, 1, -1)

        # Load apps from config
        self.apps = self.load_apps()

        # Styling
        button_height = 160 if fullscreen else 80
        font_size = 24 if fullscreen else 14
        max_columns = 5  # 👈 Wrap to next row after 5 columns

        row = 1
        col = 0
        for app_name, app_path in self.apps.items():
            button = QPushButton(f"{app_name}")
            button.setFixedHeight(button_height)
            button.setStyleSheet(f"font-size: {font_size}px;")
            button.clicked.connect(lambda checked, path=app_path: self.launch_app(path))
            layout.addWidget(button, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        self.setLayout(layout)

    def load_apps(self):
        config_path = os.path.join(home_dir, ".myra", "config", "apps.json")
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load apps.json: {e}")
            return {}

    def launch_app(self, path):
        try:
            subprocess.Popen([path])
            print(f"Launched: {path}")
        except FileNotFoundError:
            print(f"❌ Failed to launch: {path} not found.")

def main():
    app = QApplication(sys.argv)
    fullscreen = "--tv" in sys.argv
    window = MyraWindow(fullscreen=fullscreen)
    window.show() if not fullscreen else None
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
