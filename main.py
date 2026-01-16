import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import Gui

def main():
    app = QApplication(sys.argv)
    window = Gui()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()