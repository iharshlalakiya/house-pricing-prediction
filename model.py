# -*- coding: utf-8 -*-
"""Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15LaGBR8jo8SeulLW7Ihw68lgt_rSCtAq
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

"""Load dataset"""

from sklearn.datasets import load_boston

boston=load_boston()

boston.keys()

print(boston.DESCR)

print(boston.data)

print(boston.target)

print(boston.feature_names)


"""Preparing the dataset"""

dataset=pd.DataFrame(boston.data,columns=boston.feature_names)

dataset

dataset.info()

dataset['Price']=boston.target

print(dataset)

dataset.info()

dataset.describe()

dataset.isnull().sum()

dataset.corr()

import seaborn as sns

sns.pairplot(dataset)

"""Independent and Dependent features"""

x=dataset.iloc[:,:-1]
y=dataset.iloc[:,-1]

x.head()

y.head()

"""Train test split"""

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)

x_train

x_test

"""Standardize the dataset"""

from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()

x_train=scaler.fit_transform(x_train)

x_test=scaler.fit_transform(x_test)

import pickle
pickle.dump(scaler,open('scaling.pkl','wb'))

x_train

x_test

"""Model Training"""

from sklearn.linear_model import LinearRegression
regression=LinearRegression()

regression.fit(x_train,y_train)

print(regression.coef_)

print(regression.intercept_)

regression.get_params()

## Prediction With Test Data
reg_prediction=regression.predict(x_test)

reg_prediction

"""Assumptions"""

plt.scatter(y_test,reg_prediction)

residuals=y_test-reg_prediction

residuals

sns.displot(residuals,kind="kde")

plt.scatter(reg_prediction,residuals)

from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae

print(mse(y_test,reg_prediction))
print(mae(y_test,reg_prediction))
print(np.sqrt(mse(y_test,reg_prediction)))

"""R square and adjusted R square

Formula

**R^2 = 1 - SSR/SST**


R^2	=	coefficient of determination
SSR	=	sum of squares of residuals
SST	=	total sum of squares
"""

from sklearn.metrics import r2_score
score=r2_score(y_test,reg_prediction) 
score

"""**Adjusted R2 = 1 – [(1-R2)*(n-1)/(n-k-1)]**

where:

R2: The R2 of the model
n: The number of observations
k: The number of predictor variables
"""

r2_score=1 - (1-score)*(len(y_test)-1)/(len(y_test)-x_test.shape[1]-1)
r2_score

"""New Data Prediction"""

boston.data[0].reshape(1,-1)

scaler.transform(boston.data[0].reshape(1,-1))

"""Pickling The Model file For Deployment"""

import pickle

pickle.dump(regression,open('regmodel.pkl','wb'))

pickled_model=pickle.load(open('regmodel.pkl','rb'))

pickled_model.predict(scaler.transform(boston.data[0].reshape(1,-1)))