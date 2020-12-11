import numpy as np
import os
import pandas as pd
import pickle

def get_user_avg_ratings(user_item_mat):
    """
    Given one user-item matrix, calculate the average rating a user has given.
    Input:
    - user_item_mat: file containing a dataframe, with rows indicating users
     columns indicating items, each value is user's rating for that restaurant
     or 0 if the user has not visited that restaurant.
    Output:
    - df: datafram with two columns, the first one containing user ids, and the 
     second one containing the average ratings a user has ever given.
    """
    # Keep line count to suggest progress when running the dataset.
    line_count = 0
    # Perpare two lists, each one would be a column in the final dataframe.
    avg_list = []
    index_list = []
    # Read the tsv file line by line.
    for line in pd.read_csv(
            os.path.join(os.path.dirname(__file__), user_item_mat),
            sep='\t', na_values='None', index_col=0, chunksize=1):
        # Initialize sum.
        user_rating_sum = 0
        # Count only the number of restaurants the user has visited.
        user_rating_count = 0
        user_id = line.index.item()
        for bus_id in line:
            # If the user has visited the restaurant by bus_id, add the rating
            # to the sum and update review count.
            if line[bus_id].item()!=0.0:
                user_rating_sum += line[bus_id].item()
                user_rating_count += 1
        # Calculate average rating given by the user.
        user_avg_rating = user_rating_sum / user_rating_count
        print(line_count)
        line_count += 1
        avg_list.append(user_avg_rating)
        index_list.append(user_id)
    # Write the two lists into dataframe.
    df = pd.DataFrame(data={"average":avg_list}, index = np.array(index_list))
    return df

if __name__ == "__main__":
    # Read user_item_matrix.tsv.
    user_avg_ratings = get_user_avg_ratings("user_user_similarity/user_item_matrix.tsv")
    # Produce user average rating dataframe.
    user_avg_ratings.to_csv(os.path.join(os.path.dirname(__file__), "user_avg_ratings.tsv"), sep="\t")