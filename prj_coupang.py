
import datetime

### 사용자 정의 모듈 ###
import get_request # Return Request
#import dbconn # DB Connect 
import exec_psql
import search_list

#모율 위치 검색 
# import inspect
# print(inspect.getfile(get_request)) # get_request 모듈의 위치

try:
    ### 변수 선언 ####
    dt = datetime.datetime.today().strftime('%Y%m%d') # 일자
    # 쿠팡 제품정보{table: procudt ] dictionary
    
    product_dict = {}
    
    # /////////////////////////////////////////////////
    # 쿠팡 site
    # Selenium 접근이 안돼서 url별로 처리
    # /////////////////////////////////////////////////
    
    # 카테고리별 url list
    # import search_list.getSearchList() call
    # [ 0.카테고리대분류명, 1.분류코드, 2.분류코드명, 3.url ]
    urls = search_list.getSearchList()

    # /////////////////////////////////
    # import exec_psql.execPsql class 생성
    ins = exec_psql.execPsql() # object명을 table명과 동일하게 
    # /////////////////////////////////

    # 카테고리별 scraping
    for url in urls:
         
        #url page Setting
        i = 1
        max_page = 1
        
        # data dict 초기화
        product_dict.clear()  # 제품정보 dict
        p_cnt = 0        # 제품건수

        #카타고리별 page 만큼 loop scraping
        while True :
            # 마지막 page 검색후 end           
            if i > max_page:
                break
          
            # url page Call
            # ex) https://www.coupang.com/np/categories/187069?page=2
            url_page = url[3].format(i) 
            i += 1 # url page Set
               
            ###### BeautfulSoup Return ##################
            print("Url Calll >>>>>> [" + url_page + " ]")
            soup = get_request.getSoup(url_page)
            ###### BeautfulSoup Return ##################
    
            # max page 도출
            data_page = soup.find("a", attrs={"class":"icon next-page"})['data-page']
            max_page = int(data_page)

            max_page = 2 #test.....

            # ////////////////////////////////////////////////////////////
            # 구팡 랭킹순 상품 목록
            lis = soup.find("ul", attrs={"id":"productList"}).find_all("li")
            #print(len(lis))

            
            # ///////////////////////////////////////////////////////////
            # 상품정보 도출
            for li in lis:
                try:
                    #제품명
                    img = li.find("dt", attrs={"class":"image"}).find("img")
                    print("제품명 : " + img['alt'])
                    
                    #가격
                    #priceWrap = li.find("div", attrs={"class":{"price-wrap", "price-area"}}).find("strong")
                    priceWrap = li.find("div", attrs={"class":"price-wrap"})
                    ## 특정 page 는 price-wrap 가 없어서, 분기 처리 (price-wrap -> price-area)
                    if priceWrap is None :
                        priceWrap = li.find("div", attrs={"class":"price-area"}).find_all("strong")[1] # strong 배열 1 이 가격
                    else :
                        priceWrap = priceWrap.find("strong")

                    print("가격 : " + priceWrap.get_text())
                    price = priceWrap.get_text().strip().replace(",", "")

                    # 상품정보 Dictionary 
                    # 상품정보 데이타 구조 {{}, {}, .... }
                    product_dict[p_cnt] = {
                        'dt' : dt ,                      # 일자
                        'name' : img['alt'].strip()  ,   # 제품명
                        'price' : int(price ) ,          # 가격
                        'img_url' : '' ,                 # 이미지 url
                        'source_url' : url_page ,        # source_url
                        'gubun' : url[1] ,               # 쿠팡 카테고리 분류코드
                        'gubun_nm': url[2] ,             # 분류명 
                        'categori' : url[0]              # 카테고리 대분류고드명    
                        }

                    # next product
                    p_cnt += 1

                except Exception as e:
                    print("errr-------------")
                    print(e)
                    print("제품명 [" + img['alt'].strip() + "]")
                    print('url : ' + url_page)

            # /////////////////////////////////////////////////////////////
        # # //////////////////////////////////////////
        # # DataBase Insert (table : product)
        # import exec_psql.execPsql class 
        # product_dict.values() : {{}, {}, .... } => {}, {}, {}, ....
        product_dict = product_dict.values()
        ins.insertArry_product(product_dict)
        # # //////////////////////////////////////////


except Exception as e:
    print("errr-------------------------")
    print(e)
finally:

    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

