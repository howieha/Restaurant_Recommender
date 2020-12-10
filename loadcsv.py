# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:17:32 2020
@author: wchhuang
"""
import pandas as pd
from ast import literal_eval
import pickle


def loadcsv(db_name, db_path):
    """
    db_name : string
        LOAD SPECIFIC DATASET.
        CHOOSE FROM ['business', 'review', 'user']
    db_path : string
        PATH FOR DATA FILE.

    REQUIRES envinit() SETUP.
    """

    if db_name == 'business':
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
        db_business = pd.read_csv(db_path, dtype=bud_type,
                                  sep='\t', na_values='None')
        return db_business

    if db_name == 'review':
        # READ REVIEW DATABASE
        rvd_type = {'review_id': 'string', 'user_id': 'string', 'business_id': 'string',
            'stars': 'Int8',
            'Interact.useful': 'Int32', 'Interact.funny': 'Int32', 'Interact.cool': 'Int32',
            'content': 'string', 'date': 'string'
            }
        db_review = pd.read_csv(db_path, dtype=rvd_type,
                                sep='\t', na_values='None')
        db_review['date'] = pd.to_datetime(db_review['date'])
        return db_review

    if db_name == 'user':
        # READ USER DATABASE
        db_user = pd.read_csv(db_path, sep='\t', na_values='None')
        db_user.friends.fillna(value="[]", inplace=True)
        db_user.friends = db_user.friends.apply(literal_eval)
        return db_user


# LOAD DATA FILES
if __name__ == "__main__":
    from envinit import Dataset
    db = pickle.load(open("db.p", "rb"))
    print("LOADING DATA...")
    df_business = loadcsv('business', db.data['business'])
    df_review   = loadcsv('review', db.data['review'])
    df_user     = loadcsv('user', db.data['user'])
    print("LOAD FINISHED.")