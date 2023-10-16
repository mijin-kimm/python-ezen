import pymysql

class Mysql:
    # 생성자 함수 : class가 생성될때 최초로 한번만 실행이 되는 함수를 의미한다. 초기화 함수라고 부르기도 한다.
    def __init__(self, _host, _user, _pass, _db, _port):
        self.host = _host
        self.user = _user
        self.password = _pass
        self.db = _db
        self.port = _port

    # sql 쿼리문을 입력 값으로 받아서 쿼리문을 실행하고 결과값을 되돌려주는 함수
    def sql_load(self, _sql, _value= []):
        # 데이터베이스 서버와의 연결
        _db = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.db,
            port = self.port
        )
        # Cursor 생성
        cursor = _db.cursor(pymysql.cursors.DictCursor)

        # sql 쿼리문을 실행
        cursor.execute(_sql, _value)

        # _sql이 시작이 select로 시작하는 경우
        if _sql.strip().lower().startswith('select'):
            result = cursor.fetchall()
        # 아닌 경우
        else:
            _db.commit()
            result = 'Query OK'

        # 데이터베이스와의 연결을 종료
        _db.close()

        return result