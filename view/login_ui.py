"""登录窗口，动态加载login.ui文件"""

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from controller import login_controller
from view import main_ui


main = None


class LoginUI:
    def __init__(self):
        load = QUiLoader().load('view/login.ui')
        self.ui = load
        self.ui.buttonBox.accepted.connect(self.login)
        self.ui.buttonBox.rejected.connect(self.exit)

    def login(self):
        userid = self.ui.uidEdit.text()
        password = self.ui.uPwdEdit.text()
        if userid.strip() == "" or password.strip() == "":
            QMessageBox.warning(self.ui, "警告", "InputError2：用户名或密码不能为空")
            return False
        flag = login_controller.login(userid, password)
        if flag[0]:
            uName = flag[1][0]
            uType = flag[1][1]
            global main
            main = main_ui.MainUI(userid, uName, uType)
            main.ui.show()
            self.ui.close()
        elif flag[1] == "LinkError":
            QMessageBox.warning(self.ui, "警告", "LinkError：数据库连接失败！")
        elif flag[1] == "LoginError1":
            QMessageBox.information(self.ui, '提示', 'LoginError1：用户不存在', QMessageBox.Yes)
        elif flag[1] == "LoginError2":
            QMessageBox.information(self.ui, '提示', 'LoginError2：密码错误', QMessageBox.Yes)

    def exit(self):
        self.ui.close()


if __name__ == "__main__":
    app = QApplication([])
    login = LoginUI()
    login.ui.show()
    app.exec()
