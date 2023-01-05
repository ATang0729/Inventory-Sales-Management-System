"""销售明细查询界面"""

from view import sale_ui
from controller import sale_query_controller
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import QDate
from PySide6.QtUiTools import QUiLoader

newWindow = None


class SaleQueryUI:
    def __init__(self, sID):
        load = QUiLoader().load('view/ui/sale_query.ui')
        self.sID = sID
        self.ui = load

        self.ui.saleButton.clicked.connect(self.sale)
        self.ui.queryButton.clicked.connect(self.query)
        self.ui.exitButton.clicked.connect(self.exit)

        currentDate = QDate.currentDate().addDays(1)
        self.ui.dateTimeEdit_2.setDate(currentDate)

        self.query()

    def query(self):
        srID = self.ui.srIDEdit.text().strip()
        sID = self.ui.sIDEdit.text().strip()
        cName = self.ui.cNameEdit.text().strip()
        startDateTime = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        endDateTime = self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        params = {'startDateTime': startDateTime,
                  'endDateTime': endDateTime}
        if startDateTime > endDateTime:
            QMessageBox.information(self.ui, "提示", "InputError6：开始时间不能大于结束时间！")
            return False
        if srID != "":
            params['srID'] = srID
        if sID != "":
            params['sID'] = sID
        if cName != "":
            params['cName'] = cName
        flag = sale_query_controller.query_sale(params)
        if flag is None:
            QMessageBox.warning(self.ui, "警告", "LinkError：数据库连接失败！")
            return False
        if flag == False:
            QMessageBox.warning(self.ui, "警告", "QueryError：查询失败！请联系开发人员！")
            return False
        self.ui.tableWidget.setRowCount(len(flag))
        for i in range(len(flag)):
            srID = QTableWidgetItem(str(flag[i][0]))
            sID = QTableWidgetItem(str(flag[i][1]))
            salesDateTime = QTableWidgetItem(str(flag[i][2]))
            cID = QTableWidgetItem(str(flag[i][3]))
            cName = QTableWidgetItem(str(flag[i][4]))
            srQuantity = QTableWidgetItem(str(flag[i][5]))
            srUnitPrice = QTableWidgetItem(str(flag[i][6]))
            self.ui.tableWidget.setItem(i, 0, srID)
            self.ui.tableWidget.setItem(i, 1, sID)
            self.ui.tableWidget.setItem(i, 2, salesDateTime)
            self.ui.tableWidget.setItem(i, 3, cID)
            self.ui.tableWidget.setItem(i, 4, cName)
            self.ui.tableWidget.setItem(i, 5, srQuantity)
            self.ui.tableWidget.setItem(i, 6, srUnitPrice)
        return True

    def sale(self):
        global newWindow
        newWindow = sale_ui.SaleUI(self.sID)
        newWindow.ui.show()
        self.ui.close()

    def exit(self):
        self.ui.close()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = SaleQueryUI(1)
    window.ui.show()
    app.exec()
