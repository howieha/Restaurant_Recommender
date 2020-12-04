import numpy as np
import os
import pandas as pd
import pickle

content_recommendations = dict()
filtered_recommendations = dict()
with open(os.path.join(os.path.dirname(__file__), "content_recommendation.pickle"), 'rb') as content_handle:
    content_recommendations = pickle.load(content_handle)
user_avg_rating = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "user_avg_ratings.tsv"),
    sep='\t', na_values='None', index_col=0)

# TODO: Set businesses not visited to nan in the original dataset.
user_bus = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "user_user_similarity/user_item_matrix.tsv"),
        sep='\t', na_values=0, index_col=0)
users = user_bus.index
user_bus_centered = user_bus.subtract(user_avg_rating.values)
print("done pre-loading")

line_count = 0
index_list = ["1_10000", "10001_20000", "20001_30000", "30001_40000", "40001_50000", "50001_60000", "60001_67715"]
for index in index_list:
    filename = "user_user_matrix_" + index + ".tsv"
    for line in pd.read_csv(
        os.path.join(os.path.dirname(__file__), "user_user_matrix_without_friendship", filename),
        sep=',', na_values='None',chunksize=1, index_col=0):
        user = users[line_count]
        content_filtered_bus = content_recommendations[user]
        user_dict = dict()
        for bus in content_filtered_bus:
            bus_ratings = user_bus_centered[bus]
            weighted_ratings = bus_ratings.values * line.values[0]
            weighted_rating_sum = np.nansum(weighted_ratings)
            weight_sum = np.nansum(line.values[0][weighted_ratings==weighted_ratings])
            weighted_score = user_avg_rating.loc[user].item() + weighted_rating_sum / weight_sum
            if weighted_score == weighted_score:
                user_dict[bus] = weighted_score
        filtered_recommendations[user] = user_dict
        print(line_count)
        line_count += 1

with open(os.path.join(os.path.dirname(__file__), 'collaborative_filtered_recommendation.pickle'), 'wb') as handle:
    pickle.dump(filtered_recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)
