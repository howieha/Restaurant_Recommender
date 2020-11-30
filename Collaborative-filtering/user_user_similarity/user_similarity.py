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

	# in review: it is User id , business id, stars, text_based score, 
    #print(line)
    # print("line={}\nlen(line)={}\n,line[1]={}\n,line[1]-1={}\n,line[2]={}\n,line[2]-1={}\n".format(line,len(line),line[1],line[1]-1,line[2],line[2]-1))
    pos_user=users.index(line[2])
    pos_business=business.index(line[3])
    user_item_matrix[pos_user, pos_business] = (line[4]-minrates)*100.0/(maxrates-minrates)+ (line[10]-minscores)*100.0/(maxscores-minscores)   

output_path = os.path.join(os.path.dirname(__file__), "user_item_matrix.tsv")
df = DataFrame(user_item_matrix,_stat_axis=users,columns=business)
df.to_csv(output_path, index=True, sep="\t")
from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(user_item_matrix, metric='cosine')

"""matrix based on friendship 
"""
f=open('friendship_matrix.csv', 'w', encoding='utf-8', newline='') 
writer = csv.writer(f, dialect='excel')
user=pd.read_csv('dataset_user.tsv', sep="\t") 
#user_user_matrix = int(np.zeros((n_users, n_users)))
for i in range(n_users):
	user_user_matrix = np.zeros((1, n_users))
	df = DataFrame(user_user_matrix,index=user[i],columns=users)
	writer.writerow(df)
	
for line in user.itertuples():
	#to get friends list : user id, friends list
	user_user_matrix = np.zeros((1, n_users))
	pos_usercol=users.index(line[1])
	user_user_matrix[pos_usercol] = '1.0'
	df = DataFrame(user_user_matrix,index=line[1],columns=users)
	writer.writerow(df)
output_path = os.path.join(os.path.dirname(__file__), "user_user_matrix.tsv")
df = DataFrame(user_user_matrix,index=users,columns=user)
df.to_csv(output_path, index=True, sep="\t")    

"""dfunction for similarity calculation
"""
from sklearn.metrics.pairwise import pairwise_distances
def similarity_calculation(user1, user2,user): # user1=user_item_matrix.iloc[i,:], user=pd.read_csv('dataset_user.tsv', sep="\t") 
	d1=user1[1:].to_numpy().reshape(1, -1) 
	d2=user2[1:].to_numpy().reshape(1, -1) 
	#pos_d1=user[(user.user_id==user1[0])].index.tolist()
	#pos_d2=user[(user.user_id==user2[0])].index.tolist()
	#x=int((user2[0] in user[pos_d1,:].friends )| (user1[0] in user[pos_d2,:].friends))
	user_similarity = 1.0-pairwise_distances(np.concatenate((d1, d2)), metric='cosine')
	return user_similarity,x

user=pd.read_csv('user_item_matrix.tsv', sep="\t") 
x=[]
for i in range(1,30000):
	x.append(similarity_calculation(user.iloc[2,:], user.iloc[i+1,:]))
plt.plot(x)
plt.show()

