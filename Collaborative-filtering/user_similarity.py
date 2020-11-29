import json
import pandas as pd
import pandas as pd

"""
	read all business id
"""
business=[]
users=[]
t=0
with open('yelp_academic_dataset_review.json', 'r', encoding="utf-8") as f:
    # 读取所有行 每行会是一个字符串
	for jsonstr in f:
		t=t+1;
        # 将josn字符串转化为dict字典
		print(json.loads(jsonstr).get('business_id'))
		business_name=json.loads(jsonstr).get('business_id')
		user_name=json.loads(jsonstr).get('user_id')
		if business_name not in business:
			business.append(business_name)
		if user_name not in users:
			users.append(user_name)

"""
	build user-item matrix based on rate
"""
n_items=len(business)
n_users=len(users)
# reset n_user and n_item
user_item_matrix = np.zeros((n_users, n_items))
print(train_data_matrix.shape)
for line in review.itertuples():
	# in review: it is User id , business id, stars, text_based score, 
    #print(line)
    # print("line={}\nlen(line)={}\n,line[1]={}\n,line[1]-1={}\n,line[2]={}\n,line[2]-1={}\n".format(line,len(line),line[1],line[1]-1,line[2],line[2]-1))
    pos_user=users.index(line[0])
    pos_business=business.index(line[1])
    user_item_matrix[pos_user, pos_business] = line[2] #+line[3]*weight
    
user_user_matrix = np.zeros((n_users, n_users))
for line in user.itertuples():
	#to get friends list : user id, friends list
	pos_user=users.index(line[0])
	pos_usercol=users.index(line[1])
    test_data_matrix[pos_user,pos_usercol] = 1
    
 # 使用 sklearn 的pairwise_distances函数来计算余弦相似性
from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(user_item_matrix, metric='cosine')
#矩阵的转置实现主题的相似度
#item_similarity = pairwise_distances(user_item_matrix.T, metric='cosine')

#combine user_similarity and user_user_matrix
user_similarity=user_similarity+user_user_matrix
