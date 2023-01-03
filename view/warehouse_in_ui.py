"""商品入库核算界面"""

from controller import warehouse_controller
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate


newWindow = None


class WarehouseUI:
    def __init__(self, keeperid):
        self.ui = QUiLoader().load('ui/warehouse.ui')
        self.keeperid = keeperid

        current_date = QDate.currentDate().addDays(1)
        self.ui.dateTimeEdit_2.setDate(current_date)

        self.ui.queryButton.clicked.connect(self.query)

        self.ui.checkButton.clicked.connect(self.check)
        self.ui.queryButton_2.clicked.connect(self.query_2)
        self.ui.exitButton.clicked.connect(self.exit)

        self.query()

    def query(self):
        poID = self.ui.poIDEdit.text().strip()
        pID = self.ui.pIDEdit.text().strip()
        cName = self.ui.cNameEdit.text().strip()
        sName = self.ui.sNameEdit.text().strip()
        startDateTime = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        endDateTime = self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        params = {'isInWarehouse': 0, 'startDateTime': startDateTime, 'endDateTime': endDateTime}
        if poID != "":
            params['poID'] = poID
        if pID != "":
            params['pID'] = pID
        if cName != "":
            params['cName'] = cName
        if sName != "":
            params['sName'] = sName
        flag = warehouse_controller.query_purchaseOrder(params)
        if flag is None:
            QMessageBox.information(self.ui, "提示", "LinkError：数据库连接失败！")
            return False
        else:
            self.ui.tableWidget.setRowCount(len(flag))
            for i in range(len(flag)):
                poID = QTableWidgetItem(str(flag[i][0]))
                pID = QTableWidgetItem(str(flag[i][1]))
                cName = QTableWidgetItem(str(flag[i][2]))
                sName = QTableWidgetItem(str(flag[i][3]))
                unit = QTableWidgetItem(str(flag[i][6]))
                datetime = QTableWidgetItem(str(flag[i][7]))
                self.ui.tableWidget.setItem(i, 0, poID)
                self.ui.tableWidget.setItem(i, 1, pID)
                self.ui.tableWidget.setItem(i, 2, cName)
                self.ui.tableWidget.setItem(i, 3, sName)
                self.ui.tableWidget.setItem(i, 4, unit)
                self.ui.tableWidget.setItem(i, 5, datetime)
            return True

    def check(self):
        pass

    def query_2(self):
        pass

    def exit(self):
        self.ui.close()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = WarehouseUI(1)
    window.ui.show()
    app.exec()


