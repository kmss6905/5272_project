import db_conn # db_conn.py 불러오기
import pymysql
from time import time

# 유저의 계측기 정보들을 가져옵니다.
def get_data():
    conn = db_conn.get_connection()
    sql ='SELECT CAST(UNIX_TIMESTAMP(Create_time)/3600 AS SIGNED) ,FROM_UNIXTIME(CAST(UNIX_TIMESTAMP(Create_time)/3600 AS SIGNED)*3600) AS tDate ,COUNT(*) cnt, AVG(Longitude), AVG(Latitude), AVG(Height), device_id FROM rawdata_ulsan WHERE Create_time BETWEEN "2021-04-29 15:15:00" AND "2021-04-30 23:59:59" AND device_id=2214 GROUP BY 1'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    print(rows)
    return rows


if __name__ == "__main__":
    get_data()