import sys
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree

proxy = {
	'http': '127.0.0.1:7890',
	'https': '127.0.0.1:7890'
}

data = {
	'wd': 'ip'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

OutFile = []

def solve(Html, driver):  # 应该把所有数据给封装起来
    dict = {}
    Name = Html.xpath('//a[@data-pjax="#js-repo-pjax-container"]')  #仓库名
    dict.update({"Name":Name[0].text.strip()})
    About = Html.xpath('//p[@class="f4 mt-3"]')
    dict.update({"About": About[0].text.strip()})
    License = Html.xpath('//div[@class="mt-3"]/a[@class="Link--muted"]//text()')
    dict.update({"License":License[-1].strip()})
    Languages = Html.xpath('//li[@class="d-inline"]/a/span[1]')
    Proportions = Html.xpath('//li[@class="d-inline"]/a/span[2]')
    LanguageList = {}
    for i in range(len(Languages)):
        LanguageList.update({Languages[i].text:Proportions[i].text})
    dict.update({"Languages":LanguageList})
    Next = Html.xpath('//a[@class="pl-3 pr-3 py-3 p-md-0 mt-n3 mb-n3 mr-n3 m-md-0 Link--primary no-underline no-wrap"]')
    NextUrl = 'https://github.com' + Next[0].attrib.get('href')
    IssuesUrl = 'https://github.com'
    IssueList = Html.xpath('//a[@id="issues-tab"]')
    if (len(IssueList) > 0):   #如果有Issue
        IssuesUrl += IssueList[0].attrib.get('href')

    driver = requests.get(url=NextUrl, headers=headers, params=data, proxies=proxy)
    Html = etree.HTML(driver.text)
    Committers = Html.xpath('//a[@class="commit-author user-mention"]')
    CommitMessages = Html.xpath('//a[@class="Link--primary text-bold js-navigation-open markdown-title"]')
    CommitHashs = Html.xpath('//a[@class="text-mono f6 btn btn-outline BtnGroup-item"]')
    for i in range(min(5,len(Committers))):
        dict.update({"commit " + str(i + 1): Committers[i].text.strip() + " " + CommitMessages[i].text.strip() + " " +
                                             CommitHashs[i].text.strip()})

    if IssuesUrl != 'https://github.com':
        driver = requests.get(url=IssuesUrl, headers=headers, params=data, proxies=proxy)
        Html = etree.HTML(driver.text)
        IssueList = Html.xpath('//a[@class="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title"]')
        for i in range(min(5, len(IssueList))):
            print("!",i)  #输出便于查看当前爬到什么程度了
            Issue = IssueList[i]
            NextUrl = 'https://github.com' + Issue.get('href')
            driver = requests.get(url=NextUrl, headers=headers, params=data, proxies=proxy)
            Html = etree.HTML(driver.text)
            titleList = Html.xpath('//span[@class="js-issue-title markdown-title"]')
            title = titleList[0].text.strip()
            Body = ""
            Bodys = Html.xpath('//div[@class="edit-comment-hide"]//p//text()')
            for value in Bodys:
                Body += value.strip()
            Issuedict = {}
            Issuedict.update({"Title":title})
            Issuedict.update({"Body":Body})
            dict.update({"Issue " + str(i + 1):Issuedict})
    OutFile.append(dict)

def main():
    url = 'https://github.com/orgs/apache/repositories'
    driver = requests.get(url=url, headers=headers, params=data, proxies=proxy)
    html = etree.HTML(driver.text)  #换用lxml
    List = html.xpath('//div//a')
    NextList = []
    for value in List:
        if value.attrib.get('data-hovercard-type') == 'repository':
            NextList.append(value)
    print(len(NextList))
    for value in NextList:
        nextUrl = 'https://github.com' + value.get('href')
        driver = requests.get(url=nextUrl, headers=headers, params=data, proxies=proxy)
        solve(etree.HTML(driver.text), driver)
    time.sleep(3)

if __name__ == '__main__':
    main()
    with open('data.json', 'w') as fw:
        json.dump(OutFile, fw)
