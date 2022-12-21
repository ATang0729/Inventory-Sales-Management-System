"""采购订单明细查询界面"""

from controller import order_query_controller
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from view import order_ui


class QueryPurchaseUI:
    def __init__(self, purchaserID):
        self.ui = QUiLoader().load('view/order_query.ui')
        self.purchaserID = purchaserID
