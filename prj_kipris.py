
import requests
from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from urllib.request import urlretrieve

import string
from collections import Counter

### 사용자 정의 모듈 ###
import chrome
import cre_file
import exec_psql

#////////////////////////////////////////
# chrome browser Call 
# SetChrome class 생성 =>import chrome
browser = chrome.SetChrome().getBrowser()
# ///////////////////////////////////////

browser.maximize_window() # 창 최대화

# 1. kipris 이동
#browser.get("http://www.kipris.or.kr/khome/main.jsp")
browser.get("http://kpat.kipris.or.kr/kpat/searchLogina.do?next=MainSearch#page1")

time.sleep(3)

# ////////////////////////////////////////////////////////////////////////////////////////////
# selenium browser 검색조건 
# 2.메뉴 특허.실용신안 이동
#browser.find_element_by_xpath("//*[@id=\"gnb\"]/li[1]/div/ul/li[1]/a").click()
browser.find_element_by_xpath('//*[@id="opt28"]/option[3]').click()  # 페이지당 90건 조회 setting 
browser.find_element_by_xpath('//*[@id="pageSel"]/a/img').click()    # go button click 
browser.find_element_by_id("queryText").click() # 검색조건 foucs
browser.find_element_by_id("queryText").clear() # 검색조건 clear 
browser.find_element_by_id("queryText").send_keys("온라인마케팅") # 검색조건 Set
browser.find_element_by_id("queryText").send_keys(Keys.ENTER)    # 검색 
# /////////////////////////////////////////////////////////////////////////////////////////////


try:
  
    # 현재페이지 링크 pageload 완료될때까지 Wait
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='divBoardPager']/strong")))
    
    #총 page 조회
    pages= browser.find_element_by_class_name("float_left")
    pages_str = str(pages.text)
    page = pages_str.split("(")
    page = page[1].replace(")", "").replace("Pages","")
    page = page.split("/")
    
    curr_page = page[0].strip()  #현재페이지
    max_page = page[1].strip()   #max페이지

    curr_page = 1
    #테스트///////////////////////////////////
    max_page = 2 # 테스트테스트 지우기
    ###//////////////////////////////////////
    dt = datetime.datetime.today().strftime('%Y%m%d') # 일자
    article_dict = {}  # 특허정보 dict DataSet
    counter_dict = {}  # 단어 빈도수 DataSet

    while curr_page <= max_page:

        # ////////////////////////////////////////////////
        # 다음페이지 검색시 javascript를 실행시켜 page 검색
        if curr_page > 1:
            
            jscript= "SetPageAjax('{}')".format(curr_page)
            browser.execute_script(jscript)
            time.sleep(5)
        # ////////////////////////////////////////////////

        # BeautifulSoup Parsing 
        soup = BeautifulSoup(browser.page_source, 'lxml')

        
        # ////////////////////////////////////////////////////////////////////////////////////////
        # page 엑셀정보 다운로드 Click 
        # 서지정보 엑셀저장 다운로드 
        #browser.find_element_by_xpath("//*[@id='detail_content']/div[1]/div[2]/span[3]/a").click()
        # ////////////////////////////////////////////////////////////////////////////////////////

        
        # 특허정보 DataSet Start///////////////////////////////////////////////////////////////////
        # 특허정보 tag
        # page 당 90 건씩 특허정보
        
        article_dict.clear()  # 특허정보 dict DataSet 초기화
        counter_dict.clear()  # 단어 빈도수 dict DataSet 초기화

        cnt = 0               # 특허정보 건수
        wordcnt = 0           # 수집단어 건수

        search_section = soup.find("section", attrs={"class":"search_section"})
        #print(len(search_section))
        #print(search_section)
        

        # 특허정보-세부사항 
        articles = search_section.find_all("article", attrs= {"id":re.compile('^(divViewSel)')})
        for article in articles:
            #title
            stitle = article.find("h1", attrs={"class":"stitle"}).get_text()
            status = article.find("h1", attrs={"class":"stitle"}).find("span", attrs={"id":"iconStatus"}).get_text()
            #print(stitle)
            #요약정보
            summary = article.find("div", attrs={"class":"search_txt"}).get_text().strip()
           
            #출원정보
            mainlist_topinfo = article.find("div", attrs={"class":"mainlist_topinfo"}).find_all("li")

            #출원번호/출원일자
            topinfo = mainlist_topinfo[1].find("a").get_text().strip()
            topinfo_split = topinfo.split("(")
            topinfo_no = topinfo_split[0].strip()  # 출원번호
            topinfo_dt = topinfo_split[1].replace(")", "").replace(".","").strip() # 출원일자 

            #춸원인
            #topinfo_person = mainlist_topinfo[2].get_text().strip()
            topinfo_person = mainlist_topinfo[2].find("a").get_text()
            #최종권리자
            #print(mainlist_topinfo[3].get_text())
            #topinfo_rights = mainlist_topinfo[3].get_text().strip()
            topinfo_rights = mainlist_topinfo[3].find("font").get_text()
             
            #이미지 link 
            #이미지번호(출원번호)
            img_no = article['id']
            img_no = img_no[10:]
            image_url = ""

            
            alt = article.find("div", attrs={"class":"thumb"}).find("img")['alt']
            if alt == '등록된 이미지 없음':
                 image_url = ""
            else:
                #print(thumb)
                #print(img_no)
                image_url = "http://kpat.kipris.or.kr/kpat/biblio/biblioFrontDrawPop.jsp?applno={}".format(img_no)


            #print(image_url)
                
            # //////////////////////////////////////////////////////////////////////////////////////////
            # 팝업정보 필요시 로직 반영
            # # ...테스트..
            # if img_no == '1020187007157' :
            #     browser.execute_script("openDetail(1020187007157, 29, '', 'biblio', '30', 'View01')")

            #     handles = browser.window_handles # 모든 핸들 정보
            #     for handle in handles:
            #         print("********************\n")
            #         print(handle) # 각 핸들 정보
            #         browser.switch_to.window(handle) # 각 핸들로 이동해서

            #         print(browser.title) # 출력해보면 현재 핸들 (브라우저) 의 제목 표시
                    
            #         #상세정보 팝업 Open
            #         if "상세정보" in browser.title:
            #            pop_soup = BeautifulSoup(browser.page_source, 'lxml')

            #            with open("kipris.html", "w", encoding="utf8") as f:
            #                #f.write(res.text)
            #                f.write(pop_soup.prettify()) # html 문서를 예쁘게 출력
            # ///////////////////////////////////////////////////////////////////////////////////////////


            # 상품정보 Dictionary 
            # 상품정보 데이타 구조 {{}, {}, .... }
            article_dict[wordcnt] = {
                'dt' : dt ,                      # 일자
                'title' : stitle ,               # 특허제목
                'status' : status,               # 특허상태
                'topinfo_no' : topinfo_no ,      # 출원번호  
                'topinfo_dt' : topinfo_dt ,      # 출원일자
                'topinfo_person' : topinfo_person , # 출원인
                'topinfo_rights' : topinfo_rights , # 최종권리자
                'image_url' : image_url ,        # 이미지 url
                'summary': summary ,             # 요약정보
                'page_info' : curr_page          # 특허 page 정보
                }

            # next dict
            cnt += 1        # 특허정보 건수
            print ("특허명 [" + stitle + "]")

            # 특허정보 DataSet End ////////////////////////////////////            

            #print(article_dict)

            ## ////////////////////////////////////////////////////////////////////////////
            ## 요약내용 단어 빈도수 수집
            ## 공백으로 단어 구분, 특수문자 제거 => list로 단어 저장
            ## ////////////////////////////////////////////////////////////////////////////
            content = re.sub('\n', ' ', summary)   # \n 제거 
            content = content.split(' ')           # 공백으로 단어 분리
            content = [word.strip(string.punctuation+string.whitespace) for word in content] # 특수문자등 제거
            content = [word.strip() for word in content if len(word.strip()) > 1 ]           # 공백라인 제거
            
            ## /////////////////////////////////////
            # Coounter 객체 선언 
            # 요약내용 단어별 빈도수 산출
            ## /////////////////////////////////////
            ngrams  = Counter()
            
            ngrams_list = []
            n = 1
            for i in range(len(content)-n+1):
                ngrams_list.extend(content[i:i+n])

            ngrams.update(ngrams_list)

            counter_list = Counter(ngrams_list)
            ## /////////////////////////////////////
            sq = 1
            for key, value in counter_list.items():
                # 단어 빈도수 dict DataSet
                # 데이타 구조 {{}, {}, .... }
                counter_dict[wordcnt] = {
                    'dt' : dt ,                      # 일자
                    'title' : stitle ,               # 특허제목
                    'topinfo_no' : topinfo_no,       # 특허번호
                    'topinfo_dt' : topinfo_dt,       # 출원일자
                    'seq' : sq,                      # 특허1건별 수집단어 건수
                    'word' : key,                    # 단어 
                    'count' : value                  # 빈도수
                    }
                
                sq += 1       # 특허1건당 추출단어 순번 
                wordcnt += 1  # page 당 단어건수증가 (dictionary 첨자 증가) 

 
        # ////////////////////////////////////////////////////////
        # file 생성 (csv 파일 생성)
        # article_dict.values() : {0:{}, 1:{}, .... } => {}, {}, {}, ....
        # args = 0.DataSet, 1.검색조건, 2.현재page 
        # //////////////////////////////////////////////////////////

        topinfo_dict = article_dict.values()
        cre_file.topinfo_toCsv(topinfo_dict, '온라인마케팅', curr_page )

        # ////////////////////////////////////////////////////////
        # 요약내용 단어 빈도수 file 생성 (csv 파일 생성)
        # counter_dict.values() : {0:{}, 1:{}, .... } => {}, {}, {}, ....
        # args = 0.DataSet, 1.검색조건, 2.현재page 
        # //////////////////////////////////////////////////////////

        wordcnt_dict =counter_dict.values()
        cre_file.wordCnt_toCsv(wordcnt_dict, '온라인마케팅', curr_page )


        # # ///////////////////////////////////////////////////////
        # # DataBase Insert (table : kipris_info)
        # # import exec_psql.execPsql class 
        # Page 단위로 Insert (특허정보 90건씩 Insert )
        # # ///////////////////////////////////////////////////////
        
        # sql Class 생성
        ins = exec_psql.execPsql() 
        ins.insertArry_kiprisInfo(topinfo_dict) 

        # # ///////////////////////////////////////////////////////
        # # DataBase Insert (table : kipris_counter)
        # # import exec_psql.execPsql class 
        # Page 단위로 Insert (특허 요약내용 수집단어 빈도수 Insert (건수 : page당 특허수 * 수집단어수 ))
        # # ///////////////////////////////////////////////////////
        ins.insertArry_kiprisCounter(wordcnt_dict)
        
        curr_page += 1
        print("*****************\n")
        print(curr_page)    

    #테스트
    #browser.execute_script("SetPageAjax('11')")
             
finally:
    #browser.quit()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
