import sys
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

OutFile = []

def solve(soup,driver):   #应该把所有数据给封装起来
	dict = {}
	Name = soup.find("a",{"data-pjax":"#js-repo-pjax-container"})  #仓库名
	print(Name.string.strip())
	dict.update({"Name":Name.string.strip()})
	About = soup.find("p",{"class":"f4 mt-3"})  #仓库简介
	dict.update({"About":About.string.strip()})
	print(About.string.strip())
	License = soup.find("a",{"class":"Link--muted"})   #开源协议 这里要特殊处理一下找不到的情况
	dict.update({"License":License.text.strip()})
	print(License.text.strip())
	Languages = soup.find_all("span",{"class":"color-text-primary text-bold mr-1"})
	for Language in Languages:
		dict.update({Language.text : Language.find_next_sibling().text})
	NextUrl = 'https://github.com' + soup.find("a",{"class":"pl-3 pr-3 py-3 p-md-0 mt-n3 mb-n3 mr-n3 m-md-0 Link--primary no-underline no-wrap"}).get('href')
	IssuesUrl = 'https://github.com'
	if soup.find("a", {"id": "issues-tab"}) is not None:
		IssuesUrl += soup.find("a", {"id": "issues-tab"}).get('href')
	driver.get(NextUrl)
	soup = BeautifulSoup(driver.page_source,'html.parser')
	Committers = soup.find_all("a",{"class":"commit-author user-mention"})
	CommitMessages = soup.find_all("a",{"class":"Link--primary text-bold js-navigation-open markdown-title"})
	CommitHashs = soup.find_all("a",{"class":"text-mono f6 btn btn-outline BtnGroup-item"})
	for i in range(min(5,len(Committers))):  #前五个提交的信息
		dict.update({"commit " + str(i + 1) : Committers[i].text.strip() + " " + CommitMessages[i].text.strip() + " " + CommitHashs[i].text.strip()})
	if IssuesUrl != 'https://github.com':
		driver.get(IssuesUrl)
		soup = BeautifulSoup(driver.page_source,'html.parser')  #进入issues界面
		IssuesList = soup.find_all("a",{"class":'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'})
		for i in range(min(5,len(IssuesList))):
			Issue = IssuesList[i]
			NextUrl = 'https://github.com' + Issue.get('href')
			driver.get(NextUrl)
			soup = BeautifulSoup(driver.page_source,'html.parser')
			title = soup.find("span",{"class":"js-issue-title markdown-title"}).text.strip()
			Body = ""
			BodyPosition = soup.find("div",{"class":"edit-comment-hide"})
			Bodys = BodyPosition.find_all("p")
			for value in Bodys:
				Body += value.text.strip() + "\n"
			dict.update({"Issue " + str(i + 1) : "Title: " + title + "\n" + "Body: " + Body})

	print(dict)
	OutFile.append(dict)

def main():
	url = 'https://github.com/orgs/apache/repositories'
	driver = webdriver.Chrome()
	driver.get(url)
	soup = BeautifulSoup(driver.page_source,'html.parser')
	List = soup.findAll('a')
	NextList = []
	for value in List:
		if value.get('data-hovercard-type') == 'repository':
			NextList.append(value)
	for value in NextList:
		nextUrl = 'https://github.com' + value.get('href')
		driver.get(nextUrl)
		solve(BeautifulSoup(driver.page_source,'html.parser'),driver)
	time.sleep(10)

if __name__ == '__main__':
	main()
	with open('data.json', 'w') as fw:
		json.dump(OutFile, fw)
