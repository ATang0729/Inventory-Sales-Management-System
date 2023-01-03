'''order query controller'''

import model


def query_purchaseOrder(params: dict):
    flag = model.query_purchaseOrder(params)
    return flag
