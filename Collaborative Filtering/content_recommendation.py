import numpy as np
import os
import pandas as pd
import pickle
import random


def get_content_recommendations(relev_businesses, top_perc, mask_perc = 1.0, filter_all=False, include_been_to=False):
    """
    Given a dictionary of relevant businesses and a user_item_matrix, for
    each user find the businesses that have distances to the user's visited 
    restaurants lower than top_perc percentage of all distances and collate 
    them into a new dictionary (keys: businesses, values: distancees) for 
    this user. 

    Input:
    - relev_businesses: dictionary (keys:business_a, values:{keys:business_b,
     values: distances between business_a and business_b})
    - top_perc: the percentage threshold, collate only businesses that have distances
     lower than this percentage threshold
    - mask_perc: only use mask_perc of user's visited restaurants (for experimenting)
    - filter_all: retain all businesses
    - include_been_to: include restaurants users have been to in the output dictionary.

    Output:
    - content_recommendation: dictionary(keys: user, values:{keys: business, 
     values:distance})
    """

    # Initialize dictionary.
    content_recommendations = dict()
    # Keep progress when running the program.
    line_count = 0
    # Read user_item_matrix.
    for line in pd.read_csv(
            os.path.join(os.path.dirname(__file__), "user_user_similarity/user_item_matrix.tsv"),
            sep='\t', na_values='None', index_col=0, chunksize=1):
        # Get user_id from user_item_matrix.
        user_id = line.index
        recommendation = dict()
        bus_ids = []
        # Add business this user has been to to a list.
        for bus_id in line:
            if line[bus_id].item()!=0.0:
                bus_ids.append(bus_id)
        # Retain only some of the visited restaurants if necessary
        mask_length = int(len(bus_ids) * mask_perc)
        random.shuffle(bus_ids)
        bus_ids = bus_ids[:mask_length]
        # Loop through visited restaurants.
        for bus_id in bus_ids:
            # Find all restaurants output by the content recommendations.
            content_filtered_bus = relev_businesses[bus_id]
            sorted_relev_bus = sorted(content_filtered_bus, key=content_filtered_bus.get)
            # Retain only businesses that have distances lower than top_perc of all distances.
            top_k_bus = int(len(sorted_relev_bus) * top_perc)
            if not filter_all:
                if include_been_to:
                    sorted_relev_bus = sorted_relev_bus[:top_k_bus]
                else:
                    top_k_bus = min(top_k_bus, len(len(sorted_relev_bus))-1)
                    sorted_relev_bus = sorted_relev_bus[1:top_k_bus+1]
            for bus in sorted_relev_bus:
                # Update dictionary with distance.
                if (bus in recommendation and recommendation[bus] >= content_filtered_bus[bus]) or bus not in recommendation:
                    recommendation[bus] = content_filtered_bus[bus]
        content_recommendations[user_id.item()] = recommendation
        line_count += 1
        print(line_count)
    return content_recommendations

if __name__ == "__main__":
    relev_businesses = dict()
    with open(os.path.join(os.path.dirname(__file__), "distances_wid.p"), 'rb') as handle:
        relev_businesses = pickle.load(handle)
    # experimenting with mask_percs.
    mask_percs = [0.3, 0.5, 0.7]
    for mask_perc in mask_percs:
        # pervious tuning determined 0.2 to be the best top_perc.
        content_recommendations = get_content_recommendations(relev_businesses, 0.2, mask_perc)
        with open(os.path.join(os.path.dirname(__file__), "masked_content_recommendation_"+str(mask_perc)+".pickle"), 'wb') as handle:
            pickle.dump(content_recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)