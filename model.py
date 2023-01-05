"""ISMS model module"""

import pyodbc


# 建立数据库连接#########################################
def get_db():
    """Get database connection"""
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=DESKTOP-JM2MPRQ;DATABASE=ISMS;UID=sa;PWD=123456')
        cur = conn.cursor()
        return conn, cur
    except pyodbc.Error as err:
        print(err)
        return None, None


# 系统管理###############################################
def query_userTable(uID):
    """use uID to query userTable"""
    conn, cur = get_db()
    if conn is None:
        return False
    sql = '''
        SELECT * FROM userTable
        WHERE uID = %s
    ''' % uID
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result


def write_log(uID):
    """Write log"""
    conn, cur = get_db()
    if conn is None:
        return None
    sql = '''
        INSERT INTO loginLog(uID)
        VALUES (%s)
    ''' % uID
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_salesmanID(uID):
    """Get salesmanID"""
    conn, cur = get_db()
    if conn is None:
        return None
    sql = '''
        SELECT sID FROM salesmanTable where uID = %s
    ''' % uID
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


def get_purchaserID(uID):
    """Get purchaserID"""
    conn, cur = get_db()
    if conn is None:
        return None
    sql = '''
        SELECT pID FROM purchaserTable where uID = %s
    ''' % uID
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


def get_keeperID(uID):
    """Get keeperID"""
    conn, cur = get_db()
    if conn is None:
        return None
    sql = '''
        SELECT kID FROM keeperTable where uID = %s
    ''' % uID
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


def change_pwd(uID, new_pwd):
    """Change password"""
    conn, cur = get_db()
    if conn is None:
        return None
    try:
        sql = '''
            UPDATE userTable
            SET uPwd = %s
            WHERE uID = %s
        ''' % (new_pwd, uID)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as err:
        print(err)
        return False


# 采购管理###############################################
def insert_purchaseOrder(pID, cName, sName, pUnitPrice, pQuantity, pMeasuringUint):
    """Insert purchaseOrder"""
    conn, cur = get_db()
    if conn is None:
        return None
    try:
        sql = """
            INSERT INTO purchaseOrder(pID, cName, sName, pUnitPrice, pQuantity, pMeasuringUnit)
            VALUES (%s, \'%s\', \'%s\', %s, %s, \'%s\')
        """ % (pID, cName, sName, pUnitPrice, pQuantity, pMeasuringUint)
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as err:
        print(err)
        return False


def query_purchaseOrder(params: dict):
    """Query purchaseOrder"""
    conn, cur = get_db()
    if conn is None:
        return None
    where_clause = ' WHERE'
    for k, v in params.items():
        if k in ['pID', 'poID', 'isInWarehouse']:
            where_clause += ' {} = {} AND'.format(k, v)
        elif k in ['cName', 'sName']:
            where_clause += ' {} LIKE \'%{}%\' AND'.format(k, v)
    if params.get('startDateTime'):
        where_clause += ' poDatetime BETWEEN \'{}\' AND \'{}\''.format(params['startDateTime'], params['endDateTime'])
    else:
        where_clause = where_clause[:-3]
    sql = "SELECT * FROM purchaseOrder" + where_clause
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


# 入库管理###############################################
def check_purchaseOrder(poID, checkNum, kid):
    """Check purchaseOrder"""
    conn, cur = get_db()
    if conn is None:
        return None
    try:
        sql = """
            Insert into [warehouse-inRecords](poID, pQuantityReal, kID)
            VALUES (%s, %s, %s)
        """ % (poID, checkNum, kid)
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as err:
        print(err)
        return False


def query_warehouseDetail(params: dict):
    """Query warehouseDetail"""
    conn, cur = get_db()
    if conn is None:
        return None
    where_clause = ' WHERE'
    for k, v in params.items():
        if k in ['kID', 'wrID']:
            where_clause += ' {} = {} AND'.format(k, v)
        elif k in ['cName']:
            where_clause += ' {} LIKE \'%{}%\' AND'.format(k, v)
    if params.get('startDateTime'):
        where_clause += ' wrDatetime BETWEEN \'{}\' AND \'{}\''.format(params['startDateTime'], params['endDateTime'])
    else:
        where_clause = where_clause[:-3]
    sql = "SELECT wrID,kID,po.poID,cName,pQuantityReal,pMeasuringUnit,wrDatetime FROM [warehouse-inRecords] wr " \
          + "join purchaseOrder po on wr.poID = po.poID" \
          + where_clause
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


# 销售管理###############################################
def query_inventory(cName: str):
    """Query inventory"""
    conn, cur = get_db()
    if conn is None:
        return None
    try:
        sql = "SELECT cID,pO.cName,cQuantity,pMeasuringUnit,pUnitPrice FROM inventoryTable " \
              "join purchaseOrder pO on inventoryTable.cName = pO.cName " \
              "WHERE pO.cName LIKE \'%{}%\' AND cQuantity > 0".format(cName)
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()
        return result
    except pyodbc.Error as err:
        print(err)
        return False


def sale(cID: int, cQuantity: float, cPrice: float, sID: int):
    """Sale"""
    conn, cur = get_db()
    if conn is None:
        return None
    try:
        sql = """INSERT INTO salesRecords(sID, cID, srQuantity, srUnitPrice) 
                 values (%d, %d, %f, %f)""" % (sID, cID, cQuantity, cPrice)
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as err:
        print(err)
        return False


def query_sale(params: dict):
    """Query sale"""
    conn, cur = get_db()
    if conn is None:
        return None
    where_clause = ' WHERE'
    for k, v in params.items():
        if k in ['sID', 'srID']:
            where_clause += ' {} = {} AND'.format(k, v)
        elif k in ['cName']:
            where_clause += ' {} LIKE \'%{}%\' AND'.format(k, v)
    if params.get('startDateTime'):
        where_clause += ' salesDatetime BETWEEN \'{}\' AND \'{}\''.format(params['startDateTime'], params['endDateTime'])
    else:
        where_clause = where_clause[:-3]
    sql = "SELECT srID,sID,salesDatetime,iT.cID,cName,srQuantity,srUnitPrice FROM salesRecords " \
          + "join inventoryTable iT on iT.cID = salesRecords.cID" + where_clause
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result
