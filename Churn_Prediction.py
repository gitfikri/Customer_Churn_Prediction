# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] colab_type="text" id="7goFRawviZgm"
# ## SHIFT ACADEMY

# %% [markdown] colab_type="text" id="64QyQHCMiZgq"
# # HOMEWORK - Machine Learning
# ## Customer Churn Prediction

# %% [markdown] colab_type="text" id="HHzFDkG-iZgt"
# #### Nama : ABDILLAH FIKRI
# #### Email : abdillah.fikri14@gmail.com

# %% [markdown] colab_type="text" id="_bsZbYr-iZgu"
# ___

# %% [markdown] colab_type="text" id="0NNo62MqYEsB"
# # Introduction

# %% [markdown] colab_type="text" id="_REm3p5aWWIK"
# **About the problems**
#
# Customer churn is the loss of clients or
# customers. In order to avoid losing customers, a
# company needs to examine why its customers have left
# in the past and which features are more important to
# determine who will churn in the future. Our task is
# therefore to predict whether customers are about to
# churn and which are the most important features to
# get that prediction right. As in most prediction
# problems, we will use machine learning.

# %% [markdown] colab_type="text" id="8A8I2sVcW9Ya"
# **About the data**
# *   Customers who left within the last month – the column is called Churn
# *   Services that each customer has signed up for – phone, multiple lines, internet, online security, online backup, device protection, tech support, and streaming TV and movies
# *   Customer account information – how long they’ve been a customer, contract, payment method, paperless billing, monthly charges, and total charges
# *   Demographic info about customers – gender, age range, and if they have partners and dependents

# %% [markdown] colab_type="text" id="pK92zibbXnyR"
# # Data Importing and First Lookup

# %% colab_type="code" id="4KZvfSUjRrUK" colab={} outputId="cbe4c6e2-6aba-4ac5-d9af-6b6ecb38815d"
# !pip install seaborn -U

# %% colab_type="code" id="bcJHDkBfN4Ss" colab={}
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set(style='ticks', palette="deep", font_scale=1.1, rc={"figure.figsize": [7, 5]})

# %% colab_type="code" id="bV34x5q-SLt2" colab={"base_uri": "https://localhost:8080/", "height": 309} executionInfo={"elapsed": 3491, "status": "ok", "timestamp": 1600452217316, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="2a922f9b-23e8-4301-8439-114e83c84a8b"
data = pd.read_csv('telco.csv', sep=';')
data.head()

# %% colab_type="code" id="Ra746CMhScMc" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 3463, "status": "ok", "timestamp": 1600452217316, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="2723d54c-7dc7-4577-93cd-cc836df38227"
data.shape

# %% [markdown] colab_type="text" id="_DvBcP4GZfOi"
# Our data contains 7043 observations and 21 variable: <br>
# *   20 independent variables
# *   1 dependent variable with 2 classes
#
#

# %% [markdown] colab_type="text" id="vO2fYxYuagp7"
# Lets look at the data type and missing values

# %% colab_type="code" id="yYCzYcHQSvKR" colab={"base_uri": "https://localhost:8080/", "height": 493} executionInfo={"elapsed": 3439, "status": "ok", "timestamp": 1600452217317, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="8a1b6006-0ed5-4e7c-9524-ebd212c3cad4"
data.info()

# %% [markdown] colab_type="text" id="rzv9D1RwaNOM"
# It have 18 object type (categorical variables), 2 int type (discrete variables), and 1 float type (continuous variable).<br>
# And it looks like we don't have missing values.
#
# There are 2 variables with incorrect type:
# 1.   seniorcitizen : must be object type because it is categorical variable.
# 2.   totalcharges : must be numerical type
#
# We have to change the 1 and 0 values in seniorcitizen to 'Yes' and 'No' accordingly (because the other categorical variables has this value) to have better interpretation when we make visualization.
#
# Next, we want to examine totalcharges why it has an object type.

# %% colab_type="code" id="GJ9gPp1UioVm" colab={}
# Change seniorcitizen column values to Yes and No
map_yesno = {1:'Yes', 0:'No'}
data['seniorcitizen'] = data['seniorcitizen'].map(map_yesno)

# %% colab_type="code" id="tl9l5xGEg2tE" colab={"base_uri": "https://localhost:8080/", "height": 374} executionInfo={"elapsed": 3400, "status": "ok", "timestamp": 1600452217321, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="59dfed38-dc32-4154-e141-192c28e1c2f0"
# Check whether columns value contains  other than numeric and alphabet
for col in data.columns:
  print(col, data.loc[~data[col].astype(str).str.contains(pat='[0-9a-zA-Z]'), col].tolist())

# %% [markdown] colab_type="text" id="cinaWBLQa29h"
# It turns out that the totalcharges column has a value containing ' '(space). This is why the data type is object. <br>
# It is necessary to change the value containing ' '(space) and change the data type to numeric.

# %% colab_type="code" id="HAs0B-n_VT2S" colab={}
# Change data type to numeric
# Nonconvertible value will automatically inputed with NaN
data['totalcharges'] = pd.to_numeric(data['totalcharges'], errors='coerce')

# %% [markdown] colab_type="text" id="keh7Q_KLlcfU"
# After we change the data type, there must be some missing values appear.

# %% colab_type="code" id="eaz_0DocYIVo" colab={"base_uri": "https://localhost:8080/", "height": 391} executionInfo={"elapsed": 3356, "status": "ok", "timestamp": 1600452217322, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="661df71f-76e9-4e5a-acc0-99cf4fa91e84"
data.isna().sum()


# %% [markdown] colab_type="text" id="T0Jjf5E6YSjA"
# Missing values imputation will be done after train test split to avoid information leakage in the test set.

# %% [markdown] colab_type="text" id="pyJmiIzEcUac"
# # Exploratory Data Analysis

# %% [markdown] colab_type="text" id="EbW7Y8TOcaRq"
# ### Preparation

# %% [markdown] colab_type="text" id="S9w0Dso5AKsU"
# Make some function to plot custom visualization.

# %% colab_type="code" id="EdFBpPdosg-B" colab={}
def countplot_annot(nrow, ncol, columns, data, 
                    rotate=None, rcol=None,
                    t_height=25):
  '''
  Function untuk ploting sns.counplot dengan penambahan presentase
  di atas bar. (Versi tanpa hue)
  '''
  for index, col in enumerate(columns):
    plt.subplot(nrow, ncol, index + 1)

    order = sorted(data[col].unique())
    ax = sns.countplot(data=data, x=col, order=order)
    ax.set_ylabel('')

    if rotate != None:
      if col in rcol:
        plt.xticks(rotation=rotate)

    total = len(data)
    for p in ax.patches:
      ax.text(p.get_x() + p.get_width()/2., p.get_height() + t_height, 
              '{:.1f}%'.format(100*p.get_height()/total), ha="center")

def countplot_annot_hue(nrow, ncol, columns, hue, data,
                        rotate=None, rcol=None,
                        t_height=30):
  '''
  Function untuk ploting sns.counplot dengan penambahan presentase
  di atas bar. (Versi dengan hue)
  '''
  for index, col in enumerate(columns):
    plt.subplot(nrow, ncol, index + 1)

    order = sorted(data[col].unique())
    ax = sns.countplot(data=data, x=col, hue=hue, order=order)
    ax.set_ylabel('')
    
    if rotate != None:
      if col in rcol:
        plt.xticks(rotation=rotate)

    bars = ax.patches
    half = int(len(bars)/2)
    left_bars = bars[:half]
    right_bars = bars[half:]

    for left, right in zip(left_bars, right_bars):
        height_l = left.get_height()
        height_r = right.get_height()
        total = height_l + height_r

        ax.text(left.get_x() + left.get_width()/2., height_l + t_height, 
                '{0:.0%}'.format(height_l/total), ha="center")
        ax.text(right.get_x() + right.get_width()/2., height_r + t_height, 
                '{0:.0%}'.format(height_r/total), ha="center")



# %% [markdown] colab_type="text" id="4qu6ouzdcuDD"
# Divide columns to their category to make easier visualization.

# %% colab_type="code" id="pOzeqGSJS3QF" colab={"base_uri": "https://localhost:8080/", "height": 493} executionInfo={"elapsed": 3318, "status": "ok", "timestamp": 1600452217324, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="3952762f-8f8a-4956-d2af-9cf81c9584b1"
for col in data.columns:
  print(col, data[col].unique())

# %% colab_type="code" id="RDVH5DqjZX0W" colab={}
num_cols = ['tenure', 'monthlycharges', 'totalcharges']
cat_cols = [col for col in data.columns if col not in num_cols + ['customerid', 'churn']]
target_col = 'churn'

# %% colab_type="code" id="bE-d9fziaGck" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 3681, "status": "ok", "timestamp": 1600452217727, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="72f312b8-b4f2-43e8-d4ce-4533016bbd6b"
data.shape

# %% colab_type="code" id="PAxug4BmaI1N" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 3653, "status": "ok", "timestamp": 1600452217728, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="6a4793b4-884e-437a-835f-610c9df3b842"
len(num_cols + cat_cols + [target_col])

# %% [markdown] colab_type="text" id="WUtTXtFDdPeC"
# ### Univariate Analysis

# %% [markdown] colab_type="text" id="TFLdLmKjenDr"
# #### Target Class

# %% colab_type="code" id="61V9AVkJdcYN" colab={"base_uri": "https://localhost:8080/", "height": 342} executionInfo={"elapsed": 3618, "status": "ok", "timestamp": 1600452217729, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="64ff2e8a-9245-4b1b-fd26-3013dc580a28"
countplot_annot(1, 1, columns=[target_col], data=data)

# %% [markdown] colab_type="text" id="BIlSBGaSfM_O"
# Our data have slightly imbalance class distribution. It will cause a model hard to identify the minority class.
#
# *   No (Non Churn) : 73.5%
# *   Yes (Churn) : 26.5%
#
# **Consideration :** <br>
# Required to tune the model or do resampling to meet our objective (detect the minority class).

# %% [markdown] colab_type="text" id="ExwrFABjevVA"
# #### Numerical Features

# %% colab_type="code" id="SL2-bj9zi3BX" colab={"base_uri": "https://localhost:8080/", "height": 297} executionInfo={"elapsed": 3579, "status": "ok", "timestamp": 1600452217730, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="3e011791-7cff-434b-9029-c98708ebe32d"
data[num_cols].describe()

# %% colab_type="code" id="SLQ5PrN2dtze" colab={"base_uri": "https://localhost:8080/", "height": 506} executionInfo={"elapsed": 4753, "status": "ok", "timestamp": 1600452218946, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="07efbc4c-6ff7-4eb0-d97f-ed89a0625040"
plt.figure(figsize=(15,7))
for i, col in enumerate(num_cols):
  plt.subplot(2,3,i+1)
  sns.kdeplot(data=data, x=col, fill=True)
for i, col in enumerate(num_cols):
  plt.subplot(2,3,i+4)
  sns.boxplot(data=data, x=col)
plt.tight_layout()

# %% [markdown] colab_type="text" id="GMPpTIkBAZ3K"
# * Tenure and monthly charges have a bimodal distribution. Meanwhile, total charges feature  has highly right skewed distribution.
# * There are many outliers on total charges feature.

# %% [markdown] colab_type="text" id="mYJeOpB2e55a"
# #### Categorical Features

# %% colab_type="code" id="phnmBYdknNic" colab={"base_uri": "https://localhost:8080/", "height": 722} executionInfo={"elapsed": 5566, "status": "ok", "timestamp": 1600452219823, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="3a08a261-bab1-4df7-e8f3-568a0dbdb6f6"
plt.figure(figsize=(20,10))
countplot_annot(2, 4, cat_cols[:8], data)
plt.tight_layout()

# %% [markdown] colab_type="text" id="5MEN80vkBDzi"
# From this visualization we got much information about our data.
# *   Most of customer are from Germany (96%).
# *   Proportion of Male and Female customer is about the same.
# *   Senior citizen is minority here (just 16.2%).
# *   Customer who do not have partner slighly have more proportion.
# *   Most of customer do not have dependents (70%).
# *   Most of customer has a phone service (90.3%).
# *   Customer who has multiple lines are slighly lower tha who don't.
# *   44% of customers registered to Fiber Optic, 34.4% to DSL, and 21.7% who do not register to internet service. 

# %% colab_type="code" id="8HbpREjLtIQs" colab={"base_uri": "https://localhost:8080/", "height": 722} executionInfo={"elapsed": 6360, "status": "ok", "timestamp": 1600452220650, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="2d4e5753-231f-4cd8-f434-6cc03c31e268"
plt.figure(figsize=(20,10))
countplot_annot(2, 4, cat_cols[8:], data,
                rotate=25, rcol=['paymentmethod'])
plt.tight_layout()

# %% [markdown] colab_type="text" id="m7syQZNJEY10"
# Lets do for the rest
# * Many customers don't have online security, online backup, device protection and tech support compared to those who do.
# * Most of the customers use paper less billing and pay by electronic check.
#
#

# %% [markdown] colab_type="text" id="gzIYtsEIwpXp"
# ### Multivariate Analysis

# %% [markdown] colab_type="text" id="3Ks2IjjAEPT8"
# #### Numerical Features

# %% colab_type="code" id="Ev6qZl6gG7ut" colab={"base_uri": "https://localhost:8080/", "height": 294} executionInfo={"elapsed": 7169, "status": "ok", "timestamp": 1600452221486, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="8bbadb74-4653-4d5c-da9f-940ea9e338a4"
plt.figure(figsize=(15,4))
for i, col in enumerate(num_cols):
  plt.subplot(1,3,i+1)
  sns.kdeplot(data=data, x=col, hue=target_col,
              multiple='stack')
plt.tight_layout()

# %% [markdown] colab_type="text" id="jyGA9KRYIjFR"
# * In feature tenure and monthly charges, negative (non churn) class has a bimodal distribution, while positive class does not.
# * As for total charges, the distribution between the two classes is similar.

# %% colab_type="code" id="GD2aMj-Sx5_U" colab={"base_uri": "https://localhost:8080/", "height": 290} executionInfo={"elapsed": 7588, "status": "ok", "timestamp": 1600452221937, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="c59e285a-30b8-4cdf-e6b1-c94d170f04eb"
plt.figure(figsize=(15,4))
for i, col in enumerate(num_cols):
  plt.subplot(1,3,i+1)
  sns.boxplot(data=data, x=target_col, y=col)
plt.tight_layout()

# %% colab_type="code" id="FLybZgE0BsQP" colab={"base_uri": "https://localhost:8080/", "height": 290} executionInfo={"elapsed": 7973, "status": "ok", "timestamp": 1600452222365, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="7bc0cd7a-b137-45a0-8257-a830e131de4b"
plt.figure(figsize=(15,4))
for i, col in enumerate(num_cols):
  plt.subplot(1,3,i+1)
  sns.barplot(data=data.dropna(), x=target_col, y=col)
plt.tight_layout()

# %% [markdown] colab_type="text" id="300x3lqYBcZ5"
# From the comparison of the independent and dependent numerical variables above on average it can be concluded:
# * Customers with low tenure tend to have higher churn
# * Customers with high monthly charges tend to have higher churn
# * Customers with lower total charges tend to have higher churn

# %% [markdown] colab_type="text" id="NXVUF3GQESPk"
# #### Categorical Features

# %% colab_type="code" id="NFopUfFMYT9i" colab={"base_uri": "https://localhost:8080/", "height": 721} executionInfo={"elapsed": 9739, "status": "ok", "timestamp": 1600452224163, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="a0ab839f-b956-4576-8659-1667466778a2"
plt.figure(figsize=(20,10))
countplot_annot_hue(2, 4, columns=cat_cols[:8], hue=target_col, data=data)
plt.tight_layout()

# %% [markdown] colab_type="text" id="yHvFDSaOb6BP"
# *   From this comparation, the tendency for churn are more occurs on customers from the senior citizens, who do not have a partner, and who do not have dependents.
# *   In addition, customers who subscribe to fiber optic have a higher churn rate when compared to other services.

# %% colab_type="code" id="5rEim7kEf1Xg" colab={"base_uri": "https://localhost:8080/", "height": 722} executionInfo={"elapsed": 11567, "status": "ok", "timestamp": 1600452226016, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="545f08bb-c398-4062-a634-62eea487b6af"
plt.figure(figsize=(20,10))
countplot_annot_hue(2, 4, columns=cat_cols[8:], hue=target_col, data=data,
                rotate=25, rcol=['paymentmethod'], t_height=15)
plt.tight_layout()

# %% [markdown] colab_type="text" id="e9JkMygff8vA"
# * Customers who do not subscribe to online security, online backup, device protection, and tech support have a higher churn rate when compared to customers who subscribe to this service.
#
# * In streaming tv and streaming movies services, there is no significant difference between customers who churn and those who don't. (4% different)
#
# * In terms of payment, it appears that customers who using paper less billing and electronic check payment methods have higher churn.

# %% [markdown] colab_type="text" id="bVQp2skJMwuP"
# #### Features Corelation

# %% colab_type="code" id="3CsTpULnxUJI" colab={}
mapping = {'Yes' : 1, 'No' : 0}
data[target_col] = data[target_col].map(mapping)

# %% colab_type="code" id="gtGpG8CAuDD_" colab={"base_uri": "https://localhost:8080/", "height": 173} executionInfo={"elapsed": 11529, "status": "ok", "timestamp": 1600452226020, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="fc23bf24-5446-4616-c54b-c58b410d6d63"
data[num_cols + [target_col]].corr()

# %% colab_type="code" id="feKdg6Qlw_Gp" colab={"base_uri": "https://localhost:8080/", "height": 432} executionInfo={"elapsed": 11500, "status": "ok", "timestamp": 1600452226022, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="5fffe577-b036-4eaf-bb67-bfbce525c34a"
sns.heatmap(data[num_cols + [target_col]].corr(), annot=True, linewidths=.5, fmt= '.2f')

# %% colab_type="code" id="qEq65GszT1DK" colab={"base_uri": "https://localhost:8080/", "height": 776} executionInfo={"elapsed": 18341, "status": "ok", "timestamp": 1600452232892, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="ef550992-6a68-4c53-aff0-adfcb1bed245"
sns.pairplot(data[num_cols + [target_col]], hue=target_col, height=3.5, aspect=1.4)

# %% [markdown] colab_type="text" id="GWtU2JXVNLe5"
# * Tenure and total charges have a strong positive correlation.
# * The monthly charges and total charges features have a positive correlation.
# * Meanwhile, tenure and monthly charges have a weak positive correlation.

# %% [markdown] colab_type="text" id="FjVrOGZoXbJX"
# We can see some outliers that are very far away from the data set. <br>
# Judging from the data distribution, it is possible that these outliers were caused by input errors.
#
# Outlier handling will be carried out at the data processing step after this.

# %% [markdown] colab_type="text" id="b4gZByzckAiq"
# # Data Processing

# %% [markdown] colab_type="text" id="z1qC2j_9l5g-"
# ### Train Test Split

# %% colab_type="code" id="3pAWiFp8l2jC" colab={}
from sklearn.model_selection import train_test_split

# %% colab_type="code" id="oQlFHyWTmHYJ" colab={}
train, test = train_test_split(data[num_cols + cat_cols + [target_col]],
                               test_size=0.2, random_state=14)

# %% colab_type="code" id="zHs2PdYee_x7" colab={"base_uri": "https://localhost:8080/", "height": 342} executionInfo={"elapsed": 18297, "status": "ok", "timestamp": 1600452232898, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="0fd76453-dc9c-44ec-ec7d-f9faeffdccf0"
countplot_annot(1, 1, columns=[target_col], data=train)

# %% colab_type="code" id="15GFh0Hne_h8" colab={"base_uri": "https://localhost:8080/", "height": 342} executionInfo={"elapsed": 18261, "status": "ok", "timestamp": 1600452232900, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="ca5e4b7d-02d4-40a1-a702-13bb34bc3ba0"
countplot_annot(1, 1, columns=[target_col], data=test, t_height=5)

# %% [markdown] colab_type="text" id="eRdNLqcem-r1"
# ### Outlier Handling

# %% [markdown] colab_type="text" id="NpYZJHzqVnuf"
# We will remove this outlier with a threshold of 10000 for total charges and 80 for tenure. <br>
# Outliers above those values will be discarded from the data set.

# %% [markdown] id="-0pZQ8BWqTSK" colab_type="text"
# ##### Before remove outlier

# %% colab_type="code" id="Nzphx-honCps" colab={"base_uri": "https://localhost:8080/", "height": 776} executionInfo={"elapsed": 21635, "status": "ok", "timestamp": 1600452236299, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="b5b5b3c4-3ed0-4b4d-c5c6-b4a93093fdad"
sns.pairplot(train[num_cols], height=2.5, aspect=1.4)

# %% colab_type="code" id="jOmcRT3UkTzB" colab={}
train = train.drop(index=train[train['tenure']>80].index)
train = train.drop(index=train[train['totalcharges']>10000].index)

test = test.drop(index=test[test['tenure']>80].index)
test = test.drop(index=test[test['totalcharges']>10000].index)

# %% [markdown] id="bBRXlxdeqTST" colab_type="text"
# ##### After remove outlier

# %% colab_type="code" id="vSdVCM9fpSN8" colab={"base_uri": "https://localhost:8080/", "height": 776} executionInfo={"elapsed": 25541, "status": "ok", "timestamp": 1600452240248, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="17e0a13b-cf90-4835-cf66-8559609e6e86"
sns.pairplot(train[num_cols], height=2.5, aspect=1.4)

# %% [markdown] colab_type="text" id="3hqGYNEwoIIq"
# ### Missing Value Handling

# %% colab_type="code" id="iDxvyJCjoMst" colab={}
from sklearn.impute import SimpleImputer

# %% colab_type="code" id="5iwyS3aDofKO" colab={"base_uri": "https://localhost:8080/", "height": 165} executionInfo={"elapsed": 25504, "status": "ok", "timestamp": 1600452240250, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="021b467f-c727-4636-b6e5-e28b59fdda6d"
na_col = pd.DataFrame(train.isna().sum()) / train.shape[0]*100
na_col.columns = ['NA Train']
na_col['NA Test'] = test.isna().sum().values / test.shape[0]*100
round(na_col.sort_values(by='NA Train', ascending=False).T, 2)

# %% colab_type="code" id="chTbyWp3qBQB" colab={"base_uri": "https://localhost:8080/", "height": 358} executionInfo={"elapsed": 25484, "status": "ok", "timestamp": 1600452240251, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="a2773352-aba4-40d4-e449-0b5f151ca844"
sns.violinplot(data=train, y='totalcharges', x=target_col)
plt.title('Total Charges distribution')
plt.show()

# %% [markdown] colab_type="text" id="1tm06lSIRE6L"
# Because total charges feature have highly right skewed distribution, missing value imputation will be done with median value.

# %% colab_type="code" id="x-iDPX-iqKmB" colab={}
imputer = SimpleImputer(strategy='median')
train['totalcharges'] = imputer.fit_transform(train['totalcharges'].values.reshape(-1, 1))
test['totalcharges'] = imputer.transform(test['totalcharges'].values.reshape(-1, 1))

# %% colab_type="code" id="p7bqrZBkreO5" colab={"base_uri": "https://localhost:8080/", "height": 165} executionInfo={"elapsed": 25453, "status": "ok", "timestamp": 1600452240252, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="db7ef546-e3c4-46cb-8066-f48be9d04a2f"
na_col = pd.DataFrame(train.isna().sum()) / train.shape[0]*100
na_col.columns = ['NA Train']
na_col['NA Test'] = test.isna().sum().values / test.shape[0]*100
round(na_col.sort_values(by='NA Train', ascending=False).T, 2)


# %% [markdown] colab_type="text" id="UaK-U9kWwL4f"
# ### Feature Enginering

# %% [markdown] colab_type="text" id="yqPqcZjkTRCi"
# Make categorize (binning) for tenure feature.

# %% colab_type="code" id="kBagmPJGuLig" colab={}
def tenure_bin(df):
  if df['tenure'] <= 12:
    return '0-1 year'
  elif df['tenure'] > 12 and df['tenure'] <= 24:
    return '1-2 year'
  elif df['tenure'] > 24 and df['tenure'] <= 36:
    return '2-3 year'
  elif df['tenure'] > 36 and df['tenure'] <= 48:
    return '3-4 year'
  elif df['tenure'] > 48 and df['tenure'] <= 60:
    return '4-5 year'
  elif df['tenure'] > 60:
    return '5-6 year'


# %% colab_type="code" id="jgrh9kRzvbQd" colab={}
train['tenure_bin'] = train.apply(lambda x: tenure_bin(x), axis=1)
test['tenure_bin'] = test.apply(lambda x: tenure_bin(x), axis=1)

# %% colab_type="code" id="U9V-s8Tyw-gm" colab={"base_uri": "https://localhost:8080/", "height": 397} executionInfo={"elapsed": 25409, "status": "ok", "timestamp": 1600452240254, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="a964a309-2f76-41b3-db4a-af4a79b6ef1d"
plt.figure(figsize=(10,6))
countplot_annot_hue(1,1, columns=['tenure_bin'], hue=target_col, data=train,
                    t_height=5)

# %% [markdown] colab_type="text" id="s9cTjvKoSEyw"
# With binning, we can more clearly see the distribution comparison on tenure feature. <br>
# Customers with tenure less than 1 year tend to have higher churn compare to the other.

# %% [markdown] colab_type="text" id="AkRo-_aFsemH"
# ### Categorical Encoding

# %% colab_type="code" id="n-ArMLKjstAi" colab={}
map_yn = {'Yes': 1, 'No': 0}
map_gender = {'Male': 1, 'Female': 0}
map_tenure = {'0-1 year': 1,
              '1-2 year': 2,
              '2-3 year': 3,
              '3-4 year': 4,
              '4-5 year': 5,
              '5-6 year': 6}

# %% colab_type="code" id="1vA0mUdQtmzM" colab={}
for col in ['seniorcitizen', 'partner', 'dependents', 'phoneservice', 'paperlessbilling']:
  train[col] = train[col].map(map_yn)
  test[col] = test[col].map(map_yn)

train['gender'] = train['gender'].map(map_gender)
test['gender'] = test['gender'].map(map_gender)

train['tenure_bin'] = train['tenure_bin'].map(map_tenure)
test['tenure_bin'] = test['tenure_bin'].map(map_tenure)

# %% colab_type="code" id="tAPeNXrKv8op" colab={}
train = pd.get_dummies(train)
test = pd.get_dummies(test)

# %% colab_type="code" id="v3Y4ArR2woE9" colab={"base_uri": "https://localhost:8080/", "height": 258} executionInfo={"elapsed": 25357, "status": "ok", "timestamp": 1600452240256, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="790a8f49-482c-483b-e4fa-aa59c9b0744d"
train.head()

# %% [markdown] colab_type="text" id="1geqxzn4r25t"
# ### Scaling

# %% colab_type="code" id="7gKqQWtGr6Rc" colab={}
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# %% colab_type="code" id="RjKfqo8q1ACH" colab={}
features = [col for col in train.columns if col != 'churn']
X_train = train[features]
y_train = train['churn']

X_test = test[features]
y_test = test['churn']

# %% colab_type="code" id="743UaChzsLGc" colab={}
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

# %% [markdown] colab_type="text" id="frcunsSfrz27"
# # Modeling

# %% [markdown] colab_type="text" id="wx_gfElHThfc"
# At this modeling step we will use 4 machine learning, namely:
#
# 1. Logistic Regression
# 2. Desicion Tree
# 3. K-Neirest Neighbors
# 4. XGBoost Classifier
#
# We will compare the performance of several models.

# %% [markdown] colab_type="text" id="DzmAfCINXhwl"
# Because we have imbalanced classes, we will focus on roc auc score with higher recall.
#
# In situations where we want to detect instances of a minority class, we are usually concerned more so with recall than precision, as in the context of detection, it is usually more costly to miss a positive instance than to falsely label a negative instance.

# %% [markdown] colab_type="text" id="xPAoQUGmxeoA"
# ### Preparation

# %% colab_type="code" id="voV1KUHQr1jy" colab={}
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn import metrics


# %% colab_type="code" id="-Li0Jj1UnJOp" colab={}
def make_confusion_matrix(cf,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          figsize=None,
                          cmap='Blues',
                          title=None):
    '''
    This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.
    Arguments
    ---------
    cf:            confusion matrix to be passed in
    group_names:   List of strings that represent the labels row by row to be shown in each square.
    categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
    count:         If True, show the raw number in the confusion matrix. Default is True.
    normalize:     If True, show the proportions for each category. Default is True.
    cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                   Default is True.
    xyticks:       If True, show x and y ticks. Default is True.
    xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
    sum_stats:     If True, display summary statistics below the figure. Default is True.
    figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
    cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                   See http://matplotlib.org/examples/color/colormaps_reference.html
                   
    title:         Title for the heatmap. Default is None.
    '''


    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names)==cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        group_percentages = ["{0:.2%}".format(value) for value in cf.flatten()/np.sum(cf)]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels,group_counts,group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0],cf.shape[1])


    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if sum_stats:
        #Accuracy is sum of diagonal divided by total observations
        accuracy  = np.trace(cf) / float(np.sum(cf))

        #if it is a binary confusion matrix, show some more stats
        if len(cf)==2:
            #Metrics for Binary Confusion Matrices
            precision = cf[1,1] / sum(cf[:,1])
            recall    = cf[1,1] / sum(cf[1,:])
            f1_score  = 2*precision*recall / (precision + recall)
            stats_text = "\n\nPrecision={:0.3f} | Recall={:0.3f}\nAccuracy={:0.3f} | F1 Score={:0.3f}".format(
                precision, recall, accuracy, f1_score)
        else:
            stats_text = "\n\nAccuracy={:0.3f}".format(accuracy)
    else:
        stats_text = ""


    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if figsize==None:
        #Get default figure size if not set
        figsize = plt.rcParams.get('figure.figsize')

    if xyticks==False:
        #Do not show categories if xyticks is False
        categories=False


    # MAKE THE HEATMAP VISUALIZATION
    plt.figure(figsize=figsize)
    plt.subplot(1,2,1)
    sns.heatmap(cf,annot=box_labels,fmt="",cmap=cmap,cbar=cbar,xticklabels=categories,yticklabels=categories)

    if xyplotlabels:
        plt.ylabel('True label')
        plt.xlabel('Predicted label' + stats_text)
    else:
        plt.xlabel(stats_text)
    
    if title:
        plt.title(title)


# %% colab_type="code" id="6JxuujbbxOZv" colab={}
def model_eval(model, X_train, y_train, 
               scoring_='roc_auc', cv_=5):
  
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    train_predprob = model.predict_proba(X_train)[:,1]
           
    cv_score = cross_val_score(model, X_train, y_train, cv=cv_, scoring=scoring_)
    print('Model Report on Train and CV Set:')
    print('--------')
    print('Train Accuracy: {:0.6f}'.format(metrics.accuracy_score(y_train, train_pred)))
    print('Train AUC Score: {:0.6f}'.format(metrics.roc_auc_score(y_train, train_predprob)))
    print('CV AUC Score: Mean - {:0.6f} | Std - {:0.6f} | Min - {:0.6f} | Max - {:0.6f} \n'.format(
        np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score)))


# %% colab_type="code" id="Bo_XfZGPuJ4f" colab={}
def test_eval(model, X_test, y_test):

    pred = model.predict(X_test)
    predprob = model.predict_proba(X_test)[:,1]
    
    print('Model Report on Test Set:')
    print('--------')
    print('Classification Report \n', metrics.classification_report(y_test, pred))

    conf = metrics.confusion_matrix(y_test, pred)
    group_names = ['True Negative', 'False Positive', 'False Negtive', 'True Positive']
    make_confusion_matrix(conf, percent=False, group_names=group_names,
                          figsize=(14,5), title='Confusion Matrix')

    plt.subplot(1,2,2)
    fpr, tpr, _ = metrics.roc_curve(y_test, predprob)
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve\nAUC Score: {:0.3f}'.format(metrics.roc_auc_score(y_test, predprob)))
    plt.legend()


# %% [markdown] colab_type="text" id="pc5Roz_OxzrD"
# ### Model Fitting and Evaluation

# %% [markdown] colab_type="text" id="tQtnxdDuyDEv"
# #### Logistic Regression

# %% colab_type="code" id="ee_kpf_62e4i" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 27164, "status": "ok", "timestamp": 1600452242163, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="2038c5ef-1468-4ca1-adfc-f8ad8899589e"
lr = LogisticRegression(max_iter=9999)
model_eval(lr, X_train_sc, y_train)

# %% colab_type="code" id="VjptOCT4ul0u" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 27144, "status": "ok", "timestamp": 1600452242164, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="d665b0cf-0f3d-4d28-fa1f-a491d913da5d"
test_eval(lr, X_test_sc, y_test)

# %% [markdown] colab_type="text" id="HUWT6Vqwx86R"
# #### Desicion Tree

# %% colab_type="code" id="wy77y0UFxUCM" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 27110, "status": "ok", "timestamp": 1600452242164, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="12e90f3a-e0af-4e14-b648-05055b52a707"
tree = DecisionTreeClassifier()
model_eval(tree, X_train, y_train)

# %% colab_type="code" id="bjwwj7ZovGNN" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 27070, "status": "ok", "timestamp": 1600452242165, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="30044c1a-091f-47e7-f8e7-f7d1487dc38b"
test_eval(tree, X_test, y_test)

# %% [markdown] colab_type="text" id="SXdRTXCpyD-9"
# #### K-Neirest Neighbors

# %% colab_type="code" id="EjvdA4St38BB" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 31311, "status": "ok", "timestamp": 1600452246442, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="6f41a46d-4253-4b15-ece8-62bc7beece96"
knn = KNeighborsClassifier()
model_eval(knn, X_train_sc, y_train)

# %% colab_type="code" id="mcbCXdt_vSKX" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 32847, "status": "ok", "timestamp": 1600452248020, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="27852542-ba94-4dd9-8d8b-a895ec09e35b"
test_eval(knn, X_test_sc, y_test)

# %% [markdown] colab_type="text" id="d4oSlPdVyEj9"
# #### XGBoost Classifier

# %% colab_type="code" id="7WSpfF9O4Ysi" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 35343, "status": "ok", "timestamp": 1600452250543, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="cae34625-8670-4bf1-ca04-33beca47fe06"
xgb_clf = XGBClassifier(tree_method='gpu_hist',
                        seed=14)
model_eval(xgb_clf, X_train, y_train)

# %% colab_type="code" id="RRojhIN2Nvav" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 36312, "status": "ok", "timestamp": 1600452251535, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="12bb3cb9-774d-4c85-c1ff-982b7f3fc75d"
test_eval(xgb_clf, X_test, y_test)

# %% id="lQ5kvZ4yqTTs" colab_type="code" colab={} outputId="cb285901-54e9-41b4-a57a-ac613014ca25"
plt.figure(figsize=(20,15))
xgb.plot_importance(xgb_clf, ax=plt.gca())

# %% [markdown] colab_type="text" id="5b5d5mbIXGGg"
# **Summary**:
# * Logistic Regression has pretty good results, neither overfit nor underfit (CV AUC 0.837), but recall is only 0.52
# * Desicion Tree is too overfit in the training set
# * KNN results are quite good (slightly overfit on the traning set), but the AUC score is still far below the Logistic Regression
# * XGBoost results are similar to Logistic Regression with slightly superior CV AUC score of 0.839
#
#

# %% [markdown] colab_type="text" id="bTPo2PZ3c1LJ"
# Without tuning, all models struggled to detect positive classes with an average recall around 0.5

# %% [markdown] colab_type="text" id="1Kw7WuS5w_OV"
# ##### Hyperparameter Tunning

# %% colab_type="code" id="20XWZeYa1FUR" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 32259, "status": "ok", "timestamp": 1600325833132, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="4526c797-6659-4117-e6fa-4e34493eade1"
# Step 1: Get initial fix learning_rate and n_estimators
test1 = {'n_estimators':range(20,101,10)}
grid1 = GridSearchCV(estimator = XGBClassifier(learning_rate =0.05, 
                                               max_depth=5, 
                                               min_child_weight=1, 
                                               gamma=0, 
                                               subsample=0.8, 
                                               colsample_bytree=0.8,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=1, 
                                               seed=14,
                                               tree_method='gpu_hist'), 
                                               param_grid = test1, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid1.fit(X_train, y_train)
grid1.best_params_, grid1.best_score_

# %% colab_type="code" id="sdTj3FFS2Ktp" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 68341, "status": "ok", "timestamp": 1600326257892, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="898e6a85-ba0c-4ef2-88e7-79eba0e272e5"
# Step 2: Tune max_depth and min_child_weight
test2 = {'max_depth': range(3,10,2),
         'min_child_weight': range(1,6,2)}
grid2 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.05,
                                               n_estimators=70,
                                               max_depth=5, 
                                               min_child_weight=1, 
                                               gamma=0, 
                                               subsample=0.8, 
                                               colsample_bytree=0.8,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=1, 
                                               seed=14, 
                                               tree_method='gpu_hist'), 
                                               param_grid = test2, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid2.fit(X_train, y_train)
grid2.best_params_, grid2.best_score_

# %% colab_type="code" id="IVJqixKa2Qi5" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 37041, "status": "ok", "timestamp": 1600326461592, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="3bf6125e-243b-4620-82e1-6a8f7a90d72f"
# Step 2b: Tune max_depth and min_child_weight
test2 = {'max_depth': [4,5,6],
         'min_child_weight': [4,5,6]}
grid2 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.05,
                                               n_estimators=70,
                                               max_depth=5, 
                                               min_child_weight=5, 
                                               gamma=0, 
                                               subsample=0.8, 
                                               colsample_bytree=0.8,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=1, 
                                               seed=14, 
                                               tree_method='gpu_hist'),  
                                               param_grid = test2, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid2.fit(X_train, y_train)
grid2.best_params_, grid2.best_score_

# %% colab_type="code" id="RGiWtG_r2QWu" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 17856, "status": "ok", "timestamp": 1600326488650, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="1822aa32-e230-4eb5-d902-fe6a2e42ea7a"
# Step 3: Tune gamma
test3 = {'gamma': [i/10.0 for i in range(0,5)]}
grid3 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.05,
                                               n_estimators=70,
                                               max_depth=4, 
                                               min_child_weight=6, 
                                               gamma=0, 
                                               subsample=0.8, 
                                               colsample_bytree=0.8,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=1, 
                                               seed=14, 
                                               tree_method='gpu_hist'),  
                                               param_grid = test3, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid3.fit(X_train, y_train)
grid3.best_params_, grid3.best_score_

# %% colab_type="code" id="iUXhuxLd2QJx" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 51686, "status": "ok", "timestamp": 1600326577630, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="ec7708b2-e5cf-4a82-a3d0-228c6492cb89"
# Step 4: Tune subsample and colsample_bytree
test4 = {'subsample':[i/10.0 for i in range(6,10)],
         'colsample_bytree':[i/10.0 for i in range(6,10)]}
grid4 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.05,
                                               n_estimators=70,
                                               max_depth=4, 
                                               min_child_weight=6, 
                                               gamma=0, 
                                               subsample=0.8, 
                                               colsample_bytree=0.8,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=1, 
                                               seed=14, 
                                               tree_method='gpu_hist'), 
                                               param_grid = test4, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid4.fit(X_train, y_train)
grid4.best_params_, grid4.best_score_

# %% colab_type="code" id="4KsKxFvQ2P2l" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 32415, "status": "ok", "timestamp": 1600326678668, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="b5368b4e-223f-4c3e-f761-7055aedf3edf"
# Step 5: Tuning scale_pos_weight
test5 = {'scale_pos_weight': [i/10 for i in range(1,11)]}
grid5 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.05,
                                               n_estimators=70,
                                               max_depth=4, 
                                               min_child_weight=6, 
                                               gamma=0, 
                                               subsample=0.7, 
                                               colsample_bytree=0.6,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=1, 
                                               seed=14, 
                                               tree_method='gpu_hist'), 
                                               param_grid = test5, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid5.fit(X_train, y_train)
grid5.best_params_, grid5.best_score_

# %% colab_type="code" id="eb5r91dZ544Z" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 95947, "status": "ok", "timestamp": 1600326882880, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="b3d0f2a0-fcd8-4409-ec1c-dd5c6937efe1"
# Step 6: Tuning n_estimators and learning_rate
test6 = {'learning_rate': [0.005],
         'n_estimators': range(100,1001,200)}
grid6 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.05,
                                               n_estimators=70,
                                               max_depth=4, 
                                               min_child_weight=6, 
                                               gamma=0, 
                                               subsample=0.7, 
                                               colsample_bytree=0.6,
                                               objective= 'binary:logistic', 
                                               scale_pos_weight=0.9, 
                                               seed=14, 
                                               tree_method='gpu_hist'), 
                                               param_grid = test6, 
                                               scoring='roc_auc',
                                               n_jobs=-1, cv=5)
grid6.fit(X_train, y_train)
grid6.best_params_, grid6.best_score_

# %% colab_type="code" id="XxaKjAZeCPGh" colab={"base_uri": "https://localhost:8080/", "height": 136} executionInfo={"elapsed": 1509194, "status": "ok", "timestamp": 1600377472399, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="1d4dc87a-4d1d-4843-c114-c78bf8de9c0c"
params = {'max_depth': range(3,10,2),
         'min_child_weight': range(1,6,2),
         'gamma': [i/10.0 for i in range(0,5)],
         'subsample':[i/10.0 for i in range(6,10)],
         'colsample_bytree':[i/10.0 for i in range(6,10)],
         'scale_pos_weight': range(1,11)}
random = RandomizedSearchCV(estimator = XGBClassifier(learning_rate=0.01, 
                                                      n_estimators=1000,
                                                      objective='binary:logistic', 
                                                      seed=14, 
                                                      tree_method='gpu_hist'), 
                           param_distributions = params,
                           n_iter=100,
                           scoring='roc_auc',
                           n_jobs=-1, cv=5)
random.fit(X_train, y_train)
random.best_params_, random.best_score_

# %% colab_type="code" id="P7GhGUHMVSGd" colab={"base_uri": "https://localhost:8080/", "height": 170} executionInfo={"elapsed": 3355328, "status": "ok", "timestamp": 1600369018634, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="091d868e-1545-4c33-feed-70c60176dc69"
params = {'max_depth': range(3,10,2),
         'min_child_weight': range(1,6,2),
         'gamma': [i/10.0 for i in range(0,5)],
         'subsample':[i/10.0 for i in range(6,10)],
         'colsample_bytree':[i/10.0 for i in range(6,10)],
         'scale_pos_weight': [i/10 for i in range(1,11)],
         'learning_rate': [0.005, 0.01],
         'n_estimators': range(100,2001,200)}
random = RandomizedSearchCV(estimator = XGBClassifier(objective= 'binary:logistic', 
                                                     seed=14, tree_method='gpu_hist'), 
                           param_distributions = params,
                           n_iter=100,
                           scoring='roc_auc',
                           n_jobs=-1, cv=5)
random.fit(X_train, y_train)
random.best_params_, random.best_score_

# %% colab_type="code" id="tcN8UNJC8o3Y" colab={"base_uri": "https://localhost:8080/", "height": 673} executionInfo={"elapsed": 23164, "status": "ok", "timestamp": 1600377793212, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="b093e518-509b-41cd-dcbb-b82b3c588412"
model_eval(random.best_estimator_, X_train, y_train, X_test, y_test,
           model_name='XGBoost Classifier')

# %% colab_type="code" id="MX9FqcP8dbbV" colab={"base_uri": "https://localhost:8080/", "height": 673} executionInfo={"elapsed": 20880, "status": "ok", "timestamp": 1600369607495, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="1f4e254e-3883-4752-ee2e-ed17584e056c"
model_eval(random.best_estimator_, X_train, y_train, X_test, y_test,
           model_name='XGBoost Classifier')

# %% colab_type="code" id="W4IxrVV56Z6g" colab={"base_uri": "https://localhost:8080/", "height": 673} executionInfo={"elapsed": 38133, "status": "ok", "timestamp": 1600372088129, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="62203e3d-6320-42c2-ad0a-e5ac0af7ec99"
xgb_gpu = XGBClassifier(learning_rate=0.005,
                    n_estimators=1700,
                    max_depth=3,
                    min_child_weight=5,
                    gamma=0.1, 
                    subsample=0.6, 
                    colsample_bytree=0.7,
                    objective= 'binary:logistic',
                    scale_pos_weight=2.7663989290495317, 
                    seed=14, 
                    tree_method='gpu_hist')
model_eval(xgb_gpu, X_train, y_train, X_test, y_test,
           model_name='XGBoost Classifier')

# %% [markdown] colab_type="text" id="GmDteUcXz1rx"
# ### Model with Weighted Parameter

# %% [markdown] colab_type="text" id="nzmuYqNmzRFD"
# #### Logistic Regression

# %% colab_type="code" id="P5ML4J6vzWzm" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 24225, "status": "ok", "timestamp": 1600452251918, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="e85fe602-009c-4b2d-ba78-9da3bc98b83b"
lr_cw = LogisticRegression(max_iter=9999,
                           class_weight='balanced',
                           C=11.288378916846883,
                           penalty='l2')
model_eval(lr_cw, X_train_sc, y_train)

# %% colab_type="code" id="mywXBHdNzZ6Y" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 24001, "status": "ok", "timestamp": 1600452252555, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="2f083adf-a1a8-4be2-a621-82c8c1787b67"
test_eval(lr_cw, X_test_sc, y_test)

# %% [markdown] colab_type="text" id="peU9EsMF5Pdy"
# ##### Hyperparameter Tunning

# %% colab_type="code" id="AlUV9oUt4Sfw" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 7886, "status": "ok", "timestamp": 1600410205106, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="3b5ab12b-ee58-4b25-c32d-1ab0cf1c5af9"
params = {'penalty': ['l1', 'l2'],
          'C': np.logspace(-4,4,20)}

grid = GridSearchCV(estimator=LogisticRegression(max_iter=9999,
                                                 class_weight='balanced'), 
                     param_grid=params, 
                     scoring='roc_auc',
                     n_jobs=-1, cv=5)

grid.fit(X_train_sc, y_train)
grid.best_params_, grid.best_score_

# %% [markdown] colab_type="text" id="9Rkmop0IzQ0E"
# #### XGBoost Classifier

# %% colab_type="code" id="RsnS_czY6dqI" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 48245, "status": "ok", "timestamp": 1600452289579, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="31936554-9a56-4662-ac50-9aad3d407128"
ratio = float(np.sum(train['churn'] == 0)) / np.sum(train['churn'] == 1)

xgb_cw = XGBClassifier(learning_rate=0.005,
                       n_estimators=1700,
                       max_depth=3,
                       min_child_weight=5,
                       gamma=0.1, 
                       subsample=0.8, 
                       colsample_bytree=0.6,
                       objective='binary:logistic',
                       scale_pos_weight=ratio,
                       tree_method='gpu_hist',
                       seed=14)

model_eval(xgb_cw, X_train, y_train)

# %% colab_type="code" id="m0fZXDwlyyhK" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 48219, "status": "ok", "timestamp": 1600452290309, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="1b4eedc4-5581-4532-fb5e-4882b539d2bb"
test_eval(xgb_cw, X_test, y_test)

# %% [markdown] colab_type="text" id="dLmkhbhlxtFt"
# ##### Hyperparameter Tunning

# %% colab_type="code" id="fdw-8vKpFHWO" colab={}
estimator1 = XGBClassifier(learning_rate=0.1,
                           objective='binary:logistic',
                           scale_pos_weight=ratio,
                           tree_method='gpu_hist',
                           seed=14)

params1 = {'n_estimators': stats.randint(150, 1000)}

grid1 = GridSearchCV(estimator=estimator1, 
                     param_grid=params1, 
                     scoring='roc_auc',
                     n_jobs=-1, cv=5)

grid1.fit(X_train, y_train)
grid1.best_params_, grid1.best_score_)

# %% colab_type="code" id="Dkb8RNE3GgQd" colab={}
estimator2 = XGBClassifier(learning_rate=0.1,
                           n_estimators=1000,
                           objective='binary:logistic',
                           scale_pos_weight=ratio,
                           tree_method='gpu_hist',
                           seed=14)

params2 = {'max_depth': stats.randint(3,10),
           'min_child_weight': stats.randint(1,6),
           'gamma': [i/10.0 for i in range(0,5)],
           'subsample':[i/10.0 for i in range(6,10)],
           'colsample_bytree':[i/10.0 for i in range(6,10)]}


{'n_estimators': stats.randint(150, 1000),
              'learning_rate': stats.uniform(0.01, 0.6),
              'subsample': stats.uniform(0.3, 0.9),
              'max_depth': [3, 4, 5, 6, 7, 8, 9],
              'colsample_bytree': stats.uniform(0.5, 0.9),
              'min_child_weight': [1, 2, 3, 4]
             }
randomcv = RandomizedSearchCV(estimator=estimator2,
                              param_distributions=params2,
                              n_iter=50,
                              scoring='roc_auc',
                              n_jobs=-1, cv=5)

randomcv.fit(X_train, y_train)
randomcv.best_params_, randomcv.best_score_

# %% colab_type="code" id="HMrK2pz4-OAL" colab={"base_uri": "https://localhost:8080/", "height": 690} executionInfo={"elapsed": 198583, "status": "ok", "timestamp": 1600400233401, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="345a1d36-e2f7-4d14-d151-1898b01e8d6a"
estimator1 = XGBClassifier(learning_rate=0.01,
                       n_estimators=1000,
                       max_depth=3,
                       min_child_weight=5,
                       gamma=0.1, 
                       subsample=0.8, 
                       colsample_bytree=0.6,
                       objective='binary:logistic',
                       scale_pos_weight=ratio,
                       tree_method='gpu_hist',
                       seed=14)




model_eval(rs_cv.best_estimator_, X_train, y_train, X_test, y_test,
           model_name='XGBoost Classifier (Weighted)')

# %% colab_type="code" id="Q802TmLpTkp3" colab={}
ratio = float(np.sum(train['churn'] == 0)) / np.sum(train['churn'] == 1)

estimator = XGBClassifier(max_depth=3,
                       min_child_weight=5,
                       gamma=0.1, 
                       subsample=0.8, 
                       colsample_bytree=0.6,
                       objective='binary:logistic',
                       scale_pos_weight=ratio,
                       tree_method='gpu_hist',
                       seed=14)

params = {'learning_rate': [0.005, 0.01, 0.05],
          'n_estimators': range(100,2001,200)}

grid = GridSearchCV(estimator=estimator, 
                     param_grid=params, 
                     scoring='roc_auc',
                     n_jobs=-1, cv=5)

grid.fit(X_train, y_train)
print(grid.best_params_, grid.best_score_)

model_eval(grid.best_estimator_, X_train, y_train, X_test, y_test,
           model_name='XGBoost Classifier (Weighted)')

# %% colab_type="code" id="M4femqlEb0OT" colab={"base_uri": "https://localhost:8080/", "height": 690} executionInfo={"elapsed": 45514, "status": "ok", "timestamp": 1600402762027, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="c2756f35-1885-457a-d1dc-ee08c9d5883e"
print(grid.best_params_, grid.best_score_)

model_eval(grid.best_estimator_, X_train, y_train, X_test, y_test,
           model_name='XGBoost Classifier (Weighted)')

# %% [markdown] id="90PTmrQQqTUp" colab_type="text"
# **Summary:**
#
# By tuning the class weight parameter, we get a model that can give a higher recall but with a decrease in Accuracy.
# * The results of Logistic Regression evaluation on the test set obtained Recall 0.755 and AUC Score 0.847.
# * XGBoost was slightly higher with Recall 0.777 and AUC Score 0.854 on the test set.

# %% [markdown] colab_type="text" id="2imQAu646BR8"
# ### Model with Oversampling

# %% colab_type="code" id="ERqtap2X-ELM" colab={}
from imblearn.over_sampling import SMOTE

oversample = SMOTE()
X_over, y_over = oversample.fit_resample(X_train.values, y_train.values)

# %% colab_type="code" id="U4GnrZodz74u" colab={"base_uri": "https://localhost:8080/", "height": 342} executionInfo={"elapsed": 39863, "status": "ok", "timestamp": 1600452290312, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="dd788ff6-8e09-4b74-854c-34aaa3ed635a"
sns.countplot(x=y_over)

# %% [markdown] colab_type="text" id="uT1vLaGL0Y6J"
# #### Logistic Regression

# %% colab_type="code" id="AmU8acMO0LS8" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 39584, "status": "ok", "timestamp": 1600452291271, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="9867bdd8-7c8b-4328-e82e-fbc37cfb394d"
lr = LogisticRegression(max_iter=9999,
                        C=1.623776739188721,
                        penalty='l2')
model_eval(lr, X_over, y_over)

# %% colab_type="code" id="iBY_OJS70gaI" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 34402, "status": "ok", "timestamp": 1600452291945, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="a8032cab-6120-4feb-8089-f347a716f6a4"
test_eval(lr, X_test, y_test)

# %% [markdown] colab_type="text" id="KtjbGrbf5ZKm"
# ##### Hyperparameter Tunning

# %% colab_type="code" id="VFxS8S5q1WGm" colab={"base_uri": "https://localhost:8080/", "height": 34} executionInfo={"elapsed": 13954, "status": "ok", "timestamp": 1600410047151, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="d0f74e33-58c4-4061-9360-2ba634bd8177"
params = {'penalty': ['l1', 'l2'],
          'C': np.logspace(-4,4,20)}

grid = GridSearchCV(estimator=LogisticRegression(max_iter=9999), 
                     param_grid=params, 
                     scoring='roc_auc',
                     n_jobs=-1, cv=5)

grid.fit(X_train, y_train)
grid.best_params_, grid.best_score_

# %% [markdown] colab_type="text" id="kQZHotIf0boP"
# #### XGBoost Classifier

# %% colab_type="code" id="vXrOIK9I5sGl" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 43246, "status": "ok", "timestamp": 1600452557750, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="b2587d9d-0a14-4925-f8b9-488d7a2fd3a1"
from xgboost import XGBClassifier
xgb_os = XGBClassifier(learning_rate=0.005,
                       n_estimators=1700,
                       max_depth=3,
                       min_child_weight=4,
                       gamma=0.1, 
                       subsample=0.6, 
                       colsample_bytree=0.7,
                       objective= 'binary:logistic',
                       scale_pos_weight=1,
                       tree_method='gpu_hist', 
                       seed=14)
model_eval(xgb_os, X_over, y_over)

# %% colab_type="code" id="6ZoCq1k6ZW3t" colab={"base_uri": "https://localhost:8080/", "height": 622} executionInfo={"elapsed": 1485, "status": "ok", "timestamp": 1600452589385, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="2f896ef4-43e9-4472-c2e0-be829c93b948"
test_eval(xgb_os, X_test.values, y_test.values)

# %% colab_type="code" id="Nnb_hmKy5tuh" colab={"base_uri": "https://localhost:8080/", "height": 119} executionInfo={"elapsed": 102188, "status": "ok", "timestamp": 1600426288546, "user": {"displayName": "Abdillah Fikri", "photoUrl": "", "userId": "04470220666512949031"}, "user_tz": -420} outputId="a9d52926-6843-40d1-9fda-7834d5e19edb"
from sklearn.model_selection import RandomizedSearchCV

estimator = XGBClassifier(learning_rate=0.01,
                          n_estimators=700,
                          objective= 'binary:logistic',
                          scale_pos_weight=1,
                          tree_method='gpu_hist', 
                          seed=14)

params = {'max_depth': range(3,10,1),
          'min_child_weight': range(1,6,1),
          'gamma': [i/10.0 for i in range(0,5)],
          'subsample':[i/10.0 for i in range(6,10)],
          'colsample_bytree':[i/10.0 for i in range(6,10)]}

rs_cv = RandomizedSearchCV(estimator=estimator, 
                           param_distributions=params,
                           n_iter=100,
                           scoring='roc_auc',
                           n_jobs=-1, cv=5)

rs_cv.fit(X_over, y_over)
rs_cv.best_params_, rs_cv.best_score_

# %% [markdown] id="WUhHxUmdqjje" colab_type="text"
# **Summary:**
# * With the oversampling method, similar results are obtained for Logistic Regression compared to previous class weighted model.
# * However, the XGBoost results were too overfit for the training and cross validation sets. The metrics result is less than what we expected because Recall is only 0.59
