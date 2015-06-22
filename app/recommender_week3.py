import pandas
import numpy as np
import re
import pylab
from sklearn.metrics.pairwise import cosine_similarity

features_df = pandas.read_csv("./app/features_short.csv", header = 0, index_col = 0)

# calculate similarity matrix
cluster_data = features_df.ix[:,['anchor', 'arete', 'awkward', 'block', 'bolt', 'boulder', 'bulge', 'broken', 'canyon',
           'buttress', 'chains', 'chimney', 'classic', 'clean', 'corner', 'crack', 'crimps', 'crux', 
           'difficult','dihedral', 'exposure', 'face', 'finger', 'flake', 'gully', 'hand', 'jug', 'lip', 
           'jam', 'ledge','notch', 'moderate', 'ridge', 'vertical', 'horizontal','mantle', 'offwidth',
           'overhang', 'pillar', 'pocket', 'protect', 'ramp','rappel', 'roof', 'scramble', 'seam', 'slab',
           'sloper', 'solid', 'stance', 'steep', 'stemming', 'sustained',
           'technical', 'tower', 'traverse', 'undercling','toprope', 'sport', 'trad', 'ice','aid']]
           
similarity_matrix = cosine_similarity(cluster_data, cluster_data)
sim_df = pandas.DataFrame(similarity_matrix, columns=cluster_data.index, index=cluster_data.index)


def get_max_sim(ref_climb, region = None, yes = 'yes', no = 'no', sim_df = sim_df, features_df = features_df, n = 5,):
	noclimb = 0

	#get group of climbs that match criteria
	if region:
		criteria_matched = features_df[(features_df['region']== region) & (features_df[yes]==1) & (features_df[no]==0)]
	else:
		criteria_matched = features_df[(features_df[yes]==1) & (features_df[no]==0)]    
    
    #get the similarity scores for the reference climb 
	scores = sim_df.ix[ref_climb]
    
    #find the intersect and rank them
	overlap = scores.ix[criteria_matched.index]
	overlap.sort(axis=0,ascending=False)
    
    
    # find climbs that have matching criteria
	if len(overlap.index) == 0:  
		overlap = 'No climbs with matching criteria found :('
		noclimb = 1
    
    		
	elif len(overlap.index) < n: 
		n = len(overlap.index) - 1
		
		if overlap.index[0] == ref_climb: 
			overlap = overlap[1:n+1]
		else:
			overlap = overlap[:n+1]
        	
        	
	elif len(overlap.index) >= n: #n or more climbs
		n = n
    	
		if overlap.index[0] == ref_climb:
			overlap = overlap[1:n+1]
		else:
			overlap = overlap[:n+1]
    	
    # get more information about top climbs
	climbInfo = features_df.ix[overlap.index]
    
    # get more information about reference climb
	refclimbInfo = features_df.ix[ref_climb]
    
	return overlap, climbInfo, refclimbInfo
    

	
	
	
	
    
    
    
    
    