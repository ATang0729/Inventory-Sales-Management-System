"""销售出库界面"""

from view import sale_query_ui
from controller import sale_controller
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader

newWindow = None


class SaleUI:
    def __init__(self, sID):
        load = QUiLoader().load('view/ui/sale.ui')
        self.sID = sID

        self.ui = load
        self.ui.saleButton.clicked.connect(self.sale)
        self.ui.queryButton.clicked.connect(self.query)
        self.ui.exitButton.clicked.connect(self.exit)
        self.ui.cNameEdit.textChanged.connect(self.refresh)
        self.ui.tableWidget.itemDoubleClicked.connect(self.itemClicked)

        self.refresh()

    def itemClicked(self):
        row = self.ui.tableWidget.currentRow()
        cName = self.ui.tableWidget.item(row, 1).text()
        self.ui.cNameEdit.setText(cName)

    def refresh(self):
        cName = self.ui.cNameEdit.text().strip()
        flag = sale_controller.query_inventory(cName)
        if flag is None:
            QMessageBox.warning(self.ui, "警告", "LinkError：数据库连接失败！")
            return False
        if flag == False:
            QMessageBox.warning(self.ui, "警告", "QueryError：查询失败！请联系开发人员！")
            return False
        self.ui.tableWidget.setRowCount(len(flag))
        for i in range(len(flag)):
            cID = QTableWidgetItem(str(flag[i][0]))
            cName = QTableWidgetItem(flag[i][1])
            cQuantity = QTableWidgetItem(str(flag[i][2]))
            cMeasure = QTableWidgetItem(flag[i][3])
            cPrice = QTableWidgetItem(str(flag[i][4]))
            self.ui.tableWidget.setItem(i, 0, cID)
            self.ui.tableWidget.setItem(i, 1, cName)
            self.ui.tableWidget.setItem(i, 2, cQuantity)
            self.ui.tableWidget.setItem(i, 3, cMeasure)
            self.ui.tableWidget.setItem(i, 4, cPrice)

    def sale(self):
        cName = self.ui.cNameEdit.text().strip()
        cQuantity = self.ui.cQuantityEdit.text().strip()
        cPrice = self.ui.cPriceEdit.text().strip()
        if cName == "" or cQuantity == "" or cPrice == "":
            QMessageBox.warning(self.ui, "警告", "InputError2：输入不能为空！")
            return False
        try:
            cQuantity = float(cQuantity)
            cPrice = float(cPrice)
        except ValueError:
            QMessageBox.warning(self.ui, "警告", "InputError1：价格和数量必须为数字！")
            return False
        flag = sale_controller.query_inventory(cName)
        if flag is None:
            QMessageBox.warning(self.ui, "警告", "LinkError：数据库连接失败！")
            return False
        for i in range(len(flag)):
            if flag[i][1] == cName:
                if cQuantity > flag[i][2]:
                    QMessageBox.warning(self.ui, "警告", "InputError4：库存不足！请重新输入数量！")
                    return False
                else:
                    cID = flag[i][0]
                    flag2 = sale_controller.sale(cID, cQuantity, cPrice, self.sID)
                    if flag2:
                        QMessageBox.information(self.ui, "提示", "销售成功")
                        self.refresh()
                    elif flag2 == False:
                        QMessageBox.warning(self.ui, "警告", "QueryError：销售失败！请联系开发人员！")
                        return False
                    elif flag2 is None:
                        QMessageBox.warning(self.ui, "警告", "LinkError：数据库连接失败！")
                    return False
            else:
                QMessageBox.warning(self.ui, "警告", "InputError2：商品不存在！请输入完整商品名称！")
                return False

    def query(self):
        global newWindow
        newWindow = sale_query_ui.SaleQueryUI(self.sID)
        newWindow.ui.show()
        self.ui.close()

    def exit(self):
        self.ui.close()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    window = SaleUI()
    window.ui.show()
    app.exec()
