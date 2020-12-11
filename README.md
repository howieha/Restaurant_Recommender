# Restaurant_Recommender
Hybrid Recommender System for Restaurant Recommendation

# Prerequisite for Python Library
SEE `prerequisite` FILE.

## Data Loading
1. Run `envinit.py` to set up database envrionment; notice that it will provide with a dataset name (e.g. `training`, `test`). Please check your current dataset and make sure that it is the latest version. `envinit.py` will also generate a copy of database environment as `db.p`, to support instant load of evnironment by importing this pickle file.
2. Then run `loadcsv.py` to load all datasets. Loading all datasets may take some time, until `LOAD FINISHED.` shows up.

## Data Structure
Data files are under `\data` directory. Each database (e.g. prototype, training, testing) should take up its own sub-directory in `\data`.

## Content-Based Filtering
1. Run `ccbusiness.py` to calculate the correlation coefficient matrix. This would output two pickle files, one for the C matrix without filtering as `pctot_raw.p`, and another one with filtering as `pctot.p`. Plotting of heatmap is also available.
2. Run `pagerank.py`; this requires functions in `louvain.py`. ---> Output: recommended restaurant for each user.

## Collabrative Filtering
1. Run `text_score_calculation.py` to calculate text score of all reviews---> get dataset_review_emo_bayes.tsv file
2. Run `calculate_user_item_matrix.py` to calculate user-item matrix---> get user_item_matrix.tsv
   then run `user_avg_ratings.py` to calculate average ratings of each user ---> get user_avg_ratings.tsv file
   then run `calculate_user_user_similarity.py` and `rebuild_user_user_similarity_matrix.py` one by one to get final user-to-user similarity    matrix ---> get user_user_matrix_nof.tsv file
3. Run `collabrative_filter.py` with user_item_matrix.tsv, user_user_matrix_nof.tsv, user_avg_ratings.tsv, content_recommendation.pickle to    get the final recommendation.
