import requests
from bs4 import BeautifulSoup


def getRequests(url):

    #user-agent 설정
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    print("응답코드 :", res.status_code) # 200 이면 정상

    if res.status_code == requests.codes.ok:
        print("정상입니다")
    else:
        print("문제가 생겼습니다. [에러코드 ", res.status_code, "]")
    
    # request Object Return 
    return res


def getSoup(url):

    # Call url 
    res = getRequests(url)
    # BeautifulSoup Return 
    soup = BeautifulSoup(res.text, "lxml")

    return soup


