# flask 라이브러리 로드
from flask import Flask, render_template

# Flask class 생성
# 해당 class에는 생성자함수 존재
# 입력값으로 파일의 이름
# __name__ : 현재 파일의 이름
app = Flask(__name__)

# 포트번호 설정
_port = 3000

# api 생성
# localhost:3000

# 네비게이터 함수
# localhost:3000/ 요청 시 바로 아래의 함수를 호출
@app.route("/")
def index():
    return render_template('index.html')

# localhost:3000/second 요청 시
@app.route("/second")
def second():
    return render_template('second.html')




app.run(port = _port, debug=True)
# 디버그의 디폴트는 false로 놓자. 실서버에서 바로 재실행되면 유저들이 에러를 겪게 됨.