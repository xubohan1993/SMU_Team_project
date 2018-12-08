#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
# import requests
import urllib
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
# from selenium.webdriver.common.keys import Keys
import datetime as dt

 
movie_list=['베테랑',
            '암살',
            '부산행',
            '캡틴아메리카 시빌워 OR 시빌워',
            '공조',
            '밀정',
            '마스터',
            '럭키',
            '미션임파서블 OR 미션임파서블 로그네이션',
            '닥터 스트레인지',
            '마션',
            '분노의 질주 OR 분노의 질주 더 익스트림',
            '미이라',
            '인턴',
            '데드풀',
            '스타워즈 OR 스타워즈 깨어난 포스',
            '터미네이터 제네시스',
            '캐리비안의 해적 OR 캐리비안의 해적 죽은 자는 말이 없다',
            '영화 형',
            '엑스맨 아포칼립스',
            '앤트맨',
            '메이즈 러너 OR 메이즈 러너 스코치 트라이얼',
            '가디언즈 오브 갤럭시2 OR 가오갤2']

released_day= [dt.date(2015,8,5),
               dt.date(2015,7,22),
               dt.date(2016,7,20),
               dt.date(2016,4,27),
               dt.date(2017,1,18),
               dt.date(2016,9,7),
               dt.date(2016,12,21),
               dt.date(2016,10,13),
               dt.date(2015,7,30),
               dt.date(2016,10,26),
               dt.date(2015,10,8),
               dt.date(2017,4,12),
               dt.date(2017,6,6),
               dt.date(2015,9,24),
               dt.date(2016,2,17),
               dt.date(2015,12,17),
               dt.date(2015,7,2),
               dt.date(2017,5,24),
               dt.date(2016,11,23),
               dt.date(2016,5,25),
               dt.date(2015,9,3),
               dt.date(2015,9,16),
               dt.date(2017,5,3)]

#firefox 브라우져 다운로드 필요
binary=FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")  
#geckodriver.exe 다운로드 후 본인환경에 맞게 경로 수정
browser=webdriver.Firefox(executable_path='C:/Program Files/geckodriver/geckodriver.exe',firefox_binary=binary) 
    
for i in range(23):
    title = movie_list[i]
    startdate = released_day[i] - dt.timedelta(days=30)
    enddate = released_day[i] + dt.timedelta(days=30)
    
        
    """
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
    """
    
    #startdate=dt.date(year_s,month_s,day_s)
    
    untildate = startdate + dt.timedelta(days=1)
    
    #enddate=dt.date(year_e,month_e,day_e)
    
    url = "https://twitter.com/search?"
    
    totalfreq = []
    tweetContents = []
    
    while not enddate==startdate:
    
        startdate_str=str(startdate)
        untildate_str=str(untildate)
        pre_params= title+" since:"+startdate_str+" until:"+untildate_str
        params=urllib.urlencode({"q":pre_params})
           
        url2=url+params
    
        browser.get(url2)
        # html = browser.page_source
        # soup=BeautifulSoup(html,"html.parser")
    
        lastHeight = browser.execute_script("return document.body.scrollHeight")
            
        wordfreq=0
        dailyfreq={'Date':startdate}
    
        while True:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                newHeight = browser.execute_script("return document.body.scrollHeight")
                time.sleep(1)
                print newHeight
                
                if newHeight != lastHeight:
                    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    #time.sleep(2)
                    pass
                
                #tweets=soup.find_all("p",{"class":"TweetTextSize"})
                #wordfreq += len(tweets)
                #for i in tweets:
                    #dailytweet={}
                    #dailytweet['contents']=i.text.replace(u'\xa0', ' ').replace(u'\u200b', ' ').replace(u'\u0e09' ,' ').replace(u',',' ')
                    #dailytweet['date']=startdate
                    #tweetContents.append(dailytweet)
    
                #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #time.sleep(3)  #인터넷 환경이 좋지 않을 경우, 숫자크기 크게
    
                
    
                else:
                    html = browser.page_source
                    soup= BeautifulSoup(html,"html.parser")
                    tweets=soup.find_all("p",{"class":"TweetTextSize"})
                    wordfreq += len(tweets)
                    for i in tweets:
                        dailytweet={}
                        dailytweet['date']=startdate
                        dailytweet['contents']=i.text.replace(u'\xa0', ' ').replace(u'\u200b', ' ').replace(u'\u0e09' ,' ').replace(u',',' ')
                        tweetContents.append(dailytweet)
                    dailyfreq["Frequancy"]=wordfreq
                    totalfreq.append(dailyfreq)
                    startdate=untildate
                    untildate+=dt.timedelta(days=1)
                    break
    
                #else:
                    #dailyfreq["Frequancy"]=wordfreq
                    #totalfreq.append(dailyfreq)
                    #startdate=untildate
                    #untildate+=dt.timedelta(days=1)
                    #break
    
                lastHeight=newHeight
                
    df1 = pd.DataFrame(totalfreq)
    df2 = pd.DataFrame(tweetContents)
        
    my = os.getcwd()
        
    fileName1 = title+'daily_tweets.csv'
    fileName2 = title+'tweetContents.csv'
        
    # os.getcwd에서 나온 워킹디렉터리에 Movie_twitter 폴더 작성 필요
    file1= os.path.join(my, 'Movie_twitter', fileName1) 
    file2 = os.path.join(my, 'Movie_twitter', fileName2)
    
    df1.to_csv(file1.decode('utf-8'), header=True, index = False, encoding='utf-8')
    df2.to_csv(file2.decode('utf-8'), header=True, index = False, encoding='utf-8')
        
