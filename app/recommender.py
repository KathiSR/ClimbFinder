import pandas
import numpy as np
import re
import pylab as P
from math import sqrt 

### read in the .csv file
data = pandas.read_csv("./app/cleaned_data.csv", header = 0, index_col = 0)

### compute Euclidean distance
def sim_distance(data, climb1, climb2):
    # get the list of shared_items
    shared_features = {}
    
    for feature in data.columns:
        if not pandas.isnull(data.ix[climb1, feature]):     #check if the feature exists for climb1
            if not pandas.isnull(data.ix[climb2, feature]): #check if the feature also exists for climb2
                shared_features[feature]=1
        
    
    if len(shared_features)==0: return 0
    

    sum_of_squares = sum([pow(data.ix[climb1, item] - data.ix[climb2, item],2)
                          for item in shared_features])
    
    return 1/(1+sqrt(sum_of_squares))

### rank climbs by Euclidean distance
def topMatches(data, climb, n = 5, similarity = sim_distance):
    scores = [(similarity(data, climb, other),other)
             for other in data.index if other != climb]


    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]
    
    