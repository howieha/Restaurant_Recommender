# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:17:32 2020

@author: huang
"""

import pandas as pd
from datetime import datetime
from ast import literal_eval

# READ BUSINESS DATABASE
bud_type = {'review_count': 'int64',
            'Access.dogs': 'boolean', 'Access.wheelchair': 'boolean',
            'Ambience.casual': 'boolean', 'Ambience.classy': 'boolean',
            'Ambience.divey': 'boolean', 'Ambience.hipster': 'boolean',
            'Ambience.intimate': 'boolean', 'Ambience.romantic': 'boolean',
            'Ambience.touristy': 'boolean', 'Ambience.trendy': 'boolean', 'Ambience.upscale': 'boolean',
            'Equip.OutdoorSeating': 'boolean', 'Equip.TV': 'boolean', 'Equip.WiFi': 'category',
            'Good4Meal.breakfast': 'boolean', 'Good4Meal.brunch': 'boolean',
            'Good4Meal.dessert': 'boolean', 'Good4Meal.dinner': 'boolean',
            'Good4Meal.latenight': 'boolean', 'Good4Meal.lunch': 'boolean',
            'Parking.Bike': 'boolean', 'Parking.car': 'boolean',
            'Pay.CreditCards': 'boolean', 'Pay.DriveThru': 'boolean', 'Pay.PriceRange': 'int8',
            'Service.alcohol': 'category', 'Service.caters': 'boolean',
            'Service.delivery': 'boolean', 'Service.reservations': 'boolean',
            'Service.takeout': 'boolean', 'Service.reservations': 'boolean', 'Service.takeout': 'boolean',
            'Style.Attire': 'category', 'Style.GoodForGroups': 'boolean',
            'Style.GoodForKids': 'boolean', 'Style.NoiseLevel': 'category',
            'HOURS.Monday.Breakfast':'float16', 'HOURS.Monday.Lunch':'float16', 'HOURS.Monday.Afternoon':'float16', 'HOURS.Monday.Dinner':'float16',
            'HOURS.Tuesday.Breakfast':'float16', 'HOURS.Tuesday.Lunch':'float16', 'HOURS.Tuesday.Afternoon':'float16', 'HOURS.Tuesday.Dinner':'float16',
            'HOURS.Wednesday.Breakfast':'float16', 'HOURS.Wednesday.Lunch':'float16', 'HOURS.Wednesday.Afternoon':'float16', 'HOURS.Wednesday.Dinner':'float16',
            'HOURS.Thursday.Breakfast':'float16', 'HOURS.Thursday.Lunch':'float16', 'HOURS.Thursday.Afternoon':'float16', 'HOURS.Thursday.Dinner':'float16',
            'HOURS.Friday.Breakfast':'float16', 'HOURS.Friday.Lunch':'float16', 'HOURS.Friday.Afternoon':'float16', 'HOURS.Friday.Dinner':'float16',
            'HOURS.Saturday.Breakfast':'float16', 'HOURS.Saturday.Lunch':'float16', 'HOURS.Saturday.Afternoon':'float16', 'HOURS.Saturday.Dinner':'float16',
            'HOURS.Sunday.Breakfast':'float16', 'HOURS.Sunday.Lunch':'float16', 'HOURS.Sunday.Afternoon':'float16', 'HOURS.Sunday.Dinner':'float16'
            }
db_business = pd.read_csv(r"dataset_business.tsv",
                       #header=0, names=list(col_type.keys()),
                       dtype=bud_type,
                       sep='\t', na_values='None')


# READ REVIEW DATABASE
rvd_type = {'review_id': 'string', 'user_id': 'string', 'business_id': 'string',
            'stars': 'Int8',
            'Interact.useful': 'Int32', 'Interact.funny': 'Int32', 'Interact.cool': 'Int32',
            'content': 'string', 'date': 'string'
            }
db_review = pd.read_csv(r"dataset_review.tsv",
                       dtype=rvd_type,
                       sep='\t', na_values='None')
db_review['date'] = pd.to_datetime(db_review['date'])



# READ USER DATABASE
db_user = pd.read_csv(r"dataset_user.tsv",
                       sep='\t', na_values='None')
db_user.friends.fillna(value="[]", inplace=True)
db_user.friends = db_user.friends.apply(literal_eval)