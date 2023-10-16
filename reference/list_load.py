import os
import pandas as pd

# 특정 경로에 있는 파일 목록을 하나의 데이터프레임으로 결합하는 함수 생성
def list_load(_path, _end) :
        # _path : 파일의 경로
        # _end : 파일의 확장자

        # _path의 마지막 문자열이 '/' 가 아니라면?
        # if not(_path.endswith('/')):
        if _path[-1] !='/':
               _path = _path + '/' #<- 이것만 써도 되긴 함.
       
        # 특정 경로의 파일 리스트 생성
        file_list = os.listdir(_path)

        # 특정 확장자로 이루어진 파일 리스트를 생성
        file_list2 =[]

        for file in file_list :
               if file.endswith(_end):
                      file_list2.append(file)

        # 비어있는 데이터 프레임 생성
        result = pd.DataFrame()

        # 반복문 생성
        for file in file_list2 :
                # _end가 'csv'인 경우
                if _end == 'csv':
                    df = pd.read_csv(_path+file)
                elif _end == 'json' :
                       df = pd.read_json(_path+file)
                #elif (_end =='xls') | (_end == 'xlsx'): 이걸
                elif _end in ['xls', 'xlsx'] : # 이렇게 표현해도 된다. 더 간단하게.
                       df = pd.read_excel(_path+file)
                else:
                       return "지원하지 않는 확장자입니다."
                
                # 유니언 결합
                result = pd.concat([result, df], axis=0, ignore_index=True)

        return result