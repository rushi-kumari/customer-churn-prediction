# -*- coding: utf-8 -*-
"""Project_customer_Churn_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FEZqB-hp8j7GoFUMYrz0y0uZqbeTolX_

**Customer Churn Prediction**

"A Bank wants to take care of it’s customer retention for its product."
The bank wants to identify customers likely to churn balances below the minimum balance.

**Data** :

The dataset which can be cleanly divided in 3 categories:

Demographic information about customers:
customer_id 

vintage

age 

gender

dependents

occupation

city 

Customer Bank Relationship:
customer_nw_category 

branch_code

days_since_last_transaction 

Transactional Information :
current_balance 

previous_month_end_balance

average_monthly_balance_prevQ

average_monthly_balance_prevQ2 

current_month_credit 

previous_month_credit 

current_month_debit 

previous_month_debit 

current_month_balance 

previous_month_balance 

churn - Average balance of customer falls below minimum balance in the next quarter (1/0)

**Load Packages**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
#import random as rd
#from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression as LG
from sklearn.metrics import f1_score
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix, roc_curve, precision_score, recall_score, precision_recall_curve
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

#Load Data
df=pd.read_csv('churn_prediction.csv')

df.shape

df.isnull().sum()

"""**Missing Vaue Imputation**"""

df['gender'].fillna(value=df['gender'].mode()[0],inplace=True)

df=df.astype({"customer_nw_category" : 'object',"churn" : 'object'})

df['occupation'].fillna(value=df['occupation'].mode()[0],inplace=True)

df['dependents'].fillna(value=df['dependents'].mode()[0],inplace=True)

df['city'].fillna(value=df['city'].mean(),inplace=True)

df['days_since_last_transaction'].fillna(value=df['days_since_last_transaction'].mean(),inplace=True)

df.shape

df['gender'].value_counts()

df['occupation'].value_counts()

"""**Preprocessing**"""

#Convert Gender
dict_gender = {'Male': 1, 'Female':0}
df.replace({'gender': dict_gender}, inplace = True)

df['gender'] = df['gender'].fillna(-1)

df.shape

df.isnull().sum()

data=pd.get_dummies(df['occupation'])

df=pd.concat([data,df],axis=1)

df.drop(['occupation'],axis=1,inplace=True)

df.head(30)

"""**Normalize**"""

num_cols = ['customer_nw_category', 'current_balance',
            'previous_month_end_balance', 'average_monthly_balance_prevQ2', 'average_monthly_balance_prevQ',
            'current_month_credit','previous_month_credit', 'current_month_debit', 
            'previous_month_debit','current_month_balance', 'previous_month_balance']

#for i in num_cols:
 #   df[i] = np.log(df[i] + 17000)

std = StandardScaler()
scaled = std.fit_transform(df[num_cols])
scaled = pd.DataFrame(scaled,columns=num_cols)

df_df_og = df.copy()
df = df.drop(['customer_nw_category', 'current_balance',
            'previous_month_end_balance', 'average_monthly_balance_prevQ2', 'average_monthly_balance_prevQ',
            'current_month_credit','previous_month_credit', 'current_month_debit', 
            'previous_month_debit','current_month_balance', 'previous_month_balance'],axis = 1)
df = df.merge(scaled,left_index=True,right_index=True,how = "left")

X=df.drop(['churn', 'customer_id'],axis=1)
y=df['churn']

"""Baseline Column"""

baseline_cols = ['current_month_debit', 'previous_month_debit','current_balance','previous_month_end_balance','vintage'
                 ,'retired', 'salaried','self_employed', 'student']

df_baseline = df[baseline_cols]

"""**Train_Test_Split**"""

train_X,test_X,train_y,test_y= train_test_split(df_baseline,y,random_state=56,test_size=0.2,stratify=y)

train_X.shape

test_X.shape

train_y.shape

test_y.shape

"""**Logistic Regression**"""

lg=LG()

train_y.shape

train_y.head(20)

type(train_X)

type(train_y)

train_y=list(train_y)

lg.fit(train_X,train_y)

pred = lg.predict_proba(test_X)[:,1]

"""
f1 score calculation"""

train_predict=lg.predict(train_X)

train_predict

k=f1_score(train_predict,train_y)

print('training f1_score',k)

test_predict=lg.predict(test_X)

test_predict

type(test_predict)

type(test_y)

test_y=list(test_y)

k=f1_score(test_predict,test_y)

print('test_score',k)   #  checking model success

df.head()

"""*cross validation*"""

def cv_score(ml_model, rstate = 12, thres = 0.5, cols = df.columns):
    i = 1
    cv_scores = []
    df1 = df.copy()
    # print(df1[['current_month_debit']].head())
    df1 = df[cols]
    print(df1.head())
    y1 = list(y)
    
     # 5 Fold cross validation stratified on the basis of target
    kf= StratifiedKFold(n_splits=3,random_state=rstate,shuffle=True)
    for df_index,test_index in kf.split(df1,y1):
        print('\n{} of kfold {}'.format(i,kf.n_splits))
        print("{} {}".format(df_index, test_index))
        xtr,xvl = df1.loc[df_index],df1.loc[test_index]
        # ytr,yvl = y1[df_index],y1[test_index]
        ytr = [y1[idx] for idx in df_index]
        yvl = [y1[idx] for idx in test_index]
        
        # Define model for fitting on the training set for each fold
        model = ml_model
        model.fit(xtr, ytr)
        pred_probs = model.predict_proba(xvl)
        pp = []
         
        # Use threshold to define the classes based on probability values
        for j in pred_probs[:,1]:
            if j>thres:
                pp.append(1)
            else:
                pp.append(0)

        # Calculate scores for each fold and print
        pred_val = pp
        roc_score = roc_auc_score(yvl,pred_probs[:,1])
        recall = recall_score(yvl,pred_val)
        precision = precision_score(yvl,pred_val)
        sufix = ""
        msg = ""
        msg += "ROC AUC Score: {}, Recall Score: {:.4f}, Precision Score: {:.4f} ".format(roc_score, recall,precision)
        print("{}".format(msg))
         
         # Save scores
        cv_scores.append(roc_score)
        i+=1
    return cv_scores

baseline_scores = cv_score(lg, cols=baseline_cols)

all_feat_scores = cv_score(LG())

"""**Random Forest**"""

from sklearn.ensemble import RandomForestClassifier

rf_all_features = cv_score(RandomForestClassifier(n_estimators=10, max_depth=3))

"""**Comparison of Different model fold wise**"""

results_df = pd.DataFrame({'baseline':baseline_scores, 'all_feats': all_feat_scores, 'random_forest': rf_all_features})

results_df.plot(y=["baseline", "all_feats", "random_forest"], kind="bar")

"""**Life Cycle of Project**

Loading Packages and Data

Missing Value Imputation using mode value

Preprocessing of data (dummy with mutiple categories to keep data stricty numeric)

Normalize data using standardscalar to avoid outilers

Model building (logistic Regression and Random Forest)

Evauation metrics (f1_score - weighted average of precision and recall and roc_auc_score for logistic Regression)

Metrics roc_auc_score for Random Forest

# Conclusion

Here, we can see that the random forest model is giving the best result for each fold

This model is 99% in agreement with the demand of the actual business model.
"""