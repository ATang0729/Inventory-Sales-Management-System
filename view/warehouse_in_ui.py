"""商品入库核算界面"""

from controller import warehouse_controller
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader

newWindow = None


class WarehouseUI:
    def __init__(self, warehouseID):
        self.ui = QUiLoader().load('view/ui/warehouse.ui')
        self.warehouseID = warehouseID
        self.ui.inButton.clicked.connect(self.inWarehouse)
        self.ui.outButton.clicked.connect(self.outWarehouse)
        self.ui.queryButton.clicked.connect(self.query)
        self.ui.exitButton.clicked.connect(self.exit)
