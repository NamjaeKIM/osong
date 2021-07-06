from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SetChrome() :
    def __init__(self) :
        
        chrome_options = Options()
        # chrome open 설정
        chrome_options.headless = True
        #chrome_options.headless = False
        chrome_options.add_argument("window-size=1920x1080") 
        ### file download directory
        chrome_options.add_experimental_option('prefs', {'download.default_directory':r'C:\PythonWorkspace\down'})
        ### user-agent 
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        self.browser = webdriver.Chrome(options=chrome_options) # "./chromedriver.exe"

    def getBrowser(self):
        return self.browser
 
