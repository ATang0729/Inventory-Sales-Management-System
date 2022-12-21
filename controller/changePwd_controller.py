"""密码修改控制器"""
import model


def query_pwd(uID, password):
    """查询密码"""
    userinfo = model.query_userTable(uID)
    if userinfo[2] == password:
        return True
    else:
        return False

def changePwd(uID, newPwd):
    """修改密码"""
    flag = model.change_pwd(uID, newPwd)
    return flag

