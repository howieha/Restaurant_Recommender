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