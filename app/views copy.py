from flask import render_template, request
from app import app
import pymysql as mdb
from recommender_week3 import *


#db = mdb.connect(user="root", host="localhost", db="world_innodb",
#	charset='utf8')

#@app.route('/')
#def climbfinder_input():
#	return render_template("input.html")


@app.route('/')
def climbfinder_input():
	return render_template("input.html")

@app.route('/output')
def climbfinder_output():
	#pull 'ID' from input field and store it
	error = []
	climb = request.args.get('climb')
	
	if request.args.get('region'):
		region = request.args.get('region')
	else: region = None
	
	print region
		
	if request.args.get('yes'):
		yes = request.args.get('yes')
	else: yes = 'yes'
	print yes
	
	if request.args.get('no'):
		no = request.args.get('no')
	else: no = 'no'
	print no
	
	try:
		(overlap, climb_info, refclimb_info) = get_max_sim(climb, region, yes, no, sim_df = sim_df, features_df = features_df, n = 5)	
		return render_template("output.html", the_result = overlap.index, region_info = climb_info.region,
				area_info = climb_info.area, grade_info = climb_info.grade, url_info = climb_info.url,
				average_rating_info = climb_info.average_rating)
	except:
		error = 'Sorry! Climb not found in database :('
		return error
	