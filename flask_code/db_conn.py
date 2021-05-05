import pymysql

def get_connection():
    conn = pymysql.connect(host='211.62.179.66', user='root', password='tlsjfprtm', db='test', charset='utf8')
    return conn