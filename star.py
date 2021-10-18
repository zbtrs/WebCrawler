import time
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
user = {}

def main():
    username = user['username']
    useremail = user['useremail']
    userpassport = user['userpassport']
    #chrome_options = Options()
    #chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口界面大小
    #chrome_options.add_argument('--headless')
    driver = webdriver.Chrome()
    driver.get("https://github.com/orgs/apache/repositories")
    driver.set_window_size(1294,694)
    driver.find_element(By.LINK_TEXT, "Sign in").click()
    nameposition = driver.find_element(By.ID, "login_field")
    nameposition.clear()
    nameposition.send_keys(username)
    passportposition = driver.find_element(By.ID, "password")
    passportposition.clear()
    passportposition.send_keys(userpassport)
    driver.find_element(By.NAME, "commit").click()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stars = soup.find_all("a",{"class":"no-wrap Link--muted mr-3"})
    for x in stars:
        nexturl = 'https://github.com' + x.get('href')
        driver.get(nexturl)
        temp = driver.find_element(By.CSS_SELECTOR, ".unstarred > .btn")
        try:
            temp.click()
        except selenium.common.exceptions.ElementNotInteractableException as err:
            pass


if __name__ == '__main__':
    with open('user.json','r') as fw:
        user = json.load(fw)
    main()

