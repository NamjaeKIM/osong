
import dbconn # DB Connect 
import datetime

dt = datetime.datetime.today().strftime('%Y%m%d') # 일자

# //////////////////////////////////////////////////////
# 단건 insert 
# //////////////////////////////////////////////////////
def execute(sql):
    try:
        # DB connect
        with dbconn.dbConn() as db:
            
            with db.conn.cursor() as cursor:
                # table Insert 
                cursor.execute(sql)
                cursor.connection.commit()
    except Exception as e :
        print(" insert DB err ",e)


# /////////////////////////////////////////////////////
# 다건 Array Insert
# /////////////////////////////////////////////////////
def execute_many(sql, rowdata):
    try:
        with dbconn.dbConn() as db:
            with db.conn.cursor() as cursor:
                cursor.executemany(sql, rowdata)
                cursor.connection.commit()
    except Exception as e :
        print(" insert_many DB err ",e)  


# ////////////////////////////////////////////////////////////////////
# sql binding Class 
# ///////////////////////////////////////////////////////////////////
class execPsql():
    # def __init__(self) :
    
    # ----------------------------------
    # 쿠팡 상품정보 단건 (product) insert 
    # ----------------------------------
    def insert_product(self, *args):
        
        try: 
            # args : 0.일자, 1.제품명, 2.가격
            sql = """ INSERT INTO PRODUCT (DT, SQ, NAME, PRICE ) VALUES (
                                        '{}'                   
                                        , nextval('product_sq')
                                        , '{}'
                                        , '{}') ;
                                        """.format(args[0],      # 0.일자 
                                                    args[1],      # 1.제품명
                                                    args[2])      # 2.가격
            # 단건 insert exec sql
            execute(sql)

        except Exception as e:
            print('[insert_product ] sql Binding Err------------------------------------')
            print(e)


    # ----------------------------------
    # 조선일보 뉴스정보 검색 단건 Insert 
    # ----------------------------------
    def insertArry_newsinfo(self, news_dict={}):
        try:
            sql = """ INSERT INTO NEWSINFO (DT, SQ, TITLE, URL, SUMMARY, ETC)  VALUES (
                            '{}'                             
                            , nextval('newsinfo_sq')
                            , %s
                            , %s
                            , %s
                            , %s)
                """.format(dt)

            # 데이타 형태는 list[tuple(title, url, summary, etc)] 형태가 아니면 error 발생 
            rowdata_list = [tuple([r['title']         # 제목
                                , r['url']           # url
                                , r['summary']       # 요약정보 
                                , r['etc']]          # 기타 : 신문사, 일자, 기자
                                ) 
                                for r in news_dict
                            ]
            
            # 다건 insert
            execute_many(sql, rowdata_list)

        except Exception as e:
            print('[insertArry_newsinfo ] sql Binding Err------------------------------------')
            print(e)


    # --------------------------------------------
    # 조선일보 뉴스정보 검색 다건 Array Insert 
    # --------------------------------------------
    def insertArry_product(self, product_dict={}):

        try:
            # 일자/시퀀스/제품명/가격/이미지_URL/소스_URL/구분/구분명
            #sql = """ INSERT INTO PRODUCT (DT, SQ, NAME, PRICE, IMG_URL, SOURCE_URL, GUBUN, GUBUN_NM, CATEGORI)  VALUES (
            sql = """ INSERT INTO PRODUCT (DT, SQ, NAME, PRICE, IMG_URL, SOURCE_URL, GUBUN, GUBUN_NM, CATEGORI)  VALUES (
                            %s                             
                            , nextval('newsinfo_sq')
                            , %s
                            , cast(%s as integer)
                            , %s
                            , %s
                            , %s
                            , %s
                            , %s)
                """

            # 데이타 형태는 list[tuple(a,b,c,...)] 형태가 아니면 error 발생 
            rowdata_list = [tuple([r['dt']
                                , r['name']
                                , r['price']
                                , r['img_url']
                                , r['source_url']
                                , r['gubun']
                                , r['gubun_nm']
                                , r['categori'] ] 
                                ) for r in product_dict 
                            ]

            # /////////////////////////////
            # 다건 Array Insert
            execute_many(sql, rowdata_list)
            # ////////////////////////////
                                    
        except Exception as e:
            print('[insertArry_product ] sql Binding Err------------------------------------')
            print(e)

    # --------------------------------------------
    # kipris 특허정보 검색 다건 Array Insert 
    # --------------------------------------------
    def insertArry_kiprisInfo(self, article_dict={}):

        try:
            # 일자/시퀀스/특허명/특허상태/특허번호/출원일자/출원인/최종권리자/이미지URL/요약/page 
            sql = """ INSERT INTO kipris_info (DT
                                            , SQ
                                            , TITLE
                                            , status
                                            , topinfo_no
                                            , topinfo_dt
                                            , topinfo_person
                                            , topinfo_rights
                                            , image_url
                                            , summary
                                            , page_info) 
                                    VALUES (
                                            %s                             
                                        , nextval('kipris_info_sq') 
                                        , %s, %s, %s, %s, %s, %s, %s, %s, %s
                                        )
                """

            # 데이타 형태는 list[tuple(a,b,c,...)] 형태가 아니면 error 발생 
            rowdata_list = [tuple([r['dt']
                                , r['title']
                                , r['status']
                                , r['topinfo_no']
                                , r['topinfo_dt']
                                , r['topinfo_person']
                                , r['topinfo_rights']
                                , r['image_url'] 
                                , r['summary']
                                , r['page_info']] 
                                ) for r in article_dict 
                            ]


            # /////////////////////////////
            # 다건 Array Insert
            execute_many(sql, rowdata_list)
            # ////////////////////////////                            
        except Exception as e:
            print('[insertArry_kiprisInfo ] sql Binding Err------------------------------------')
            print(e)


    # --------------------------------------------
    # kipris 특허정보 단어 빈도수 다건 Array Insert 
    # --------------------------------------------
    def insertArry_kiprisCounter(self, wordcnt_dict={}):

        try:
            # 일자/시퀀스/특허명/특허상태/특허번호/출원일자/출원인/최종권리자/이미지URL/요약/page 
            sql = """ INSERT INTO kipris_counter (DT
                                            , TITLE
                                            , topinfo_no
                                            , topinfo_dt
                                            , seq
                                            , word
                                            , count
                                            ) 
                                    VALUES (
                                            %s, %s, %s, %s, cast(%s as integer) , %s, %s
                                        )
                """

            # 데이타 형태는 list[tuple(a,b,c,...)] 형태가 아니면 error 발생 
            rowdata_list = [tuple([r['dt']
                                , r['title']
                                , r['topinfo_no']       # 특허번호
                                , r['topinfo_dt']       # 특허일자 
                                , r['seq']              # 특허1건당 수집단어 순번
                                , r['word']             # 단어
                                , r['count']]           # 빈도수
                                ) for r in wordcnt_dict 
                            ]
            #print(rowdata_list)
            # /////////////////////////////
            # 다건 Array Insert
            execute_many(sql, rowdata_list)
            # ////////////////////////////

        except Exception as e:
            print('[insertArry_kiprisCounter ] sql Binding Err ------------------------------------')
            print(e)


 

