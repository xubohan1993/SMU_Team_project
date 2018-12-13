import pandas as pd
from sklearn.preprocessing import LabelEncoder

#"순위","매출액","매출액 점유율","국적" remove 및 연도별 영화데이터 merge
year=2005
data=pd.read_csv("2004.csv")
data=data.drop(["순위","매출액","매출액 점유율","국적"],1)

while year<2017:
  n_data=pd.read_csv(str(year)+".csv")
  n_data=n_data.drop(["순위","매출액","매출액 점유율","국적"],1)
  data=pd.concat([data,n_data]) 
  year+=1

#영화데이터 생성
data.to_csv("movie.csv",encoding="utf-8",index=False)
# movie=pd.read_csv("movie.csv")
# movie.head()
