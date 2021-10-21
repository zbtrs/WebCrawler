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

user = {}

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
    driver = session.get("https://github.com/zbtrs2/test/issues",headers = headers,params=data, proxies=proxy)
    html = etree.HTML(driver.text)  #换用lxml
    labels = html.xpath('//a[@class="d-block d-md-none position-absolute top-0 bottom-0 left-0 right-0"]')
    for x in labels:
        nexturl = 'https://github.com' + x.attrib.get('href')
        driver = session.get(nexturl, headers=headers, params=data, proxies=proxy)
        html = etree.HTML(driver.text)  # 换用lxml
        tokenposition = html.xpath('//details-menu[@class="select-menu-modal position-absolute right-0 hx_rsm-modal js-discussion-sidebar-menu" and @style="z-index: 99; overflow: visible;"]')
        tokenurl = tokenposition[1].attrib.get('src')
        tokenurl = 'https://github.com' + tokenurl
        response = session.get(tokenurl, headers=headers, params=data, proxies=proxy)
        html = etree.HTML(response.text)
        tokens = html.xpath('//form[@aria-label="Apply labels"]//input[@name="authenticity_token"]')
        authenticity_token = tokens[0].attrib.get('value')
        tag_data = {
            '_method': 'put',
            'authenticity_token': authenticity_token,
            'issue[labels][]':'3453563381'
        }
        tag_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh,ja;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
            'Content-Length' : '548',
            'Origin': 'https://github.com',
            'Sec-Ch-Ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'X-Requested-With' : 'XMLHttpRequest'
        }
        tagurl = nexturl + '/labels'
        response = session.post(tagurl,headers = tag_headers, data = tag_data,params=data, proxies=proxy)
        print(response)


if __name__ == '__main__':
    with open('user.json','r') as fw:
        user = json.load(fw)
    main()