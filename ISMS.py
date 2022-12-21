"""系统入口"""

from view.login_ui import LoginUI
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    login = LoginUI()
    login.ui.show()
    app.exec()
