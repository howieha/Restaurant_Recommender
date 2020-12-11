# Restaurant_Recommender
Hybrid Recommender System for Restaurant Recommendation

## Data Loading
Run `envinit.py` to set up database envrionment. Then run `loadcsv.py` to load dataset. Loading all datasets may take some time.

## Data Structure
Data files are now under `\data` directory. Each database (e.g. prototype, training, testing) should take up its own sub-directory in `\data`.

## Collabrative Filtering
1. Run `text_score_calculation.py` to calculate text score of all reviews---> get dataset_review_emo_bayes.tsv file
2. Run `calculate_user_item_matrix.py` to calculate user-item matrix---> get user_item_matrix.tsv
   then run 
   then run `calculate_user_user_similarity.py` and `rebuild_user_user_similarity_matrix.py` one by one ---> get user_user_matrix_nof.tsv  
   file
3. `Run collabrative_filter.py` with user_item_matrix.tsv, user_user_matrix_nof.tsv, 
