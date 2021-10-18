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

user = {}

def main():
    username = user['username']
    useremail = user['useremail']
    userpassport = user['userpassport']
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
    driver.get("https://github.com/zbtrs2/test/issues")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    labels = soup.find_all("a",{"class":"d-block d-md-none position-absolute top-0 bottom-0 left-0 right-0"})
    for x in labels:
        nexturl = 'https://github.com' + x.get('href')
        driver.get(nexturl)
        driver.find_element(By.CSS_SELECTOR, "#labels-select-menu > .text-bold > .octicon").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".select-menu-item:nth-child(1) .description").click()
        time.sleep(1)

if __name__ == '__main__':
    with open('user.json','r') as fw:
        user = json.load(fw)
    main()