import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus

#파일불러오기
data=pd.read_csv("movie.csv")

#전처리
for x in range(len(data)):
  try:
    #관객수','제거
    data["관객수"][x]=data["관객수"][x].replace(",","")
    
    #스크린수'.0'제거
    data["스크린수"][x]=data["스크린수"][x].replace(".0","")
    data["스크린수"][x]=data["스크린수"][x].replace(",","")
    
    #개봉일 월 추출
    data["개봉일"][x]=data["개봉일"][x].split("-")[1]
    
  except:
    pass


#결측치 제거
data=data.dropna(axis=0)

#관객수 int형 변환
data["관객수"]= map(int,data["관객수"])
data["스크린수"]= map(int,data["스크린수"])


#관객수 등급 열추가
data.loc[data["관객수"]>0,"관객수 등급"]="G"
data.loc[data["관객수"]>100,"관객수 등급"]="F"
data.loc[data["관객수"]>1000,"관객수 등급"]="E"
data.loc[data["관객수"]>10000,"관객수 등급"]="D"
data.loc[data["관객수"]>100000,"관객수 등급"]="C"
data.loc[data["관객수"]>1000000,"관객수 등급"]="B"
data.loc[data["관객수"]>10000000,"관객수 등급"]="A"

#data

#Dataset
feature_names=["개봉일","스크린수","대표국적","배급사"]
dfX=data[feature_names].copy()
dfy=data["관객수 등급"].copy()
#dfX.info()

#Labeling
dfX["배급사"]=LabelEncoder().fit_transform(dfX["배급사"])
dfX["대표국적"]=LabelEncoder().fit_transform(dfX["대표국적"])

X_train, X_test, y_train, y_test = train_test_split(
     dfX, dfy, test_size=0.2, random_state=0)



# from sklearn.preprocessing import StandardScaler
# import numpy as np
# sc=StandardScaler()
# sc.fit(X_train)

# X_train_std=sc.transform(X_train)
# X_test_std=sc.transform(X_test)



#Make DecisionTree
model = DecisionTreeClassifier(
    criterion='entropy', max_depth=3)
    
model.fit(dfX,dfy)

#Accuracy
y_pred_tr = model.predict(X_test)
print('Accuracy: %.2f' % accuracy_score(y_test, y_pred_tr))

#visualization
dot_data = StringIO()
export_graphviz(model, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())
