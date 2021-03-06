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
	print crag
	
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


	
	try:
		
		### retrieve the reference climb from sql
		refclimb = get_refclimb(climb, crag)
		available_crags = refclimb.crag
		if len(refclimb) > 1:
		
			error = "Sorry! Climbs named '%(climb)s' were found in the following crags:" %{"climb": climb.title()}
			error2 = "Please try again and specify crag."
			
			return render_template("except_duplicateclimbs.html", the_result = error, the_crags = refclimb.crag, the_result_2 = error2)
	
		if len(refclimb) == 0:
			error = "Sorry! Climb '%(climb)s' not found in database. Please check back soon - we are working on expanding the database." %{"climb": climb.title()}
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
		area_info = climb_info.crag, grade_info = climb_info.grade, url_info = climb_info.url,
		average_rating_info = climb_info.average_rating, length = climb_info.pitches, type = climb_info.type)
			
	except:
		
		### if it didn't work, return a generic error message
		error = 'Sorry, something went wrong :(. Please try again.'
		return render_template("except.html",  the_result = error)
	
	