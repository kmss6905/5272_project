import pymysql
from flask_code.db_conn import get_connection


# 닉네임을 통해 유저데이터를 값을 반환받습니다.
def get_user_by_user_nickname(nickname):
    conn = get_connection()
    sql = "select * from user where user_nickname=%s"
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, nickname)
    user = cursor.fetchone()
    conn.close()
    return user

# 유저고유아이디를 통해 유저데이터를 반환받습니다.
def get_user_by_id(id):
    conn = get_connection()
    sql = "select * from user where id=%s"
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, id)
    user = cursor.fetchone()
    conn.close()
    return user





