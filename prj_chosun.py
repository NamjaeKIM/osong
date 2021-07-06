from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
from bs4 import BeautifulSoup
import re
import time

### 사용자 정의 모듈 ###
import chrome
import get_request # Call Url
import cre_file
import exec_psql

#////////////////////////////////////////
# chrome browser Call 
# SetChrome class 생성 =>import chrome
browser = chrome.SetChrome().getBrowser()
# ///////////////////////////////////////

#////////////////////////////////////////
### Call url 
url = "https://www.chosun.com/nsearch/?query='온라인광고'&siteid=&sort=1&date_period=all&writer=&field=&emd_word=&expt_word=&opt_chk=false&app_check=0&website=www,chosun"
browser.get(url)
browser.maximize_window() # 창 최대화
print("Url Calll >>>>>> [" + url + " ]")
#///////////////////////////////////////


# 현재 Window handle 정보 
#curr_handle = browser.current_window_handle

# 현재페이지 링크 pageload 완료될때까지 Wait
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='load-more-stories']")))

# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# 조회 기간 설정
browser.find_element_by_xpath("//*[@id='main']/div[1]/div[2]/div/div[1]/button/span").click() # 기간선택
browser.find_element_by_xpath("//*[@id='1w']/span").click()                                   # 최근 1주선택
browser.find_element_by_xpath("//*[@id='main']/div[1]/div[2]/div/div[1]/div/button").click()  # 적용선택
time.sleep(5)
# ///////////////////////////////////////////////////////////////////////////////////////////////////////

# 뉴스검색 결과 건수 
tot_news_cnt = browser.find_element_by_xpath("//*[@id='main']/div[1]/div[1]/div[1]/p")
tot_news_cnt = int(tot_news_cnt.text.replace('건','').strip())
# max page set 
max_page = math.ceil(tot_news_cnt / 10 ) # 1 page 당 10건씩 조회 >> max_page set 

print ("[{}, {} ]".format(tot_news_cnt,max_page )) 

try :
  
    print("111111")

    cur_page = 1    # 현재 page
    news_dict = {}  # 뉴스정보 dictionary
    news_cnt = 0    # 뉴스 건수 

    while True:
        # 마지막 page 검색후 end 

      
        if cur_page > max_page:
            break
            
        # 1page 이후 더보기 click() 
        if cur_page > 1: 
            browser.find_element_by_xpath("//*[@id='load-more-stories']").click()
            

        # 현재페이지 링크 pageload 완료될때까지 Wait
        # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='load-more-stories']")))
        # WebDriverWait -> last page 오류로 seleep 으로 변경
        time.sleep(3) 

        # BeautifulSoup parsing 
        soup = BeautifulSoup(browser.page_source, 'lxml')
        news = soup.find('div',{'class' : 'search-feed'})

        #뉴스목록
        news_list = news.find_all('div', {'class': 'story-card-wrapper'})

        # print(len(news_list))
        # 1 page 당 10건씩 뉴스목록이 존재 하므로, news_list 에서 (cur_page -1) *10 으로 슬라이싱 
        for info in news_list[(cur_page-1)*10:len(news_list)]: # 10건씩 리스트 슬라이싱
            
            #title 
            news_title = info.find('h3').get_text()
            #url
            news_url = info.find('h3').find('a').get('href')
            #기사본문 요약정보
            summary = info.find('span', attrs={"class":re.compile('^(story-card__deck)')})
            #기자, 날짜 
            etc = info.find('div', attrs={"class":re.compile('^(story-card__breadcrumb)')})

            # print(news_title + "\n")
            # print(news_url + "\n") 
            # print(summary.get_text() + "\n")
            # print(etc.get_text() + "\n")

            # ////////////////////////////////////////////////////////////////////////////////////
            ### 기사 원문 
            orgurl_page = news_url + "?outputType=amp"
            print("기사원문 상세 페이지 >>>>>> [" + orgurl_page + " ]")
            
            # module Call => import get_request.getRequests() 
            res = get_request.getRequests(orgurl_page)
            res_soup = BeautifulSoup(res.text, "lxml")

            ### 뉴스목록별 원문
            content = res_soup.find_all("p", attrs= {"class": re.compile('^(article-body__content)')})
        
            content_data = "" # 기사원문 데이타
            ### 기사 상세페이지 구조가 다른 page 가 존재 하여 분기시켜줌
            if len(content) > 0 :
                
                # 기사원문 데이타를 문단단위로 재조합 한다. 한줄로 나오는걸 피하기 위해 
                #content_data = [text.get_text().strip() for text in content]
                for text in content :
                    content_data = content_data + text.get_text().strip() + "\n"
            #기사원문 page 의 형식이 다름 (2가지종류)
            #위에서 content 내용이 없을때, 다른형식 page parsing
            if len(content) == 0 :
                
                # 일부 한글깨짐 현상때문에 html 다시 parsing 
                res.encoding = 'euc-kr'
                res_soup = BeautifulSoup(res.text, "lxml")

                content = res_soup.find("div", attrs= {"class": "Paragraph"})

                # 기사원문 데이타를 문단단위로 재조합 한다. 한줄로 나오는걸 피하기 위해
                # tag dt, span 은 제외 시키고 기사원문 내용만 도출 
                #content_data = [text.strip() for text in content.find_all(text=True) if text.parent.name != "dt" and text.parent.name != "span" ]
                for text in content.find_all(text=True) :
                    if text.parent.name != "dt" and text.parent.name != "span" :
                        content_data = content_data + text.get_text().strip() + "\n"

            
            # ////////////////////////////////////////////////////////////////////////////////////
            # 뉴스정보 Dictionary 
            # 뉴스정보 데이타 구조 {0:{}, 1:{}, .... }
            news_dict[news_cnt] = {
                'title' : news_title,
                'url' : news_url  ,
                'summary' : summary.get_text().strip() ,         # 요약정보
                'etc' : etc.get_text().strip(),                  # 기타정보 : 조선일보 , 기자, 일자
                'content' : content_data                         # 기사 상세내역
                }

            # next news
            news_cnt += 1
            print("[{}] {}".format(news_cnt, news_title))
            
            # ////////////////////////////////////////////////////////////////////////////////////
        # next page
        cur_page += 1
    
    # ////////////////////////////////////////////
    # file 생성
    # new_dict.values() : {0:{}, 1:{}, .... } => {}, {}, {}, ....
    news_dict = news_dict.values()

    cre_file.newsfile_chosun(news_dict)
    # ////////////////////////////////////////////

    # # //////////////////////////////////////////
    # # DataBase Insert (table : newsinfo)
    #   import exec_psql.execPsql class 
    ins = exec_psql.execPsql() #
    ins.insertArry_newsinfo(news_dict)
    # # //////////////////////////////////////////

finally :
    #browser.quit()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")





