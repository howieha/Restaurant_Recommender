import numpy as np

user_similarity_mat = np.array()
user_business_mat = np.array()
user_avg = np.array()

n_users = user_similarity_mat.shape[0]
n_businesses = user_business_mat.shape[1]

pred = np.zeros((n_users, n_businesses))

# r_{u,i}-avg(r_u)
#TODO: use_business_mat might contain invalid entries or entries we are not 
# interested in (requires extra processing with nan values) 
# (Question: would computations with nan vlaues yield nan values, in which case we 
# can proceed as is?)
user_business_mat -= np.transpose(use_avg)
for u in n_users:
    for b in n_businesses:
        user_ratings = user_business_mat[:, b]
        user_weights = user_similarity_mat[u, :]
        weighted_rating = sum(user_ratings*user_weights) / sum(user_weights)
        pred[u, b] = user_avg[u] + weighted_rating
