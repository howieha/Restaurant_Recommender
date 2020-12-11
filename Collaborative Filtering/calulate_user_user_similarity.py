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
userdd=pd.read_csv('users.tsv', sep="\t") 
users=userdd.to_numpy()



"""define function for similarity calculation
"""
from sklearn.metrics.pairwise import pairwise_distances
def similarity_calculation(user1,user2): # user1=user_item_matrix.iloc[i,:], user=pd.read_csv('dataset_user.tsv', sep="\t") 	
	d1=user1.iloc[0:].to_numpy().reshape(1,-1)
	d2=user2.iloc[:,0:].to_numpy()

	#pos_d1=user[(user.user_id==user1[0])].index.tolist()
	#pos_d2=user[(user.user_id==user2[0])].index.tolist()
	#x=int((user2[0] in user.iloc[pos_d1,:].friends )| (user1[0] in user.iloc[pos_d2,:].friends))
	user_similarity = 1.0-pairwise_distances(d1,d2, metric='cosine')
	#print(np.shape(user_similarity))
	return user_similarity




import csv
"""
	calculate similarities in bunch
"""


user=pd.read_csv('user_item_matrix_only_star.tsv', sep="\t") 
dataset_user=pd.read_csv('dataset_user.tsv', sep="\t") 

with open("test4.tsv","w",newline='') as csvfile: 
	writer = csv.writer(csvfile)
	writer.writerow(np.hstack(("index", users.reshape(1,-1)[0,:])))
	x=[]
	y=[]
	t=0
	import time
	import datetime
	startTime = time.time()
	#user_user_matrix=np.zeros((67715,300))
	for i in range(67715):
		print(t)
		t=t+1;
		a=similarity_calculation(user.iloc[i,1:],user.iloc[30000:40000,1:])
		#print(DataFrame(a))
		a=np.hstack((i,a[0,:]))		
		a=DataFrame(a)
		writer.writerow(a.T.iloc[0,:])


with open("test5.tsv","w",newline='') as csvfile: 
	writer = csv.writer(csvfile)
	writer.writerow(np.hstack(("index", users.reshape(1,-1)[0,:])))
	x=[]
	y=[]
	t=0
	#user_user_matrix=np.zeros((67715,300))
	for i in range(67715):
		print(t)
		t=t+1;
		a=similarity_calculation(user.iloc[i,1:],user.iloc[40000:50000,1:])
		#print(DataFrame(a))
		a=np.hstack((i,a[0,:]))		
		a=DataFrame(a)
		writer.writerow(a.T.iloc[0,:])
		
with open("test6.tsv","w",newline='') as csvfile: 
	writer = csv.writer(csvfile)
	writer.writerow(np.hstack(("index", users.reshape(1,-1)[0,:])))
	x=[]
	y=[]
	t=0
	#user_user_matrix=np.zeros((67715,300))
	for i in range(67715):
		print(t)
		t=t+1;
		a=similarity_calculation(user.iloc[i,1:],user.iloc[50000:60000,1:])
		#print(DataFrame(a))
		a=np.hstack((i,a[0,:]))		
		a=DataFrame(a)
		writer.writerow(a.T.iloc[0,:])

with open("test7.tsv","w",newline='') as csvfile: 
	writer = csv.writer(csvfile)
	writer.writerow(np.hstack(("index", users.reshape(1,-1)[0,:])))
	x=[]
	y=[]
	t=0
	#user_user_matrix=np.zeros((67715,300))
	for i in range(67715):
		print(t)
		t=t+1;
		a=similarity_calculation(user.iloc[i,1:],user.iloc[60000:67716,1:])
		#print(DataFrame(a))
		a=np.hstack((i,a[0,:]))		
		a=DataFrame(a)
		writer.writerow(a.T.iloc[0,:])
