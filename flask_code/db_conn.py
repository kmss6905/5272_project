import pymysql

def get_connection():
    conn = pymysql.connect(host='localhost', user='root', password='tlsjfprtm', db='test', charset='utf8')
    return conn