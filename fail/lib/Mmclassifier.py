import os
import json
import random
from collections import defaultdict
import numpy as np
from scipy.sparse import csc_matrix
import gzip
from csv import reader, writer
from sklearn.ensemble import RandomForestClassifier
import six


def readData(featSet = None, sample = False, seed=1234):

    read_mode, write_mode = ('r','w') if six.PY2 else ('rt','wt')

    # Decide zip based on python version
    if six.PY2:
        from itertools import izip
        zp = izip
    else:
        zp = zip

    # Set path to your consolidated files
    path = ''
    os.chdir(path)

    # File names
    ftrain = 'train.7z'
    ftest = 'test.7z'
    flabel = 'trainLabels.csv'
    fsubmission = 'submission.gz'

    print('loading started')
    # Lets read labels first as things are not sorted in files
    labels = {}
    with open(flabel) as f:
        next(f)    # Ignoring header
        for row in reader(f):
            labels[row[0]] = int(row[1])
    print('labels loaded')

    # Dimensions for train set
    ntrain = 10868
    nfeature = 16**2 + 1 + 1 # For two_byte_codes, no_que_marks, label
    train = np.zeros((ntrain, nfeature), dtype = int)
    with gzip.open(ftrain, read_mode) as f:
        next(f)    # Ignoring header
        for t,row in enumerate(reader(f)):
            train[t,:-1] = map(int, row[1:]) if six.PY2 else list(map(int, row[1:]))
            train[t,-1] = labels[row[0]]
            if(t+1)%1000==0:
                print(t+1, 'records loaded')
    print('training set loaded')

    del labels

    # Parameters for Randomforest
    random_state = 123
    n_jobs = 5
    verbose = 2


def train():
    features, labels, featDict, appHashes = readData(sample = True)
    print ("done reading")
    clf = RandomForestClassifier(random_state=random_state, n_jobs=n_jobs, verbose = verbose)
    # Start training
    print('training started')
    clf.fit(train[:,:-1], train[:,-1])
    print('training completed')

    # We don't need training set now
    del train

    # Dimensions for train set
    ntest = 10873
    nfeature = 16**2 + 1 # For two_byte_codes, no_que_marks
    test = np.zeros((ntest, nfeature), dtype = int)
    Ids = []    # Required test set ids

    with gzip.open(ftest, read_mode) as f:
        next(f)    # Ignoring header
        for t,row in enumerate(reader(f)):
            test[t,:] = map(int, row[1:]) if six.PY2 else list(map(int, row[1:]))
            Ids.append(row[0])
            if(t+1)%1000==0:
                print(t+1, 'records loaded')
    print('test set loaded')