"""销售明细查询控制器"""

import model


def query_sale(params: dict):
    flag = model.query_sale(params)
    return flag
