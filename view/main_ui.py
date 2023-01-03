"""主程序窗口"""

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from view import login_ui
from controller import main_controller
from view import changePwd_ui
from view import order_ui, order_query_ui
from view import warehouse_in_ui

newWindow = None


class MainUI:
    def __init__(self, userid, uName, uType):
        self.ui = QUiLoader().load('view/ui/main.ui')
        self.userid = userid
        self.uName = uName
        self.uType = uType
        print(self.userid, self.uName, self.uType)

        if self.uType == "销售员":
            self.ui.purchase.setEnabled(False)
            self.ui.warehouse.setEnabled(False)
        elif self.uType == "采购员":
            self.ui.sales.setEnabled(False)
            self.ui.warehouse.setEnabled(False)
        elif self.uType == "仓管员":
            self.ui.sales.setEnabled(False)
            self.ui.purchase.setEnabled(False)

        self.roleid = main_controller.get_roleID(self.userid, self.uType)
        self.roleid = self.roleid[0][0]
        self.ui.statusbar.showMessage("当前用户是" + self.uType + str(self.roleid) + ":" + self.uName + "。欢迎您！")

        self.ui.relogin.triggered.connect(self.relogin)
        self.ui.exit.triggered.connect(self.exit)
        self.ui.changePwd.triggered.connect(self.changePwd)

        self.ui.order.triggered.connect(self.order)
        self.ui.query_purchase.triggered.connect(self.query_purchase)

        self.ui.warehouse_in.triggered.connect(self.warehouse)

    def relogin(self):
        global newWindow
        newWindow = login_ui.LoginUI()
        newWindow.ui.show()
        self.ui.close()

    def exit(self):
        self.ui.close()

    def changePwd(self):
        global newWindow
        newWindow = changePwd_ui.ChangePwdUI(self.userid)
        newWindow.ui.show()

    def order(self):
        global newWindow
        newWindow = order_ui.OrderUI(self.roleid)
        newWindow.ui.show()

    def query_purchase(self):
        global newWindow
        newWindow = order_query_ui.QueryPurchaseUI(self.roleid)
        newWindow.ui.show()

    def warehouse(self):
        global newWindow
        newWindow = warehouse_in_ui.WarehouseUI(self.roleid)
        newWindow.ui.show()


if __name__ == "__main__":
    app = QApplication([])
    main = MainUI()
    main.ui.show()
    app.exec()
