"""商品入库核算控制器"""

import model


def query_purchaseOrder(params: dict):
    flag = model.query_purchaseOrder(params)
    return flag
