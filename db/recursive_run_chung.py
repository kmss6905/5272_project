from db_query import insert_chung
import time 


def insert():
    # 재귀함수로 계측기 멈췄을 때 다시 실행하도록..
    try:
        insert_chung()
        insert()
    except:
        time.sleep(3000) # data입력 안되고있으면 30분 기다렸다가 다시 실행하기
        print("**************ReStart****************")
        insert()


if __name__ == '__main__':
    insert()