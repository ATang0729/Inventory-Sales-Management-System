"""入库单明细查询界面"""

from controller import warehouse_query_controller
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate
from view import warehouse_in_ui


newWindow = None


class QueryWarehouseUI:
    def __init__(self, keeperid):
        load = QUiLoader().load('view/ui/warehouse_query.ui')
        self.ui = load
        self.kid = keeperid

        self.ui.checkButton.clicked.connect(self.check)
        self.ui.queryButton.clicked.connect(self.query)
        self.ui.exitButton.clicked.connect(self.exit)

        currentDate = QDate.currentDate().addDays(1)
        self.ui.dateTimeEdit_2.setDate(currentDate)

        self.query()

    def check(self):
        global newWindow
        newWindow = warehouse_in_ui.WarehouseUI(self.kid)
        newWindow.ui.show()
        self.ui.close()

    def query(self):
        wrID = self.ui.wrIDEdit.text().strip()
        kID = self.ui.kIDEdit.text().strip()
        cName = self.ui.cNameEdit.text().strip()
        startDateTime = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        endDateTime = self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if startDateTime > endDateTime:
            QMessageBox.information(self.ui, "提示", "InputError6：开始时间不能大于结束时间！")
            return False
        for i in (wrID, kID):
            if i != "":
                try:
                    int(i)
                except ValueError:
                    QMessageBox.information(self.ui, "提示", "InputError1：输入的ID必须为数字！")
                    return False
        params = {'startDateTime': startDateTime, 'endDateTime': endDateTime}
        if wrID != "":
            params['wrID'] = wrID
        if kID != "":
            params['kID'] = kID
        if cName != "":
            params['cName'] = cName
        flag = warehouse_query_controller.query_warehouseDetail(params)
        if flag is None:
            QMessageBox.information(self.ui, "提示", "LinkError：数据库连接失败！")
            return False
        else:
            self.ui.tableWidget.setRowCount(len(flag))
            for i in range(len(flag)):
                wrID = QTableWidgetItem(str(flag[i][0]))
                kID = QTableWidgetItem(str(flag[i][1]))
                poID = QTableWidgetItem(str(flag[i][2]))
                cName = QTableWidgetItem(str(flag[i][3]))
                pQuantity = QTableWidgetItem(str(flag[i][4]))
                pMeasuringUnit = QTableWidgetItem(str(flag[i][5]))
                wrDatetime = QTableWidgetItem(str(flag[i][6]))
                self.ui.tableWidget.setItem(i, 0, wrID)
                self.ui.tableWidget.setItem(i, 1, kID)
                self.ui.tableWidget.setItem(i, 2, poID)
                self.ui.tableWidget.setItem(i, 3, cName)
                self.ui.tableWidget.setItem(i, 4, pQuantity)
                self.ui.tableWidget.setItem(i, 5, pMeasuringUnit)
                self.ui.tableWidget.setItem(i, 6, wrDatetime)

    def exit(self):
        self.ui.close()


if __name__== '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = QueryWarehouseUI(1)
    window.ui.show()
    app.exec()