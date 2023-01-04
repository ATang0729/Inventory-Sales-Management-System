"""入库明细查询控制器"""

import model


def query_warehouseDetail(params: dict):
    flag = model.query_warehouseDetail(params)
    return flag
