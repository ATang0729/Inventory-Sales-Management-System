"""采购订单下达界面"""

from controller import order_controller
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from view import order_query_ui

newWindow = None


class OrderUI:
    def __init__(self, purchaserID):
        self.ui = QUiLoader().load('view/order.ui')
        self.purchaserID = purchaserID
        self.ui.orderButton.clicked.connect(self.order)
        self.ui.queryButton.clicked.connect(self.query)
        self.ui.exitButton.clicked.connect(self.exit)

    def order(self):
        cName = self.ui.nameEdit.text()
        sName = self.ui.supplyEdit.text()
        price = self.ui.priceBox.value()
        num = self.ui.quantityBox.value()
        measure = self.ui.measureEdit.text()
        if cName.strip() == "" or sName.strip() == "" or measure.strip() == "":
            QMessageBox.information(self.ui, "提示", "InputError2:请填写完整信息！")
            return False
        if price <= 0 or num <= 0:
            QMessageBox.information(self.ui, "提示", "InputError5:输入的价格或数量需大于零！")
            return False
        else:
            flag = order_controller.order(self.purchaserID, cName, sName, price, num, measure)
            if flag:
                QMessageBox.information(self.ui, "提示", "下达成功！")
            elif flag == False:
                QMessageBox.information(self.ui, "提示", "下达失败！")
            elif flag is None:
                QMessageBox.information(self.ui, "提示", "LinkError：数据库连接失败！")

    def query(self):
        global newWindow
        newWindow = order_query_ui.QueryPurchaseUI(self.purchaserID)
        newWindow.ui.show()
        self.ui.close()

    def exit(self):
        self.ui.close()
