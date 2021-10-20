import sys
import time
import json
import requests
import re
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By

proxy = {
	'http': '127.0.0.1:7890',
	'https': '127.0.0.1:7890'
}

data = {
	'wd': 'ip'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
}

def main():
    username = user['username']
    useremail = user['useremail']
    userpassword = user['userpassword']
    login_url = 'https://github.com/login'
    session = requests.Session()
    response = session.get(login_url,headers = headers,params=data, proxies=proxy)
    pattern = re.compile(r'<input type="hidden" name="authenticity_token" value="(.*)">')
    authenticity_token1 = pattern.findall(response.text)[0]
    authenticity_token = ""
    for ch in authenticity_token1:
        if ch == '"':
            break
        authenticity_token += ch
    login_data = {
        'commit': 'Sign in',
        'utf8': '%E2%9C%93',
        'authenticity_token': authenticity_token,
        'login': username,
        'password': userpassword
    }
    session_url = 'https://github.com/session'
    response = session.post(session_url, headers = headers, data = login_data,params=data, proxies=proxy)
    print(response)
    driver = session.get("https://github.com/orgs/apache/repositories",headers = headers,params=data, proxies=proxy)
    html = etree.HTML(driver.text)  #换用lxml
    List = html.xpath('//a[@class="d-inline-block"]')
    for x in List:
        nexturl = 'https://github.com' + x.attrib.get('href')
        starurl = nexturl + '/star'
        star_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh,ja;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
            'Content-Length' : '341',
            'Origin': 'https://github.com',
            'Referer': 'nexturl',
            'Sec-Ch-Ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'X-Requested-With' : 'XMLHttpRequest'
        }
        driver = session.get(nexturl, headers=headers, params=data, proxies=proxy)
        html = etree.HTML(driver.text)  # 换用lxml
        List = html.xpath('//form[@class="unstarred js-social-form"]/input[@name="authenticity_token"]')
        authenticity_token = List[0].attrib.get('value')
        star_data = {
            'authenticity_token': authenticity_token,
            'context': 'repository'
        }
        session.post(starurl,headers = star_headers, data = star_data,params=data, proxies=proxy)

if __name__ == '__main__':
    with open('user.json','r') as fw:
        user = json.load(fw)
    main()