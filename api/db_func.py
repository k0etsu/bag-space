def add_item(db_conn, data):
    db_cur = db_conn.cursor()
    sql = """insert into items (name, category, stock, notes)
    values(%s, %s, %s, %s)"""
    db_cur.execute(sql, (data["name"], data["category"], data["stock"], data["notes"]))
    db_conn.commit()
    db_cur.close()
    return 200


def get_items(db_conn):
    db_cur = db_conn.cursor()
    sql = """select * from items order by id"""
    db_cur.execute(sql)
    data = db_cur.fetchall()
    db_cur.close()
    return data


def delete_item(db_conn, data):
    db_cur = db_conn.cursor()
    sql = """delete from items where id = %s"""
    db_cur.execute(sql, (data["id"],))
    db_conn.commit()
    db_cur.close()
    return 200


def update_item(db_conn, data):
    db_cur = db_conn.cursor()
    sql = """update items set name = %s, category = %s, stock = %s, notes = %s where id = %s"""
    db_cur.execute(sql, (data["name"], data["category"], data["stock"], data["notes"], data["id"]))
    db_conn.commit()
    db_cur.close()
    return 200


def inc_stock(db_conn, data):
    db_cur = db_conn.cursor()
    sql = """update items set stock = stock+1 where id = %s"""
    db_cur.execute(sql, (data["id"],))
    db_conn.commit()
    db_cur.close()
    return 200


def dec_stock(db_conn, data):
    db_cur = db_conn.cursor()
    sql = """update items set stock = stock-1 where id = %s"""
    db_cur.execute(sql, (data["id"],))
    db_conn.commit()
    db_cur.close()
    return 200
