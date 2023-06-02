import sqlite3

def get_anniv(aid):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'select * from anniversary where aid=?'
    cur.execute(sql, (aid,))
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row

def get_anniv_list(sdate, edate, uid):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    if uid == 'admin':
        sql = "select * from anniversary where adate between ? and ? and uid=?"
    else:
        sql = "select * from anniversary where adate between ? and ? and (uid='admin' or uid=?)"
    cur.execute(sql, (sdate, edate, uid))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def insert_anniv(params):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'insert into anniversary(aname, adate, is_holiday, uid) values(?, ?, ?, ?)'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def insert_anniv_many(params):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'insert into anniversary(aname, adate, is_holiday, uid) values(?, ?, ?, ?)'
    cur.executemany(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def update_anniv(params):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'update anniversary set aname=?, adate=?, is_holiday=? where aid=?'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def delete_anniv(aid):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'delete from anniversary where aid=?'
    cur.execute(sql, (aid,))
    conn.commit()

    cur.close()
    conn.close()