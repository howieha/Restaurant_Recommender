# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:04:24 2020
@author: wchhuang
"""
import numpy as np
from envinit import Dataset
import json
import loadcsv
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle


def normalize(df, na_value):
    """
    Parameters
    ----------
    df : PANDAS DATAFRAME. Dataframe input for normalization.
    na_value : NON-ITERATABLE OBJECT. NA indicators (0, False, ...).

    Returns
    -------
    PANDAS DATAFRAME AFTER NORMALIZATION.
    """
    df0 = df.fillna(na_value, inplace=False)
    mean_df0 = np.mean(df0, axis=0)
    std_df0  = np.std(df0, axis=0)
    return (df0 - mean_df0) / std_df0


def corr(df, ccmethod='pearson',
         norm=True, include_loc=True, weight_loc=1, cutoff=0.20):
    """
    Parameters
    ----------
    df : PANDAS DATAFRAME. Dataframe input for correlation coefficient.
    ccmethod : CATEGORICAL ('pearson', 'spearman'). Corr Coeff method.
    norm : BOOLEAN, default = True. Normalization for features.
    include_loc : BOOLEAN, default = True. Include location features.
    weight_loc : INTEGER, default = 1. Weight for location features.
    cutoff : FLOAT (0-1), default = 0.20. Cutoff for Corr Coeff.

    Returns
    -------
    cctot : 2-D Array. Overall correlation coefficient matrix.
    cccat : 2-D Array. Correlation coefficient matrix for categoricals.
    ccloc : 2-D Array. Correlation coefficient matrix for location.
    """
    # PARAM VALIDATION
    if not include_loc:
        if weight_loc != 0:
            raise ValueError('For include_loc = False, location weight must be 0.')
            return
    else:
        if weight_loc < 0:
            raise ValueError('Location weight must be larger than 0.')
            return

    # PREPROCESSING
    dfcat = df.filter(regex='^CAT',axis=1)          # FILTER CATEGORICAL FEATURE
    dfloc = df.loc[:, ['latitude', 'longitude']]    # FILTER GPS FEATURE
    if norm:                                        # NORMALIZED CATEGORICALS
        dfcat = normalize(dfcat, False)
        dfloc = normalize(dfloc, 0)

    # CORRELATION COEFFICIENT
    cccat   = dfcat.T.corr(method=ccmethod)
    cccat   = cccat.to_numpy()
    ccloc   = dfloc.T.corr(method=ccmethod)
    ccloc   = ccloc.to_numpy() if include_loc else np.zeros(dfcat.shape)

    # OVERALL CORRELATION COEFFICIENT
    catN  = dfcat.shape[1]                      # CATEGORICAL FEATURE NUMBER
    cctot = cccat * catN/(catN + weight_loc) \
            + ccloc * weight_loc/(catN + weight_loc)    # WEIGHTED CC

    # CUTOFF FOR UNCORRELATED
    cctot[cctot < cutoff] = 0

    return cctot, cccat, ccloc


if __name__ == "__main__":
    # LOAD DATA FROM JSON ENV FILE
    with open('env.json') as infile:
        dbinfo = json.load(infile)
    db = Dataset(initname=dbinfo['name'], initdir=dbinfo['dir']['basedir'])
    db.setup()
    db.check_db()
    del dbinfo, infile
    df_business = loadcsv.load('business', db.data['business'])

    pctot, pccat, pcloc = corr(df_business)
    pickle.dump(pctot, open("pctot.p", "wb"))

    # PLOT CORR COEFFICIENT HEATMAP
    fig1 = plt.figure(figsize=(12, 12))
    plt.rcParams['font.size'] = 10
    plt.imshow(pctot, cmap=cm.RdBu)
    plt.title('Pearson Correlation, Overall')
    plt.show()

    # PLOT CORR COEFFICIENT DISTRIBUTION
    fig2 = plt.figure(figsize=(12, 12))
    plt.rcParams['font.size'] = 10
    plt.hist(pctot.flatten(), bins=80)
    plt.title('Pearson Correlation Distribution')
    fig2.show()