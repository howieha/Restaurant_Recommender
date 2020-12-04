import numpy as np
import os
import pandas as pd
import pickle

def get_user_avg_ratings(user_item_mat):
    user_avg_ratings = dict()
    line_count = 0
    avg_list = []
    index_list = []
    for line in pd.read_csv(
            os.path.join(os.path.dirname(__file__), user_item_mat),
            sep='\t', na_values='None', index_col=0, chunksize=1):
        user_rating_sum = 0
        user_rating_count = 0
        user_id = line.index.item()
        for bus_id in line:
            if line[bus_id].item()!=0.0:
                user_rating_sum += line[bus_id].item()
                user_rating_count += 1
        user_avg_rating = user_rating_sum / user_rating_count
        print(line_count)
        line_count += 1
        avg_list.append(user_avg_rating)
        index_list.append(user_id)
    df = pd.DataFrame(data={"average":avg_list}, index = np.array(index_list))
    return df

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "distances_wid.p"), 'rb') as handle:
        relev_businesses = pickle.load(handle)
        
    user_avg_ratings = get_user_avg_ratings("user_user_similarity/user_item_matrix.tsv")
    user_avg_ratings.to_csv(os.path.join(os.path.dirname(__file__), "user_avg_ratings.tsv"), sep="\t")
                
"""
for line in pd.read_csv(
        os.path.join(os.path.dirname(__file__), "user_user_similarity/user_item_matrix.tsv"),
        sep='\t', na_values='None', index_col=0, chunksize=1):
    user_id = line.index
    recommendation = set()
    for bus_id in line:
        if line[bus_id].item()!=0.0:
            content_filtered_bus = relev_businesses[bus_id]
            sorted_relev_bus = sorted(content_filtered_bus, key=content_filtered_bus.get)
            if not filter_all:
                if include_been_to:
                    sorted_relev_bus = sorted_relev_bus[:top_k_bus]
                else:
                    sorted_relev_bus = sorted_relev_bus[1:top_k_bus+1]
            recommendation.update(sorted_relev_bus)
            content_recommendations[user_id.item()] = recommendation
    print(line_counter)
    line_counter += 1

with open(os.path.join(os.path.dirname(__file__), 'content_recommendation.pickle'), 'wb') as handle:
    pickle.dump(content_recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)
"""
