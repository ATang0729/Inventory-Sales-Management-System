"""销售出库控制器"""

import model


def query_inventory(cName: str):
    flag = model.query_inventory(cName)
    return flag


def sale(cID, cQuantity, cPrice, sID):
    flag = model.sale(cID, cQuantity, cPrice, sID)
    return flag
