from db_query import insert_chung,insert_ulsan
import time 


def insert():
    device_num = int(input("충무로:0 // 울산:1 선택하세요. ")) # device 고르기 충무로는 0 // 울산은 1
    if device_num ==0:
        # 재귀함수로 계측기 멈췄을 때 다시 실행하도록..
        insert_chung()
        time.sleep(600) # data입력 안되고있으면 10분 기다렸다가 다시 실행하기
        print("**************ReStart****************")
        insert()

    elif device_num ==1:
        insert_ulsan()
        time.sleep(600)
        print("***********ReStart************")
        insert()

if __name__ == '__main__':
    insert()