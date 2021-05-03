# app.py
from flask import Flask, render_template

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
  return render_template('index.html')
  # jinja2템플릿 엔진을 통해 데이터 값들을 index.html에 표현될 수 있다.

if __name__=="__main__":
  app.run(host="211.62.179.66", port=3000, debug=True)
