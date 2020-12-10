# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:49:43 2020
@author: wchhuang
"""

from os import path, chdir, stat
import sys
from glob import glob
from datetime import datetime
import json
import pickle
import warnings

basedir_default = path.dirname(__file__)    # CURRENT DIRECTORY


class Dataset:
    """
        DATASET ENVIRONMENT.

        ATTRIBUTES
            name:       database name
            basedir:    base directory for codes
            datadir:    database location
            data:       dict of dataset files

        METHODS
            setup():    Switch to database location.
            check_db(): Check uniqueness and timetag for data files.
    """
    def __init__(self, initname='dataset', initdir=basedir_default):
        self.basedir = initdir                  # BASE DIRECTORY
        self.name    = initname                 # DATASET NAME
        self.datadir = self.basedir \
                        + r'\\data\\' \
                        + self.name             # DATA DIRECTORY
        self.data    = {'business': None, 'review': None, 'user': None}

    def setup(self):
        chdir(self.datadir)                     # CHANGE TO DATA DIR
        sys.path.append(self.basedir)
        sys.path.append(self.basedir + r'\\Content-based')
        sys.path.append(self.basedir + r'\\Misc')
        print('===== DATABASE SETUP =====')
        print('NAME = %s' % self.name)
        print('BASEDIR = %s' % self.basedir)
        print('DATADIR = %s' % self.datadir)
        print()

    def store_json(self, filename):
        env = {'name': self.name,
               'dir': {'basedir': self.basedir, 'datadir': self.datadir},
               'datafiles': self.data}
        with open(filename, 'w') as outfile:
            json.dump(env, outfile)

    def validate(self, db_name):
        files = glob('*' + db_name + '*.tsv')   # SEARCH FILE LIST
        if files:                               # IF NOT EMPTY, CHECK VERSION
            if len(files) == 1:
                finfo = stat(files[0])
                self.data[db_name] = files[0]
                fedit = datetime.fromtimestamp(finfo.st_mtime)
                print('"%s" \tLAST EDITED:\t%s' %
                      (db_name, fedit.strftime('%Y-%m-%d %H:%M')))
                return True
            else:                               # IF MULTIPLE, WARN
                warnings.warn('Multiple files found for "%s".' % db_name)
                return False
        else:                                   # IF NON-EXIST, WARN
            warnings.warn('"%s" data not found.' % db_name)
            return False

    def check_db(self):
        print('===== DATABASE VALIDATION =====')
        if all([self.validate('business'),
                self.validate('review'),
                self.validate('user')]):
            self.store_json(self.basedir + r'\\env.json')
            print('===== SETUP COMPLETE =====\n')
        else:
            print('SETUP FAILED. PLEASE RESET THE DATA ENVIRONMENT.')
            print('===== SETUP FAILED =====\n')


# SETUP DATASET LOCATION
if __name__ == "__main__":
    db = Dataset(initname='prototype')
    # db = Dataset(initname='test')
    db.setup()
    db.check_db()
    pickle.dump(db, open("db.p", "wb"), pickle.HIGHEST_PROTOCOL)
    del basedir_default