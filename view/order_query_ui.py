"""采购订单明细查询界面"""

from controller import order_query_controller
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate
from view import order_ui

newWindow = None


class QueryPurchaseUI:
    def __init__(self, purchaserID):
        self.ui = QUiLoader().load('view/order_query.ui')
        self.purchaserID = purchaserID
        self.ui.pIDEdit.setText(self.purchaserID)

        currentDate = QDate.currentDate()
        self.ui.dateTimeEdit_2.setDate(currentDate)

        self.ui.orderButton.clicked.connect(self.order)
        self.ui.queryButton.clicked.connect(self.query)
        self.ui.exitButton.clicked.connect(self.exit)

        self.query()

    def order(self):
        global newWindow
        newWindow = order_ui.OrderUI(self.purchaserID)
        newWindow.ui.show()
        self.ui.close()

    def query(self):
        # 采购单编号
        poID = self.ui.poIDEdit.text().strip()
        # 采购员编号
        pID = self.ui.pIDEdit.text().strip()
        # 供应商名称
        sName = self.ui.sNameEdit.text().strip()
        # 商品名称
        cName = self.ui.cNameEdit.text().strip()
        # 起始日期时间
        startDateTime = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        # 终止日期时间
        endDateTime = self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        params = {'startDateTime': startDateTime, 'endDateTime': endDateTime}
        if poID != "":
            params['poID'] = poID
        if pID != "":
            params['pID'] = pID
        if sName != "":
            params['sName'] = sName
        if cName != "":
            params['cName'] = cName
        flag = order_query_controller.query_purchaseOrder(params)
        if flag is None:
            QMessageBox.information(self.ui, "提示", "LinkError：数据库连接失败！")
            return False
        else:
            pass

    def exit(self):
        self.ui.close()
