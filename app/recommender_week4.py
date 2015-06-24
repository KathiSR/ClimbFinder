import pandas
import numpy as np
import re
import pylab
from sklearn.metrics.pairwise import cosine_similarity
import MySQLdb as mdb

# set up connection with sql server
con = mdb.connect('localhost', 'root', '', 'climbfinder_test')


def get_refclimb(name, crag = None):
    if crag == None:
        sql  = "SELECT * FROM Features WHERE name LIKE '%(name)s'" %{"name": name}
        ref_climb = pandas.read_sql_query(sql=sql, con=con)
    else:
        sql  = "SELECT * FROM Features WHERE name LIKE '%(name)s' AND crag LIKE '%(crag)s'" %{"name": name, "crag": crag}
        ref_climb = pandas.read_sql_query(sql=sql, con=con) 
    
    return ref_climb
    
    	

def get_comparisonclimbs(region = None, yes = 'yes', no = 'no'):
    if region != None:
        sql  = "SELECT * FROM Features WHERE region LIKE '%(region)s' AND %(yes)s = 1 AND %(no)s = 0" %{"region": region,
                                                                                                      "yes": yes, 
                                                                                                      "no":no}
    else: 
        sql  = "SELECT * FROM Features WHERE %(yes)s = 1 AND %(no)s = 0" %{"yes": yes, "no":no}
    
    comparisonclimbs = pandas.read_sql_query(sql=sql, con=con)
    return comparisonclimbs	
    
    
def get_max_sim(ref_climb, comparisonclimbs, n = 5,):
    features = ['toprope',
       'sport', 'trad', 'alpine', 'ice', 'aid', 'bouldering', 'pitches',
       'grade_num', 'anchor', 'arete', 'awkward', 'block',
       'bolt', 'boulder', 'bulge', 'broken', 'canyon', 'buttress',
       'chains', 'chimney', 'classic', 'clean','corner', 'crack',
       'crimps', 'crux', 'difficult', 'dihedral', 'exposure', 'face',
       'finger', 'flake', 'gully', 'hand', 'jug', 'ledge', 'lip',
       'jam', 'notch', 'moderate', 'ridge', 'vertical', 'horizontal',
       'mantle', 'offwidth', 'overhang','pillar', 'pocket', 'protect',
       'ramp', 'rappel', 'roof', 'scramble', 'seam', 'slab', 'sloper',
       'solid', 'stance', 'steep', 'stemming', 'sustained', 'technical',
       'tower', 'traverse', 'undercling', 'average_rating']
    
    ref_climb = ref_climb[features]
    
    if len(comparisonclimbs) == 0:
        topfive = None
        return topfive
    
    else:
    	comparisonclimbs = comparisonclimbs.ix[:,features]
    
    	similarities = cosine_similarity(ref_climb, comparisonclimbs)
    	similarities_df = pandas.DataFrame(similarities).transpose().sort(0, ascending = False)
    
    	if len(similarities_df) >= 5:
        	topfive = similarities_df[:5]
    	elif len(similarities_df) <= 5:
        	if len(similarities_df) > 0:
				topfive = similarities_df[:len(similarities_df)]
        	else: 
				topfive = None
    
    return topfive
    

def get_climb_info(topfive, comparisonclimbs):
    climbinfo = comparisonclimbs.ix[topfive.index,:]
    climbinfo.reset_index(inplace = True)
    
    return climbinfo  

    

	
	
	
	
    
    
    
    
    