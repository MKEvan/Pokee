import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# Create dataframe for model output
curdir = os.curdir()
traindir = curdir + '/train-data'
testdir = curdir + '/test-data'
files = list()
for file in os.listdir(testdir):
    print(file)
    files.append(file)

# files.sort()
# df = pd.DataFrame(data = files, columns = ['Filename'])

# Preprocessing steps
# train_data = load_files(raindir, load_content = True, shuffle = True, random_state = 42)
# test_data = load_files(testdir, load_content = True, shuffle = False)
# train_labels = train_data.target

# count_vect = CountVectorizer(decode_error = 'ignore')
# train_counts = count_vect.fit_transform(train_data.data)
# tf_transformer = TfidfTransformer(use_idf = False)
# train_tf = tf_transformer.fit_transform(train_counts)

# test_counts = count_vect.transform(test_data.data)
# tf_transformer = TfidfTransformer(use_idf = False)
# test_tf = tf_transformer.fit_transform(test_counts)