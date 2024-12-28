import pickle

from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


diabetes = datasets.load_diabetes()

X = diabetes.data
Y = diabetes.target

train_x, test_x, train_y, test_y = train_test_split(X,Y,test_size=0.3, random_state=33)

reg = LinearRegression()
reg.fit(train_x,train_y)

with open('model/model.pkl','wb') as f:
    pickle.dump(reg, f)
