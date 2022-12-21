"""主程序模块控制器"""
import model


def get_roleID(uID, uType):
    if uType == "销售员":
        salesmanID = model.get_salesmanID(uID)
        return salesmanID
    elif uType == "采购员":
        purchaserID = model.get_purchaserID(uID)
        return purchaserID
    elif uType == "仓管员":
        keeperID = model.get_keeperID(uID)
        return keeperID

