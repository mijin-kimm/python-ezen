from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


class Trip():

    def __init__(self, search):
        self.search = search

    async def save_excel(self):
        # 웹드라이버를 오픈 
        driver = webdriver.Chrome()

        # 웹드라이버에 네이버로 접속
        driver.get('http://www.naver.com')

        # 검색어창 태그를 선택
        element = driver.find_element(By.ID, 'query')

        # 검색어창에 특정 문자열 입력
        element.send_keys('트립어드바이저')

        # 검색어창에서 ENTER키 이벤트 발생
        element.send_keys(Keys.ENTER)


        time.sleep(1)

        # class가 link_name인 태그를 선택
        element2 = driver.find_element(By.CLASS_NAME, 'link_name')


        # element2를 클릭 이벤트 발생
        element2.click()
        
        time.sleep(1)

        # 자식창으로 이동 
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[1])

        # name이 q인 태그를 선택
        element3 = driver.find_element(By.NAME, 'q')

        # element3에 특정 문자열을 입력
        element3.send_keys(self.search)  

        element3.send_keys(Keys.ENTER)
        
        time.sleep(1)

        soup = bs(driver.page_source, 'html.parser')

        div_data = soup.find('div', attrs={
            'class' : 'prw_search_search_results'
        })

        div_data2 = div_data.find('div', attrs={
            'class' : 'is-multiline'
        })

        title_list = div_data2.find_all('div', attrs={
            'class' : 'result-title'
        })

        title = []

        for i in title_list:
            title.append(i.get_text())

        img_list = div_data2.find_all('div', attrs={
            'class' : 'is-shown-at-desktop'
        })

        img = list(map(
            lambda x : x.find('div', attrs={
                'class' : 'inner'
            })['style'], 
            img_list
        ))

        img2 = list(map(
            lambda x : x.replace("background-image:url(", "").replace(");", ""), 
            img
        ))

        df = pd.DataFrame({
            'title' : title, 
            'img' : img2
        })

        df.to_excel(f'{self.search}.xlsx', index=False)

        driver.close()

        return "엑셀 저장 완료"