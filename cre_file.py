import pandas as pd
from pandas import DataFrame
import os
from datetime import datetime
#import datetime

#from openpyxl import load_workbook
import csv

date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':','시') + '분' 

# 조선일보 뉴스검색 file 생성
def newsfile_chosun(news_dict={}) :

    filename = 'C:\PythonWorkspace\조선일보뉴스_온라인광고.txt'

    # news_dict = dict
    # # 뉴스정보 데이타 구조를 dict 형태로 변경 
    # # values 값이 dict 형태 
 
    # ////////////////////////////////////////////////////////////
    ## txt 파일 생성 
    # ////////////////////////////////////////////////////////////
    with open(filename, "w", encoding='utf8') as newsfile:
        for news_data in news_dict:
            newsfile.write("\n[title] " + news_data['title'])
            newsfile.write("\n[url  ] " + news_data['url'])
            newsfile.write("\n[요약 ] " + news_data['summary'])
            newsfile.write("\n[출처 ] " + news_data['etc'])
            newsfile.write("\n[기사원문 ]")

            newsfile.write("\n" + news_data['content'])
            newsfile.write("\n")

    # ///////////////////////////////////////////////////////////////////////
    # pip pandas
    ### 엑셀파일 생성 
    # ///////////////////////////////////////////////////////////////////////
    news_df = DataFrame(news_dict)
    # news_df = DataFrame(news_dict).transpose() # pandas 행열 전환
    # news_df = news_df.T

    folder_path = os.getcwd()
    xlsx_file_name = '조선일보뉴스_온라인광고_{}.xlsx'.format(date)
    #csv_file_name  = '조선일보뉴스_온라인광고_{}.txt'.format(date)
    news_df.to_excel(xlsx_file_name)
    #news_df.to_csv(csv_file_name, sep = '\t', index = False)

    print('파일 저장 완료 | 경로 : {}\\{}'.format(folder_path, xlsx_file_name))
    #os.startfile(folder_path)
    # /////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////
# 키프리스 특허정보 엑셀파일 생성 
# ///////////////////////////////////
import datetime
def topinfo_toCsv(topinfo_dict={}, *args) :


    dt = datetime.datetime.today().strftime('%Y%m%d') # 일자

    folder_path = os.getcwd()
    
    print(folder_path)
    try : 
        file_name = "특허정보_{}_{}.csv".format(args[0], dt)
        csv_file_name = folder_path + '\\' + file_name 

        f = open(csv_file_name, "a", encoding="utf-8-sig", newline="")
        writer = csv.writer(f)

        # Header Write
        if args[1] == 1 :
            title = ['일자','특허명', '상태', '출원번호', '출원일자', '출원인', '최종관리자', '이미지url', '요약정보']
            #print(type(title))
            writer.writerow(title)

        # Data Write
        for row in topinfo_dict:
            data = [row['dt'], row['title'], row['status'], row['topinfo_no'], row['topinfo_dt'], row['topinfo_person'], row['topinfo_rights'], row['image_url'], row['summary']]
            writer.writerow(data)
        
        f.close()

        print('파일 저장 완료 | 경로 : {}\\{}'.format(folder_path, file_name))
        #os.startfile(folder_path)
    
    except Exception as e:
        print('file err ------------------------------------')
        print(e)
        f.close()
    finally:
        f.close()


# ////////////////////////////////////////////////
# 키프리스 특허정보 요약내용 단어 빈도수 엑셀파일 생성 
# ////////////////////////////////////////////////
def wordCnt_toCsv(wordcnt_dict={}, *args) :


    dt = datetime.datetime.today().strftime('%Y%m%d') # 일자

    folder_path = os.getcwd()
    
    print(folder_path)
    try : 
        file_name = "특허정보_{}_단어빈도수_{}.csv".format(args[0], dt)
        csv_file_name = folder_path + '\\' + file_name 

        f = open(csv_file_name, "a", encoding="utf-8-sig", newline="")
        writer = csv.writer(f)

        # Header Write
        if args[1] == 1 :
            title = ['일자','특허명', '특허번호', '출원일자', '순번', '단어', '빈도수']
            #print(type(title))
            writer.writerow(title)

        # Data Write
        for row in wordcnt_dict:
            data = [ row['dt'], row['title'], row['topinfo_no'], row['topinfo_dt'], row['seq'], row['word'], row['count'] ]
            writer.writerow(data)
        
        f.close()

        print('파일 저장 완료 | 경로 : {}\\{}'.format(folder_path, file_name))
        #os.startfile(folder_path)
    
    except Exception as e:
        print('file err ------------------------------------')
        print(e)
        f.close()
    finally:
        f.close()