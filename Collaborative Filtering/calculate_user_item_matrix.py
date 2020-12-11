import json
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import os
import collections
import nltk.classify
import nltk.metrics
import numpy as np


"""
	read all business id
"""
business=[]
users=[]
scores=[]
rates=[]
t=0
review=pd.read_csv('dataset_review_emo_bayes.tsv', sep="\t") 

"""
	get all business and user id
"""

for line in review.itertuples():
	
	#print(t)
	t+=1
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

#to save files
#output_path = os.path.join(os.path.dirname(__file__), "business.tsv")
#businessd =  DataFrame (business)
#businessd.to_csv(output_path, index=False, sep="\t")
#output_path = os.path.join(os.path.dirname(__file__), "users.tsv")
#usersd= DataFrame(users)
#usersd.to_csv(output_path, index=False, sep="\t")
#output_path = os.path.join(os.path.dirname(__file__), "stars.tsv")
#starsd= DataFrame(stars)
#starsd.to_csv(output_path, index=False, sep="\t")
	
"""
	build user-item matrix based on rate, matrix includes index and coloums shown the business and user id
"""
n_items=len(business)
n_users=len(users)

# reset n_user and n_item
user_item_matrix = np.zeros((n_users, n_items))
print(np.shape(user_item_matrix))
for line in review.itertuples():
	#print(line)
	# in review: it is User id , business id, stars, text_based score, 
    #print(line)
    # print("line={}\nlen(line)={}\n,line[1]={}\n,line[1]-1={}\n,line[2]={}\n,line[2]-1={}\n".format(line,len(line),line[1],line[1]-1,line[2],line[2]-1))
	pos_user=users.index(line[2])
	pos_business=business.index(line[3])
	user_item_matrix[pos_user, pos_business] = (line[4]-minrates)*100.0/(maxrates-minrates)#+ (line[10]-minscores)*100.0/(maxscores-minscores)   

output_path = os.path.join(os.path.dirname(__file__), "user_item_matrix_only_star.tsv")
df = DataFrame(user_item_matrix,index=users,columns=business)
df.to_csv(output_path, index=True, sep="\t")




