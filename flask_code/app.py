import os
from flask import Flask, render_template, make_response, request, session, redirect, url_for, escape
from flask_login import LoginManager, login_user
from Model.User import User

from form import LoginForm
import json
import chung_dao
import device_list_dao
from device_data_dao import (get_data,get_device_list,get_all_device,get_my_device
                            ,all_device_info,each_device_building,each_device_info,register_my_device)
from building_data_dao import (get_all_building, get_user_building,get_my_building_info_map,get_my_building_info_table
                                ,decide_criteria)
from box_plot import box_plot,each_plot,plot
import random


# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.urandom(24) # 코드는 사용자 세션 관리를 할 때 필요한 정보입니다.


login_manager = LoginManager()
login_manager.init_app(app)


# 전역으로 우선 설정합니다.(나중에는 DB와 연동하겠습니다)
USERS = {
    "kmss69052@naver.com": User("kmss69052@naver.com", passwd_hash='123'),
    "admin@naver.com": User("admin@naver.com", passwd_hash='123'),
    "admin2@naver.com": User("admin2@naver.com", passwd_hash='123'),
}


# 로그인 객체 가져올 때 사용 ( user_email 로 해당 사용자 객체 가져옴 )
@login_manager.user_loader
def user_loader(user_email):
    return USERS[user_email]

# @app.route('/')
# def index():
#     device_list = device_list_dao.get_device_list()
#     return render_template('index.html', device_list=device_list)


# 주석에 있는 부분 참고할 게 있어서 지우지 않았습니다! 나중에 지울예정
# @app.route('/info', methods=['GET'])
# def get_data():
#     data = device_data_dao.get_data()
#     print(data)
#     response = make_response(json.dumps(data))
#     response.content_type = 'application/json'
#     return response

#
# @app.route('/live-data')
# def live_data():
#     content_list = chung_dao.get_chung()
#     response = make_response(json.dumps(content_list))
#     response.content_type = 'application/json'
#     return response  # {a:1500.000,
#     #   b: 1235.232525)


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return



# 로그인
@app.route('/signin')
def signin():
    return render_template('signin.html')

# 로그인
@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('building_dashboard')) # 로그인 했을 경우는 해당 페이지로 이동

    user_email = request.json['user_email']
    passwd_hash = request.json['passwd_hash']
    if user_email not in USERS:
        json_res = {'ok': False, 'error': 'Invalid user_id or password'}
    elif not USERS[user_email].can_login(passwd_hash):
        json_res = {'ok': False, 'error': 'Invalid user_id or password'}
    else:
        json_res = {'ok': True, 'msg': 'user <%s> logined' % user_email}
        USERS[user_email].authenticated = True
        # User 인스턴스를 current_user 에 등록
        login_user(USERS[user_email], remember=True)
        session['username'] = user_email # session 등록
    return user_email(json_res)






# 건물대시보드 (로그인x 전체사용자정보_전체적)
@app.route('/building_dashboard_all')
def dashboard_all():
    return render_template('building_dashboard_all.html')

# 건물대시보드 (로그인o_전체적)
@app.route('/building_dashboard')
def building_dashboard():
    return render_template('building_dashboard.html')


#특정 건물 정보
@app.route('/building')
def building_page():
    return render_template('building_page.html')


# 개별 계측기 정보
@app.route('/device')
def devices():
    # device_name = request.args['info']
    # data_list = device_data_dao.get_data()
    # device_list = device_list_dao.get_device_list()
    # return render_template('devices.html', device_name=device_name, data_list=data_list, device_list=device_list)
    return render_template('device.html')


# 계측기 등록
@app.route('/register')
def register_device():
    return render_template('register_form.html')

# print(get_all_building()) #
# print(get_user_building('1')) # 1에다가 로그인 시 여기에 user_id변수를 넣어주면 된다
# print(get_my_building_info('1')) 
# print(get_my_device('1'))
# print(get_my_building_info_table('1','충무로영상센터')) # 충무로영상센터에 찾고싶은 building_name을 넣어주면 된다. 
# print(decide_criteria(1,'충무로영상센터')) # 한 건축물의 모든 계측기 이상범위 기준// 일단 기준만 받아오고 이상측정을 실시간으로 할지 결정해야할듯
# print(all_device_info()) 
# device_id_list = each_device_building(1,'충무로영상센터') # 빌딩이름에 해당하는 계측기의 device_id가 나온다. 
# each_device_info(device_id_list[0]['device_id']) # 이렇게 하면 선택한 계측기의 정보데이터를 받아올 수 있다. 
# print(plot('syntest1',6))
# register_my_device(2,'춘천빌딩1',4,'강원도 춘천시 33','test','chuncheon1','36.123/126.123/44.123') # register페이지의 폼에 데이터 입력하면 인자에 해당 데이터변수가 입력되고 db에 insert된다

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
