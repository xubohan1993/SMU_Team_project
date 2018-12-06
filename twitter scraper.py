#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import urllib
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt

def twitterScraper():
    binary=FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
    browser=webdriver.Firefox(executable_path='/content/geckodriver.exe',firefox_binary=binary)

    print "검색어 입력"
    title = raw_input().decode("cp949").encode("utf-8")

    print "시작 연도 입력"
    year_s = int(raw_input())
    print "시작 월 입력"
    month_s = int(raw_input())
    print "시작 일 입력"
    day_s = int(raw_input())

    
    
    print "종료 연도 입력"
    year_e = int(raw_input())
    print "종료 월 입력"
    month_e = int(raw_input())
    print "종료 일 입력"
    day_e = int(raw_input())


    startdate=dt.date(year_s,month_s,day_s)
    # startdate_str=str(startdate)

    untildate=startdate + dt.timedelta(days=1)
    # untildate_str=str(untildate)

    enddate=dt.date(year_e,month_e,day_e)
    # enddate_str=str(enddate)

    # pre_params= title+" since:"+startdate_str+" until:"+untildate_str 

    url = "https://twitter.com/search?"
    # params=urllib.urlencode({"q":pre_params})
    # headers={
    #   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    # }

    # url2=url+params

    totalfreq = []
    tweetContents = []

    while not enddate==startdate:

        startdate_str=str(startdate)
        untildate_str=str(untildate)
        pre_params= title+" since:"+startdate_str+" until:"+untildate_str
        params=urllib.urlencode({"q":pre_params})
        url2=url+params

        browser.get(url2)
        html = browser.page_source
        soup=BeautifulSoup(html,"html.parser")

        lastHeight = browser.execute_script("return document.body.scrollHeight")
        wordfreq=0

        while True:
                dailyfreq={'Date':startdate}
    #             i=0
                tweets=soup.find_all("p",{"class":"TweetTextSize"})
                wordfreq += len(tweets)
                for i in tweets:
                    dailytweet={}
                    dailytweet['date']=startdate
                    dailytweet['contents']=i.text
                    tweetContents.append(dailytweet)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                newHeight = browser.execute_script("return document.body.scrollHeight")
                print newHeight

                if newHeight != lastHeight:
                    html = browser.page_source
                    soup= BeautifulSoup(html,"html.parser")
                    tweets=soup.find_all("p",{"class":"TweetTextSize"})
                    wordfreq += len(tweets)
                    for i in tweets:
                        dailytweet={}
                        dailytweet['date']=startdate
                        dailytweet['contents']=i.text
                        tweetContents.append(dailytweet)

                else:
                    dailyfreq["Frequancy"]=wordfreq
                    wordfreq=0
                    totalfreq.append(dailyfreq)
                    startdate=untildate
                    untildate+=dt.timedelta(days=1)
                    dailyfreq={}
                    break
    #             i+=1
                lastHeight=newHeight
    
    df1 = pd.DataFrame(totalfreq)
    df2 = pd.DataFrame(tweetContents)
    
    my = os.getcwd()
    
    fileName1 = title+'daily_tweets.csv'
    fileName2 = title+'tweetContents.csv'
    
    file1= os.path.join(my, 'Movie_twitter', fileName1)
    file2 = os.path.join(my, 'Movie_twitter', fileName2)

    df1.to_csv(file1.decode('utf-8'), header=True, index = False, encoding='utf-8')
    df2.to_csv(file2.decode('utf-8'), header=True, index = False, encoding='utf-8')

def main():
    twitterScraper()

if __name__ == '__main__':
    main()

