import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data=pd.read_csv("movie.csv")
data=data.dropna()
#data.info()

feature_names=["스크린수","대표국적","배급사"]
dfX=data[feature_names].copy()
dfy=data["관객수"].copy()
#dfX.info()

dfX["배급사"]=LabelEncoder().fit_transform(dfX["배급사"])
dfX["대표국적"]=LabelEncoder().fit_transform(dfX["대표국적"])
#dfX


X_train, X_test, y_train, y_test = train_test_split(
    dfX, dfy, test_size=0.3, random_state=0)

model = DecisionTreeClassifier(
    criterion='entropy', max_depth=3, min_samples_leaf=5)
    
model.fit(X_train,y_train)  #error
