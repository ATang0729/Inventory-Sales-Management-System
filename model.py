"""ISMS model module"""

import pyodbc


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
    '''
    cur.execute(sql, uID)
    conn.commit()
    conn.close()


def get_salesmanID(uID):
    """Get salesmanID"""
    conn, cur = get_db()
    if conn is None:
        return None
    sql = '''
        SELECT sID FROM salesmanTable where uID = %s
    '''
    cur.execute(sql, uID)
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
    '''
    cur.execute(sql, uID)
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
    '''
    cur.execute(sql, uID)
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
    except pymssql.Error as err:
        print(err)
        return False


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
    except pymssql.Error as err:
        print(err)
        return False


def query_purchaseOrder(params: dict):
    """Query purchaseOrder"""
    conn, cur = get_db()
    if conn is None:
        return None
    where_clause = ' WHERE'
    for k, v in params.items():
        where_clause += ' {} = {} AND'.format(k, v)
    where_clause = where_clause[:-4]
    sql = "SELECT * FROM purchaseOrder" + where_clause
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result
