import numpy as np
import os
import pandas as pd
import pickle

def run_x(index_name):

	content_recommendations = dict()
	filtered_recommendations = dict()
	with open(os.path.join(os.path.dirname(__file__), "collaborative_filtering_preprocessing\content_recommendation_"+index_name+".pickle"), 'rb') as content_handle:
		content_recommendations = pickle.load(content_handle)


	"""
		the average rating based on 411 items of user i
	"""
	user_avg_rating = pd.read_csv(
		os.path.join(os.path.dirname(__file__), "user_avg_ratings_only_star.tsv"),
		sep='\t', na_values='None', index_col=0)


	"""
		TODO: Set businesses not visited to nan in the original dataset.
	"""
	user_bus = pd.read_csv(
			os.path.join(os.path.dirname(__file__), "user_item_matrix_only_star.tsv"),
			sep='\t', na_values=0, index_col=0)
	users = user_bus.index
	user_bus_centered = user_bus.subtract(user_avg_rating.values)
	print('Data Load is Done...')
	line_count=0
	ite=0
	filename = "user_user_matrix_nof.tsv"

	"""
		main code to run filtering
	"""

	with open(filename, 'r') as fp1:
		for line in fp1:
			print(ite)
			if ite>0:
				lined=line.split(',')
				line_f=lined[-1]
				line=[]
				[line.append(float(i[2:-1])) for i in lined[1:-1]]
				line.append((float(line_f[2:-4])))
				user = users[line_count]
				content_filtered_bus = content_recommendations[user]
				user_dict = dict()
				for bus in content_filtered_bus:
					bus_ratings = user_bus_centered[bus]
					weighted_ratings = bus_ratings.values * line
					#print(len(weighted_ratings))
					weighted_rating_sum = np.nansum(weighted_ratings)
					weight_sum = np.nansum(line)
					weighted_score = user_avg_rating.loc[user].item() + weighted_rating_sum / weight_sum
					if weighted_score == weighted_score:
						user_dict[bus] = weighted_score
				filtered_recommendations[user] = user_dict
				line_count += 1
				
				#stopTime = time.time()
				#sumTime = stopTime - startTime

				#print('The total time is: ', sumTime)
			
			ite=ite+1

	with open(os.path.join(os.path.dirname(__file__), 'collaborative_filtered_recommendation_'+index_name+'.pickle'), 'wb') as handle:
		pickle.dump(filtered_recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
"""
	file name 
"""
run_x('0.1')
