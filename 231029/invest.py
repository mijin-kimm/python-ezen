# 라이브러리 로드
from time import strptime
import pandas as pd
import numpy as np
from datetime import datetime

# class 선언
class Invest:
    # 생성자 함수 : class가 생성될때 최초로 한번만 실행이 되는 함수(초기화 함수)
    def __init__(self, _df, _col = 'Adj Close', _start = '20100101', _end = '20231231'):
        # self 변수들을 정의
        self.df = _df
        self.col = _col
        self.start = _start
        self.end = _end
        self.start = datetime.strptime(self.start, '%Y%m%d').isoformat()
        self.end = datetime.strptime(self.end, '%Y%m%d').isoformat()


    def buyandhold(self):
        # df에 columns에 Date가 존재한다면 Date를 인덱스로 변환
        if 'Date' in self.df.columns:
            self.df = self.df.set_index('Date')
        # index를 시계열 데이터로 변경 (to_datetime(Series데이터, format=Series데이터의 폼))
        self.df.index = pd.to_datetime(self.df.index, format='%Y-%m-%d')

        # 결측치, 무한대, 음의 무한대 값을 제외시킨다. 
        self.df = self.df.loc[~self.df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]
        # 기준이 되는 컬럼을 제외하고 나머지 컬럼을 제거 
        self.df = self.df[[self.col]]
        # 일별 수익율 계산해서 새로운 파생변수에 대입
        self.df["daily_rtn"] = self.df[self.col].pct_change()
        # 구매한 날과 판매한 날을 기준으로 데이터를 필터링
        self.df = self.df.loc[self.start : self.end]
        # 누적 수익율을 계산하여 새로운 파생변수에 대입 
        self.df['st_rtn'] = (1 + self.df['daily_rtn']).cumprod()

        return self.df
    
    def bollinger(self):
        # df에 columns에 Date가 존재한다면 Date를 인덱스로 변환
        if 'Date' in self.df.columns:
            self.df = self.df.set_index('Date')
        # index를 시계열 데이터로 변경 (to_datetime(Series데이터, format=Series데이터의 폼))
        self.df.index = pd.to_datetime(self.df.index, format='%Y-%m-%d')

        # 결측치, 무한대, 음의 무한대 값을 제외시킨다. 
        self.df = self.df.loc[~self.df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]
        # 기준이 되는 컬럼을 제외하고 나머지 컬럼을 제거 
        self.df = self.df[[self.col]] 
        # 구매한 날과 판매한 날을 기준으로 데이터를 필터링
        self.df = self.df.loc[self.start : self.end]
        # case2 (rolling(n)) : n개 만큼 데이터를 묶는다.
        self.df['center'] = self.df[self.col].rolling(20).mean()   
        # 상단 밴드 
        self.df['ub'] = self.df['center'] + ( 2 * self.df[self.col].rolling(20).std() )
        # 하단 밴드 
        self.df['lb'] = self.df['center'] - ( 2 * self.df[self.col].rolling(20).std() )# 거래 내역 파생변수 생성 
        self.df['trade'] = ''

        for i in self.df.index:
            # i? -> self.df의 index 값들이 하나씩 대입

            # 상단밴드보다 종가가 높은 경우
            if self.df.loc[i, self.col] > self.df.loc[i, 'ub']:
                self.df.loc[i, 'trade'] = ''
            # 하단밴드보다 종가가 낮은 경우
            elif self.df.loc[i, self.col] < self.df.loc[i, 'lb']:
                self.df.loc[i, 'trade'] = 'buy'
            # 밴드 사이에 종가가 존재하는 경우
            else:
                # 현재 구매 상태라면? 전날의 trade가 buy인 경우
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = 'buy'
                else :
                    self.df.loc[i, 'trade'] = ''
        rtn = 1.0
        buy = 0.0
        sell = 0.0

        # 수익율 파생변수 생성
        self.df['return'] = 1.0

        for i in self.df.index:
            # i? self.df의 index값들이 하나씩 대입하여 실행

            # 구매가
            if (self.df.shift(1).loc[i, 'trade'] == '') & (self.df.loc[i, 'trade'] == 'buy'):
                # 해당하는 날짜의 종가를 buy에 대입
                buy = self.df.loc[i, self.col]
                print('매수한 날짜 :', i, '매수가 :', buy)
            # 판매가
            elif (self.df.shift(1).loc[i, 'trade'] == 'buy') & (self.df.loc[i, 'trade'] == ''):
                # 판매가를 sell에 대입
                sell = self.df.loc[i, self.col]
                # 수익율 계산
                rtn = sell / buy
                # 수익율을 해당하는 날짜의 return에 대입
                self.df.loc[i, 'return'] = rtn
                print('매도 날짜 :', i, '매도가 :', sell, '수익율 :', rtn)
        # 누적 수익율

        acc_rtn = 1.0

        for i in self.df.index:
            rtn = self.df.loc[i, 'return']
            acc_rtn *= rtn
            self.df.loc[i, 'acc_rtn'] = acc_rtn

        print('누적 수익율 :', acc_rtn)
        return self.df
