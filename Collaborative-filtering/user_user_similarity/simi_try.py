import json
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import os
import collections
import nltk.classify
import nltk.metrics
import numpy as np
import csv

"""
	read all business id
"""
business=[]
users=[]
scores=[]
rates=[]
t=0
review=pd.read_csv('dataset_review_emo_bayes.tsv', sep="\t") 

#print(len(review_data))

for line in review.itertuples():
	
	#print(t)
	t+=1
    # 将josn字符串转化为dict字典
	#print(json.loads(jsonstr).get('business_id'))
	business_name=line[3]
	user_name=line[2]
	scores.append(line[10])
	rates.append(line[4])
	if business_name not in business:
		business.append(business_name)
	if user_name not in users:
		users.append(user_name)

print('******* Business & user search finished*********')		
print('Total user number: ', len(users))
print('Total business number: ', len(business))
maxrates=max(rates)
minrates=min(rates)
maxscores=max(scores)
minscores=min(scores)

dataset_user=pd.read_csv('dataset_user.tsv', sep="\t") 
f=open('friendship_matrix.csv', 'w', encoding='utf-8', newline='') 
writer = csv.writer(f, dialect='excel')
t=0;
for i in range(len(users)):
	print(t)
	t=t+1
	pos=user[(dataset_user.user_id==users[i])].index.tolist()
	posf=users.index(user.iloc[pos_d1,:].friends)
	user_user_matrix = np.zeros((1, n_users))
	user_user_matrix[posf]=1.0
	df = DataFrame(user_user_matrix,columns=users)
	writer.writerow(df)

