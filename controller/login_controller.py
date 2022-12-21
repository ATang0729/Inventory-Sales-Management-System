"""登录模块控制器"""
import model


def login(userid, password):
    """登录验证"""
    userinfo = model.query_userTable(userid)
    if userinfo is None:
        return False, "LoginError1"
    elif userinfo[2] != password:
        return False, "LoginError2"
    elif userinfo == False:
        return False, "LinkError"
    else:
        model.write_log(userid)
        uName = userinfo[1]
        uType = userinfo[3]
        return True, (uName, uType)

def get_roleID(userid, uType):
    """获取角色ID"""
    if uType == "销售员":
        salesmanID = model.get_salesmanID(userid)
        return True, uType, salesmanID
    elif uType == "采购员":
        purchaserID = model.get_purchaserID(userid)
        return True, uType, purchaserID
    elif uType == "仓管员":
        keeperID = model.get_keeperID(userid)
        return True, uType, keeperID
