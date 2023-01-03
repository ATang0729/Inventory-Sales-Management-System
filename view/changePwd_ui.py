"""修改密码界面"""

from controller import changePwd_controller
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader


class ChangePwdUI:
    def __init__(self, userid):
        load = QUiLoader().load('view/ui/changePwd.ui')
        self.ui = load
        self.ui.buttonBox.accepted.connect(self.changePwd)
        self.ui.buttonBox.rejected.connect(self.exit)
        self.uid = userid

    def changePwd(self):
        password = self.ui.uPwdEdit.text()
        newPwd = self.ui.newPwdEdit.text()
        newPwd2 = self.ui.newPwdEdit2.text()
        if password.strip() == "" or newPwd.strip() == "" or newPwd2.strip() == "":
            QMessageBox.warning(self.ui, "警告", "InputError2：输入项不能为空")
            return False
        if newPwd != newPwd2:
            QMessageBox.warning(self.ui, "警告", "InputError3：两次输入的新密码不一致")
            return False
        flag1 = changePwd_controller.query_pwd(self.uid, password)
        if not flag1:
            QMessageBox.warning(self.ui, "警告", "LoginError2：原密码错误")
            return False
        flag2 = changePwd_controller.changePwd(self.uid, newPwd)
        if flag2:
            QMessageBox.information(self.ui, "提示", "密码修改成功")
            self.ui.close()
        elif flag2 is None:
            QMessageBox.warning(self.ui, "警告", "LinkError：数据库连接失败！")

    def exit(self):
        self.ui.close()