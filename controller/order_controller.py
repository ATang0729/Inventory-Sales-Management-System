"""采购订单下达控制器"""

import model


def order(purchaserID, cName, sName, price, num, measure):
    """下达订单"""
    flag = model.insert_purchaseOrder(purchaserID, cName, sName, price, num, measure)
    return flag
