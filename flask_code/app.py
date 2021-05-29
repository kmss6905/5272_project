from flask import Flask, render_template, request, flash, redirect, url_for, session, g



# Flask 객체 인스턴스 생성
from flask_code.device_data_dao import each_device_info
from flask_code.model.user import User
from flask_code.repo.user_repo import *  # USER repository
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'  # 세션을 이용한 로그인 시스템을 만들기위해서 필요함

# 모든 요청에 로그인 유무를 확인하여 글로벌 객체에 유저정보를 넣습니다. 앞으로 g.user <-- 에 접근하여 유저정보를 가져오시면 됩니다.
@app.before_request
def before_request():
    print(session)
    if 'user_id' in session:
        user_dao = get_user_by_id(session['user_id'])
        user_dto = User(user_dao)  # 우리가 사용하는 User 객체 (여기는 패스워드가 빠져있다)
        g.user = user_dto


# 로그인 기능
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            username = request.form['username']  # 클라이언트로 부터 받아온 유저아이디
            password = request.form['password']  # 패스워트

            # 잘못된 아이디
            user = get_user_by_user_nickname(username)  # 유저를 가져옵니다.
            if not get_user_by_user_nickname(username):  # 유저가 없다면
                flash("존재하지 않는 유저입니다")
                return redirect(url_for('login'))  # 다시 로그인 페이지로 이동

            # 잘못된 비밀번호
            if user and user['user_password'] != password:
                flash("잘못된 패스워드 입니다")
                return redirect(url_for('login'))  # 다시 로그인 페이지로 이동

            # 로그인 성공
            if user and user['user_password'] == password:
                session['user_id'] = user['id']  # user_id : 1 (로그인 유저의 고유의 아이디값 추가)
                return redirect(url_for('index'))  # dashboard_building 페이지로 이동
        return render_template('signin.html')


# 건물대시보드
@app.route('/index')
def index():
    if 'user_id' in session:
        return render_template('building_dashboard.html')  # 로그인 했다면 해당 페이지 반환
    else:
        return render_template('building_dashboard_all.html')  # 로그인 하지 않았다면 해당 페이지로 이동합니다.


# 특정 건물 정보
@app.route('/building')
def building_page():
    return render_template('building_page.html')


# 개별 계측기 정보
@app.route('/device')
def devices():
    device_info = each_device_info('syntest1')
    return render_template('device.html', device_info=device_info)


# 계측기 등록
@app.route('/register')
def register_device():
    return render_template('register_form.html')


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)