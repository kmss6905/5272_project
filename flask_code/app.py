from flask import Flask, render_template, make_response, request
import json
import chung_dao
import device_list_dao
import device_data_dao
import random

# Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route('/')
def index():
    device_list = device_list_dao.get_device_list()
    return render_template('index.html', device_list=device_list)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/password')
def password():
    return render_template('password.html')


@app.route('/401')
def f_401():
    return render_template('401.html')


@app.route('/404')
def f_404():
    return render_template('404.html')


@app.route('/500')
def f_500():
    return render_template('500.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')


@app.route('/safe-detail')
def safe_detail():
    return render_template('safe-detail.html')


@app.route('/warning-detail')
def warning_detail():
    return render_template('warning-detail.html')


@app.route('/danger-detail')
def danger_detail():
    return render_template('danger-detail.html')


@app.route('/all-detail')
def all_detail():
    return render_template('all-detail.html')


@app.route('/layout-static')
def layout_static():
    return render_template('layout-static.html')


@app.route('/layout-sidenav-light')
def layout_sidenav_light():
    return render_template('layout-sidenav-light.html')


@app.route('/live-graph')
def graph():
    return render_template('live-graph.html')


@app.route('/devices', methods=['GET'])
def devices():
    device_name = request.args['info']
    data_list = device_data_dao.get_data()
    device_list = device_list_dao.get_device_list()
    return render_template('devices.html', device_name=device_name, data_list=data_list, device_list=device_list)


@app.route('/info', methods=['GET'])
def get_data():
    data = device_data_dao.get_data()
    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/live-data')
def live_data():
    content_list = chung_dao.get_chung()
    response = make_response(json.dumps(content_list))
    response.content_type = 'application/json'
    return response  # {a:1500.000,
    #   b: 1235.232525}


@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
