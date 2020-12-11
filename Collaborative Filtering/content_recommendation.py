import numpy as np
import os
import pandas as pd
import pickle
import random


def get_content_recommendations(relev_businesses, top_perc, mask_perc, filter_all=False, include_been_to=False):
    content_recommendations = dict()
    line_count = 0
    for line in pd.read_csv(
            os.path.join(os.path.dirname(__file__), "user_user_similarity/user_item_matrix.tsv"),
            sep='\t', na_values='None', index_col=0, chunksize=1):
        user_id = line.index
        recommendation = dict()
        bus_ids = []
        for bus_id in line:
            if line[bus_id].item()!=0.0:
                bus_ids.append(bus_id)
        mask_length = int(len(bus_ids) * mask_perc)
        random.shuffle(bus_ids)
        bus_ids = bus_ids[:mask_length]
        for bus_id in bus_ids:
            content_filtered_bus = relev_businesses[bus_id]
            sorted_relev_bus = sorted(content_filtered_bus, key=content_filtered_bus.get)
            top_k_bus = int(len(sorted_relev_bus) * top_perc)
            if not filter_all:
                if include_been_to:
                    sorted_relev_bus = sorted_relev_bus[:top_k_bus]
                else:
                    top_k_bus = min(top_k_bus, len(len(sorted_relev_bus))-1)
                    sorted_relev_bus = sorted_relev_bus[1:top_k_bus+1]
            for bus in sorted_relev_bus:
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
    mask_percs = [0.3, 0.5, 0.7]
    for mask_perc in mask_percs:
        content_recommendations = get_content_recommendations(relev_businesses, 0.2, mask_perc, include_been_to=True)
        with open(os.path.join(os.path.dirname(__file__), "masked_content_recommendation_"+str(mask_perc)+".pickle"), 'wb') as handle:
            pickle.dump(content_recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)