from flask import render_template, request
from app import app
import pymysql as mdb
from recommender_week4 import *


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
	
	#set up the connection with the sql database
	con = setup_con('climbfinder_test')
	
	#pull 'ID' from input field and store it
	error = []
	climb = request.args.get('climb')
	print climb
	
	if request.args.get('crag'):
		crag = request.args.get('crag')
	else: crag = None
	
	if request.args.get('region'):
		region = request.args.get('region')
	else: region = None
		
	if request.args.get('yes'):
		yes = request.args.get('yes')
	else: yes = 'yes'
	
	if request.args.get('no'):
		no = request.args.get('no')
	else: no = 'no'


	
	try:
		
		### retrieve the reference climb from sql
		refclimb = get_refclimb(climb, crag)
	
		if len(refclimb) > 1:
			error = "Sorry! More than one climb named '%(climb)s' found in database. Please specify crag." %{"climb": climb.title()}
			return render_template("except.html", the_result = error)
	
		if len(refclimb) == 0:
			error = "Sorry! Climb '%(climb)s' not found in database." %{"climb": climb.title()}
			return render_template("except.html",  the_result = error)
		
	
		### retrieve the reference climb from sql
		comparisonclimbs = get_comparisonclimbs(region, yes, no)

		if len(comparisonclimbs) == 0:
			error = 'No climbs matching your criteria found in database.'
			return render_template("except.html",  the_result = error)
	
		
		### get the top five most similar climbs
		topfive = get_max_sim(refclimb, comparisonclimbs)
		
		### retrieve the information for the five climbs
		climb_info = get_climb_info(topfive, comparisonclimbs)

		
		### feed into output page
		return render_template("output.html", the_result = climb_info.name, region_info = climb_info.region,
			area_info = climb_info.area, grade_info = climb_info, url_info = climb_info.url,
			average_rating_info = climb_info.average_rating)
			
	except:
		
		### if it didn't work, return a generic error message
		error = 'Sorry, something went wrong :('
		return render_template("except.html",  the_result = error)
	
	