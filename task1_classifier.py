"""
Created on Mon Mar 24 13:53:28 2019
@author: nehabhomia
"""

import pandas as pd
from sklearn import datasets, model_selection, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV

#importing data

tweets = pd.read_csv('task1_training.tsv', delimiter='\t')