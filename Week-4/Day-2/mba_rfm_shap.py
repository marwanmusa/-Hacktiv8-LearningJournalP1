# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/ardhiraka/FSDS_Guidelines/blob/master/p1/w4/D2AM_new.ipynb

# More Algorithm

Have you ever wondered how often do you buy certain items together? Why do you buy some items together? How likely do you purchase an item along with another one? Why sugar placed near tea bags? Is there any relationship between these items? What is the main idea behind it?

## Market Basket Analysis

**What Actually is Market Basket Analysis?**

Market basket analysis is a data mining technique used by retailers to increase sales by better understanding customer purchasing patterns. It involves analyzing large data sets, such as purchase history, revealing product groupings, and products that are likely to be purchased together.

**How does it actually work in real life?**

Market Basket Analysis is one of the key techniques used by large retailers to uncover associations between items. It works by looking for combinations of items that occur together frequently in transactions. To put it another way, it allows retailers to identify relationships between the items that people buy.

To make it easier to understand, think of Market Basket Analysis in terms of shopping at a supermarket. Market Basket Analysis takes data at the transaction level, which lists all items bought by a customer in a single purchase. The technique determines relationships of what products were purchased with which other product(s).

![MBA](https://miro.medium.com/max/421/1*6uVTNwBuTTvpOpMhBPHghQ.jpeg)

It works on the logic of frequent itemset as described in the above image. So, it seems like the person who purchased milk also purchases bread.

**So how to find such Association Rules?**

Association Rules are widely used to analyze retail basket or transaction data and are intended to identify strong rules discovered in transaction data using measures of interestingness, based on the concept of strong rules.

- `Frequently Bought Together` → Association
- `Customers who bought this item also bought` → Recommendation

These relationships are then used to build profiles containing If-Then rules of the items purchased. for example:

`If {A} Then {B} : A => B`

**Itemset**

As everyone knows, an itemset is a set of items that consist of two or more items.

![MBA-Additionals](https://miro.medium.com/max/166/1*GXQQsO2FuJbk8-Z70MUIxA.png)

**Transactions**

Transactions are the main data source of Affinity Analysis. Stores or retailers gather tremendous transaction data by recording activities over time. Each transaction is associated with a unique transaction ID (TID), and it contains subsets of itemsets.

![MBA-Additionals](https://miro.medium.com/max/187/1*TSxr87-xhA6IHIKv5GXVzg.png)

**Support**

Support simply emphasizes how popular an itemset is. Support, despite being simple, is an important metric in the Affinity Analysis that used to determine the strength of association between items. Take 5 transactions, for instance. If you purchase bread in 3 transactions, you can tell the support of bread is equal to 3/5.

![MBA-Additionals](https://miro.medium.com/max/192/1*QAfEmwoWOVCjAkiOMqBjeg.png)

**Confidence**

While the support emphasizes how popular an itemset is, confidence denotes the likelihood of certain items are purchased together. For instance, how likely butter is purchased when item bread is purchased. Confidence is typically notated as Bread ⇒ Butter (Proportion of transactions containing Bread that also contain Butter.)

![MBA-Additionals](https://miro.medium.com/max/306/1*2TgF0JWLRWwtfefBt2Re0w.png)

Confidence, as you can see above, is a probability and so its range is [0,1]. If the confidence of Bread ⇒ Butter is equal to 1, we can say every time a customer purchases bread, also purchases butter.

**Lift**

Like confidence, the lift is notated as Bread ⇒ Butter. It says how likely Butter is purchased when Bread is purchased while controlling for how popular Butter is.

![MBA-Additionals](https://miro.medium.com/max/614/1*FRe0_HRlXqyg3rvs9Usb7Q.png)

Lift’s range is [0, +∞]. When lift equal to one, bread and butter are independent and, thus, no inferences can be made about butter when the bread is purchased. However, when the lift is greater than 1, it means that the butter is likely to be purchased together with bread.

**Conviction**

Wikipedia says "conviction can be interpreted as the ratio of the expected frequency that X occurs without Y (that is to say, the frequency that the rule makes an incorrect prediction) if X and Y were independent divided by the observed frequency of incorrect predictions." Conviction has the range [0,+∞] and the following form:

![MBA-Additionals](https://miro.medium.com/max/462/1*88PnWvjVMoptWSsFR23LsA.png)

Example of MBA:
"""

my_basket=[['bread','butter','wine','bananas','coffee','carrots'],
          ['tomatoes','onions','cheese','milk','potatoes'],
          ['beer','chips','asparagus','salsa','milk','apples'],
          ['olive oil','bread','butter','tomatoes','steak','carrots'],
          ['tomatoes','onions','chips','wine','ketchup','orange juice'],
          ['bread','butter','beer','chips','milk'],
          ['butter','tomatoes','carrots','coffee','sugar'],
          ['tomatoes','onions','cheese','milk','potatoes'],
          ['bread','butter','ketchup','coffee','chicken wings'],
          ['butter','beer','chips','asparagus','apples'],
          ['tomatoes','onion','beer','chips','milk','coffee']]

def frequency_items (x,y):
    fx_=sum([x in i for i in my_basket])
    fy_=sum([y in i for i in my_basket])
    
    fxy_=sum([all(z in i for z in [x,y]) for i in my_basket])
    
    support=fxy_/len(my_basket)

    confidence = support/(fx_/len(my_basket))

    lift =confidence /(fy_/len(my_basket))
    
    if confidence ==1:
        conviction = 0
    else:
        conviction=(1-(fy_/len(my_basket)))/(1-confidence)
    
    print("Support = {}".format(round(support,2)))
    print("Confidence = {}".format(round(confidence,2)))
    print("Lift= {}".format(round(lift,2)))
    print("Conviction={}".format(round(conviction,2)))

frequency_items('bread','butter')

"""36% of transactions contain both bread and butter. Butter appears every time in transactions that contain bread only. Confidence = 1 indicates that butter is always purchased whenever bread is purchased. Lastly, the value of lift is greater than 1 and it means it is more likely bread and butter will be bought together than each individually.

**Market Basket Analysis using the Apriori method**
"""

!pip install -q mlxtend

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

"""Dataset can be found [here](https://www.kaggle.com/irfanasrullah/groceries)."""

# Loading Data
import csv

with open('groceries.csv', newline='') as f:
    reader = csv.reader(f)
    data_csv = list(reader)

# Importing packages and data preprocessing
import mlxtend.frequent_patterns 
import mlxtend.preprocessing

encode_=mlxtend.preprocessing.TransactionEncoder()
encode_arr=encode_.fit_transform(data_csv)

print(encode_arr)

# Converting to dataframe
encode_df=pd.DataFrame(encode_arr, columns=encode_.columns_)
encode_df

# Calculating support

md=mlxtend.frequent_patterns.apriori(encode_df)
md_minsup=mlxtend.frequent_patterns.apriori(encode_df,
                                           min_support=0.01, 
                                            use_colnames=True)
md_minsup.head(20)

# Creating rules (Metric: Confidence) Antecedents ⇒ Consequents

rules=mlxtend.frequent_patterns.association_rules(
md_minsup, metric="confidence",min_threshold=0.06,support_only=False)

rules.head(20)

# Creating rules (Metric: Lift) Antecedents ⇒ Consequents

rules2=mlxtend.frequent_patterns.association_rules(
md_minsup, metric="lift",min_threshold=0.06,support_only=False)

rules2.head(20)

"""## RFM Analysis

RFM analysis is a basic customer segmentation algorithm. It stands for Recency, Frequency, and Monetary analysis.

RFM segmentation will make you able to understand your customer base better, and also serve as a good starting point for your data journey and more advanced customer models. You will be able to give more accurate answers to key questions for your business — for example:

- Who are your best customers?
- Which customers are at the verge of churning?
- Who has the potential to be converted in more profitable customers
- Which customer are lost/inactive?
- Which customers is critical to retain?
- Who are your loyal customers?
- Which group of customers is most likely to respond to your current campaign?

The behaviour is identified by using only three customer data points: the recency of purchase (R), the frequency of purchases (F) and the mean monetary value of each purchase (M). After some calculations on the RFM data we can create customer segments that are actionable and easy to understand — like the ones below:

- Champions: Bought recently, buy often and spend the most
- Loyal customers: Buy on a regular basis. Responsive to promotions.
- Potential loyalist: Recent customers with average frequency.
- Recent customers: Bought most recently, but not often.
- Promising: Recent shoppers, but haven’t spent much.
- Needs attention: Above average recency, frequency and monetary values. May not have bought very recently though.
- About to sleep: Below average recency and frequency. Will lose them if not reactivated.
- At risk: Some time since they’ve purchased. Need to bring them back!
- Can’t lose them: Used to purchase frequently but haven’t returned for a long time.
- Hibernating: Last purchase was long back and low number of orders. May be lost.

The above segments and labels are frequently used as a starting point but you can come up with your own segments and labels that is better fits for your customer base and business model.

For each of the segments, you could design appropriate actions, for example:

- Champions: Reward them. They can become evangelists and early adopters of new products.
- Loyal customers: Up-sell higher value products. Engage them. Ask for reviews.
- Potential loyalist: Recommend other products. Engage in loyalty programs.
- Recent/new customers: Provide a good onboarding process. Start building the relationship.
- Promising: Create more brand awareness. Provide free trials.
- Needs attention: Reactivate them. Provide limited time offers. Recommend new products based on purchase history.
- About to sleep: Reactivate them. Share valuable resources. Recommend popular products. Offer discounts.
- At risk: Send personalised email or other messages to reconnect. Provide good offers and share valuable resources.
- Can’t lose them: Win them back. Talk to them. Make them special offers. Make them feel valuable.
- Hibernating:Recreate brand value. Offer relevant products and good offers.

"""

!pip install -q lifetimes

# Read the data
df = pd.read_csv('https://github.com/ardhiraka/PFDS_sources/blob/master/OnlineRetail.csv.zip?raw=true', 
                 compression='zip', 
                 header=0, 
                 sep=',', 
                 encoding= 'unicode_escape')

df.head()

# Filter on Unite Kingdom to get a clean cohort
df = df[df['Country'] == 'United Kingdom']
df.head()

# Transform to proper datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df.head()

# Remove records with no CustomerID
df = df[~df['CustomerID'].isna()]
df.head()

# Remove negative/0 quantities and prices
df = df[df['Quantity']>0]
df = df[df['UnitPrice']>0]
df.head()

# Create new revenue columns
df['Revenue'] = df['Quantity'] * df['UnitPrice']
df.head()

# Create a new data frame grouped by InvoiceNo
orders = df.groupby(['InvoiceNo', 'InvoiceDate']).sum().reset_index()
orders.head()

# Create the rfm summary table from litetimes utility function
from lifetimes.utils import summary_data_from_transaction_data

rfm = summary_data_from_transaction_data(orders, 'CustomerID', 'InvoiceDate', monetary_value_col='Revenue').reset_index()
rfm

# Filter out non repeat customers
rfm = rfm[rfm['frequency']>0]
rfm.head()

# Filter out monetary outliers
rfm = rfm[rfm['monetary_value']<2000]
rfm.head()

"""Getting the individual RFM score can be done in several ways. You could use your own business expertise and heuristics to make rankings that suit your customer base. For this case, we are going to go the statistical route and rank our customer using quartiles.

The ranking of the individual RFM scores is done by dividing each of the RFM values into quartiles which creates four more or less equal buckets. We then rank each bucket from one to four; four being the best.

A recency(R) of 1, the lowest score, represents the customers that have been inactive for a while. A frequency of 4, the highest score, are your most frequent buyers, and so on.
"""

# Create the quartiles scores
quantiles = rfm.quantile(q=[0.25, 0.5, 0.75])
quantiles

quantiles = quantiles.to_dict()

def RFMScore(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4

rfm['R'] = rfm['recency'].apply(RFMScore, args=('recency', quantiles,))
rfm['F'] = rfm['frequency'].apply(RFMScore, args=('frequency', quantiles,))
rfm['M'] = rfm['monetary_value'].apply(RFMScore, args=('monetary_value', quantiles,))

rfm

"""Calculate the overall RFM score

This step can be done in two ways:

- Concatenation — creates segments\
Here we just concatenate (not add) the individual RFM score like strings and get labeled segments in return. Our best segment will be 444 and our worst will be 111 — signifying the lowest score on all three of the RFM categories.
- Addition — creates a score\
Here we add the individual RFM scores like numbers and get a number in return indicating the customer score. The score will range from 3 to 12 and we can use this to create more human friendly labelled categories.
"""

# Concat RFM quartile values to create RFM Segments
def join_rfm(x): return str(x['R']) + str(x['F']) + str(x['M'])
rfm['RFM_Segment'] = rfm.apply(join_rfm, axis=1)

# Calculate RFM_Score
rfm['RFM_Score'] = rfm[['R','F','M']].sum(axis=1)

rfm

"""Even though segments like 411 and 243 may be interpretable by a human, they are not the most human friendly labels. But as promised in the beginning of the post, it’s possible to create more usable labels both for the RFM segments and the RFM scores. For the RFM segment we are going to use the most common naming scheme, as outlined above."""

# Create human friendly RFM labels
segt_map = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][2-3]': 'At risk',
    r'[1-2]4': 'Can\'t loose them',
    r'2[1-2]': 'About to sleep',
    r'22': 'Need attention',
    r'[2-3][3-4]': 'Loyal customers',
    r'31': 'Promising',
    r'41': 'New customers',
    r'[3-4][1-2]': 'Potential loyalists',
    r'4[3-4]': 'Champions'
}

rfm['Segment'] = rfm['R'].map(str) + rfm['F'].map(str)
rfm['Segment'] = rfm['Segment'].replace(segt_map, regex=True)

"""As you see, we now have the champions and hibernators etc. in place.
If you like the addition scheme more, we could create customer labels such as: bronze, silver, gold and platinum.
"""

# Create some human friendly labels for the scores
rfm['Score'] = 'Green'
rfm.loc[rfm['RFM_Score']>5,'Score'] = 'Bronze' 
rfm.loc[rfm['RFM_Score']>7,'Score'] = 'Silver' 
rfm.loc[rfm['RFM_Score']>9,'Score'] = 'Gold' 
rfm.loc[rfm['RFM_Score']>10,'Score'] = 'Platinum'

rfm.head(5)

"""To get a birds eye view of your overall customer base, we can plot a simple bar chart showing how many customers reside in each category:"""

import matplotlib.pyplot as plt

barplot = dict(rfm['Segment'].value_counts())
bar_names = list(barplot.keys())
bar_values = list(barplot.values())
plt.barh(bar_names, bar_values)
print(pd.DataFrame(barplot, index=[' ']))

"""Unfortunately, it looks like most of our customers are hibernating, so we better get going. On the bright side: We have some champions, and also a few customers in the promising and new categories. We’d better take good care of them.
We can do the same plot for the RFM score and see how it compares.
"""

barplot = dict(rfm['Score'].value_counts())
bar_names = list(barplot.keys())
bar_values = list(barplot.values())
plt.bar(bar_names, bar_values)
print(pd.DataFrame(barplot, index=[' ']))

"""Naturally we see the same pattern: Few of the most valuable customers and a lot of customers who need attention and reactivation. Better get to work.

**What we have learned**

If the customers in the OnlineRetail dataset where ours, we could say that we have learned the following:

- Over 85% of our customers are non repeat customers — we need to make a plan on how to improve retention.
- Our data contains a lot of garbage that need to be cleaned — we need to look at how the data is generated and improve our data validation.
- Our data contain outliers and the outliers should be investigated and maybe labeled or removed.
- After cleaning the data our RFM model can be used for creating more precise action plans for each customer segments. This can have positive effects on marketing spend, conversion rates and customer retention.

## Explainable AI

Explainability has been for sure one of the hottest topics in the area of AI — as there is more and more investment in the area of AI and the solutions are becoming increasingly effective, some businesses have found that they are not able to leverage AI at all! And why? Simple, a lot of these models are considered to be "black boxes", which means that there is no way to explain the outcome of a certain algorithm, at least in terms that we are able to understand.

**AI Explainability frameworks**

This is a subject that has been explored by many authors — in 2016 in a seminar work by Marco Ribeiro, Sameer Singh, and Carlos Guestrin a novel solution for the interpretability of a black-box model was proposed. The proposed solution aimed at building two types of trust: trusting the prediction delivered by the model and trusting the model.

Since then many other frameworks and tools have been proposed to make AI explainability a reality across different data types and sectors.

### SHAP

In order to provide model transparency, the SHAP (SHapley Additive exPlanations) was invented by Lundberg and Lee (2016). The article “Explain Your Model with the SHAP Values” has the following analogy:

Is your highly-trained model easy to understand? If you ask me to swallow a black pill without telling me what’s in it, I certainly don’t want to swallow it. The interpretability of a model is like a label on a drug bottle. We need to make our effective pill transparent for easy adoption.

The SHAP provides three salient propositions:

- The first one is global interpretability — the collective SHAP values can show how much each predictor contributes, either positively or negatively, to the target variable. This is like the variable importance plot but it is able to show the positive or negative relationship for each variable with the target (see the SHAP value plot below).
- The second one is local interpretability — each observation gets its own set of SHAP values (see the individual SHAP value plot below). This greatly increases its transparency. We can explain why a case receives its prediction and the contributions of the predictors. Traditional variable importance algorithms only show the results across the entire population but not on each individual case. The local interpretability enables us to pinpoint and contrast the impacts of the factors.
- Third, the SHAP values can be calculated for any tree-based model, while other methods use linear regression or logistic regression models as the surrogate models.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
np.random.seed(1)

wine = datasets.load_wine()
wine_data = pd.DataFrame(data= np.c_[wine['data'], wine['target']],
                     columns= wine['feature_names'] + ['target'])

X = wine_data.drop('target', axis=1)
y = wine_data['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Build the model with the random forest regression algorithm:
model = RandomForestRegressor(max_depth=6, random_state=0, n_estimators=10)
model.fit(X_train, y_train)

!pip install -q shap

"""The shap.summary_plot function with plot_type="bar" let you produce the variable importance plot. A variable importance plot lists the most significant variables in descending order. The top variables contribute more to the model than the bottom ones and thus have high predictive power."""

import shap

shap_values = shap.TreeExplainer(model).shap_values(X_train)
shap.summary_plot(shap_values, X_train, plot_type="bar")

"""The SHAP value plot can further show the positive and negative relationships of the predictors with the target variable. The code shap.summary_plot(shap_values, X_train)produces the following plot:"""

import matplotlib.pyplot as plt
f = plt.figure()
shap.summary_plot(shap_values, X_train)

"""This plot is made of all the dots in the train data. It demonstrates the following information:

- Feature importance: Variables are ranked in descending order.
- Impact: The horizontal location shows whether the effect of that value is associated with a higher or lower prediction.
- Original value: Color shows whether that variable is high (in red) or low (in blue) for that observation.
- Correlation: A high level of the "flavanoids" content has a high and positive impact on the quality rating. The "high" comes from the red color, and the "positive" impact is shown on the X-axis. Similarly, we will say the "color_intensity" is negatively correlated with the target variable.

In order to show how the SHAP values can be done on individual cases, We will execute on several observations. We randomly chose a few observations in as shown in Table below:
"""

# Get the predictions and put them with the test data.
X_output = X_test.copy()
X_output.loc[:, 'predict'] = np.round(model.predict(X_output), 2)

# Randomly pick some observations
random_picks = np.arange(1, 50, 10) # Every 20 rows
S = X_output.iloc[random_picks]
S

# Write in a function
def shap_plot(j):
    explainerModel = shap.TreeExplainer(model)
    shap_values_Model = explainerModel.shap_values(S)
    p = shap.force_plot(explainerModel.expected_value, shap_values_Model[j], S.iloc[[j]])
    return(p)

"""Let me walk you through the above code step by step. The above `shap.force_plot()` takes three values: the base value (`explainerModel.expected_value[0]`), the SHAP values (`shap_values_Model[j][0]`) and the matrix of feature values (`S.iloc[[j]]`). The base value or the expected value is the average of the model output over the training data X_train. It is the base value used in the following plot.

When I execute shap_plot(0) I get the result for the first row of Table.
"""

# Initialize your Jupyter notebook with initjs(), otherwise you will get an error message.
shap.initjs()
shap_plot(0)

"""Let me describe this elegant plot in detail:

- The output value is the prediction for that observation (the prediction of the first row in Table is 1.90).
- The base value: The original paper explains that the base value E(y_hat) is "the value that would be predicted if we did not know any features for the current output." In other words, it is the mean prediction, or mean(yhat).
- Red/blue: Features that push the prediction higher (to the right) are shown in red, and those pushing the prediction lower are in blue.
- Proline: has a positive impact on the quality rating. The Proline content of this wine is 345 (as shown in the first row of Table) which is lower than the average value 724. So it pushes the prediction to the left.
- Alcohol: has a negative impact on the quality rating. A lower than the average Alcohol drives the prediction to the right.
- Flavanoids: is positively related to the quality rating. A higher than the average Flavanoids pushes the prediction to the left.
- You may wonder how we know the average values of the predictors. Remember the SHAP model is built on the training data set. The means of the variables are: X_train.mean()
"""

X_train.mean()

"""What is the result for the 2nd observation in Table B look like? Let’s doshap_plot(1):"""

shap.initjs()
shap_plot(1)

"""**LIME**

Lime, Local Interpretable Model-Agnostic, is a local model interpretation technique using Local surrogate models to approximate the predictions of the underlying black-box model.

Local surrogate models are interpretable models like Linear Regression or a Decision Trees that are used to explain individual predictions of a black-box model.

Lime trains a surrogate model by generating a new data-set out of the datapoint of interest. The way it generates the data-set varies dependent on the type of data. Currently Lime supports text, image and tabular data.

For text and image data LIME generates the data-set by randomly turning single words or pixels on or off. In the case of  tabular data, LIME creates new samples by permuting each feature individually.

The model learned by LIME should be a good local approximation of the black box model but that doesn’t mean that it’s a good global approximation.

People may say that a linear model is easier than a complicated machine learning model. Is it true? The authors of LIME have two criteria:

- Easy to interpret: A linear model can have hundreds or thousands of variables. Is it more interpretable than a complex gradient boosting or deep learning model?
- Local fidelity: the explanation for individual predictions should at least be locally faithful, i.e. it must correspond to how the model behaves in the vicinity of the individual observation being predicted. The authors address that local fidelity does not imply global fidelity: features that are globally important may not be important in the local context, and vice versa. Because of this, it could be the case that only a handful of variables directly relate to a local (individual) prediction, even if a model has hundreds of variables globally.
"""

!pip install -q lime

X_featurenames = X.columns

"""To analyze the predictions of a tabular data-set like the Wine data-set we need to create a LimeTabularExplainer."""

import lime
import lime.lime_tabular

explainer = lime.lime_tabular.LimeTabularExplainer(np.array(X_train),
                    feature_names=X_featurenames, 
                    class_names=['target'], 
                    # categorical_features=, 
                    # There is no categorical features in this example, otherwise specify them.                               
                    verbose=True, mode='regression')

"""Why is it named `lime_tabular`? LIME names it for tabular (matrix) data, in contrast to `lime_text` for text data and `lime_image` for image data. In our example all predictors are numeric. LIME perturbs the data by sampling from a Normal(0,1) and doing the inverse operation of mean-centering and scaling, according to the means and standard deviations in the training data. If you have categorical variables, LIME perturbs the data by sampling according to the training distribution, and creates a binary feature of 1 if the value is the same as the instance being explained.

You can create a plot for each individual. Use num_features to specify the number of features displayed.
"""

exp = explainer.explain_instance(X_test.iloc[0], 
     model.predict, num_features=10)
exp.as_pyplot_figure()

"""- Green/Red color: features that have positive correlations with the target are shown in green, otherwise red.
- Flavanoids <=1.01: high Flavanoids values positively correlate with high wine targets.
- Alcohol > 13.51: high Alcohol values negatively correlate with high wine targets.
- Use the same logic to understand the rest features.

You can obtain the coefficients of the LIME model by as_list():
"""

pd.DataFrame(exp.as_list())

"""And you can show all the results in a notebook-like format:"""

exp.show_in_notebook(show_table=True, show_all=False)