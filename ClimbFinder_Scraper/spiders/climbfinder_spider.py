import scrapy

from ClimbFinder_Scraper.items import Climb
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
#from scrapy.spider import Spider
from scrapy.selector import Selector
import unicodedata
import string

# save info to .csv using: scrapy crawl ClimbFinder -o climbs.csv -t csv
#climbtype=['Trad', 'Sport', 'Ice', 'Aid', 'Mixed', 'Alpine', 'Boulder', 'TR']


class ClimbfinderScraper(CrawlSpider):
	name = "ClimbFinder"
	rules = [Rule(LinkExtractor(allow=['\/v\/.+\/\d+']), callback='parse_items', follow=True)]
	# for only allowing climbs: 	
	
	def __init__(self):
		super(ClimbfinderScraper, self).__init__()
		self.allowed_domains = ["mountainproject.com"]
		self.start_urls = ["http://www.mountainproject.com/v/new-york/105800424"]
  	
	rules = [Rule(LinkExtractor(allow=['\/v\/.+\/\d+']), callback = 'parse_items', follow = True)]
    
    
    
	def parse_items(self, response):
		sel = Selector(response)
		pagetype=checkpagetype(sel, response.url)
		print '******************************' 
		print '************' + pagetype  + '************'
		print '******************************' 
        
		if pagetype=='climb': #check page type, if it is a climbing page, initiate climb instance (defined in items.py)
			climb = Climb()
        
			#url
			climb['url'] = response.url
        
        	#name
			climb['name']=sel.xpath('//span[@itemprop="itemreviewed"]/text()').extract()[0]
        
        	#area & area url
			climb['area']=sel.xpath('//span[@itemprop="title"]/text()').extract()[-1] #grab last item
			climb['areaurl']='mountainproject.com'+sel.xpath('//a[@itemprop="url"]/@href').extract()[-1]
        
        	#region
			climb['region']=sel.xpath('//span[@itemprop="title"]/text()').extract()[0]
        
        	#crag
			climb['crag']=sel.xpath('//span[@itemprop="title"]/text()').extract()[1]
        
        	
        	#description (the way I am extracting this now, includes 'location' and 'protection')
			descrip1=sel.xpath('//h3[contains(text(),"Description")]/following-sibling::div/text()').extract()
			descrip2=sel.xpath('//h3[contains(text(),"Description")]/following-sibling::p[1]/text()').extract()
        	  	
			if len(descrip1)>0: 
				climb['description']= [par for par in descrip1 if par!=' ']
			elif len(descrip2)>0: 
				climb['description']=[par for par in descrip1 if par!=' ']
			else:
				climb['description']='unavailable'
        	
        	#location (don't care about this, include it to remove overlap with description)
			loc1=sel.xpath('//h3[contains(text(),"Location")]/following-sibling::div/text()').extract()
			loc2=sel.xpath('//h3[contains(text(),"Location")]/following-sibling::p[1]/text()').extract()
			if len(loc1)>0:
				climb['location']=loc1
			elif len(loc2)>0:
				climb['location']=loc2
			else:
				climb['location']='unavailable'
        	
        	#protection (note: remove protection from description) 
			prot1=sel.xpath('//h3[contains(text(),"Protection")]/following-sibling::div/text()').extract()
			prot2=sel.xpath('//h3[contains(text(),"Protection")]/following-sibling::p[1]/text()').extract()
			if len(prot1)>0:            
				climb['protection']=prot1[0]
			elif len(prot2)>0:
				climb['protection']=prot2[0]
			else:
				climb['protection']='unavailable'
            
            #grade (go with consensus rating if nothing official is available)
			grades1=sel.xpath('//span[@class="rateYDS"]/text()').extract()
			grades2=sel.xpath('//span[@class="rateHueco"]/text()').extract()
			grades3=sel.xpath('//td[contains(text(),"Consensus")]/following-sibling::td/text()').extract()
			if len(grades1)>0:
				climb['grade']=grades1[-1]
			elif len(grades2)>0:
				climb['grade']=grades2[-1]
			elif len(grades3)>0:
				climb['grade']=grades3[0]
			else:
				climb['grade']='unavailable'
            
        
        
            #number of votes - as a proxy for popularity
			try: 
				climb['number_of_votes']=sel.xpath('//meta[@itemprop="votes"]/@content').extract()[0]
			except:
				climb['number_of_votes'] = 'unavailable'
        	
        	
        	#average_rating
			try:
				climb['average_rating']=sel.xpath('//meta[@itemprop="average"]/@content').extract()[0]
			except:
				climb['average_rating']='unrated'
        
        	
        	#climb_type & length (grab anything in one piece for now, process further offline)
			try: 
				climb['climb_info']=sel.xpath('//td[contains(text(),"Type")]/following-sibling::td[1]/text()').extract()[0].split(',')
			except:
				climb['climb_info']='unavailable'
                
			# clean up text 
			for key in climb.keys():
				try:
					climb[key]=cleanhtml(climb[key])
				except:
					pass
        
			yield climb

def checkpagetype(sel, url):
    if len(sel.xpath('//span[@itemprop="itemreviewed"]/text()').extract())>0 and len(sel.xpath('//h3[contains(text(),"Climbing Season")]/text()').extract())==0:
        pagetype='climb'
    elif len(sel.xpath('//h1[@class="dkorange"]/em/text()').extract())>0 and len(sel.xpath('//h3[contains(text(),"Climbing Season")]/text()').extract())>0:
        pagetype='area'
    return pagetype

	# clean up the extracted strings
def cleanhtml(stringfromhtml, join=True):
    if type(stringfromhtml)==list:
        newstrings=[]
        for string in stringfromhtml:
            try:
                string=unicodedata.normalize('NFKD', string).encode('ascii','ignore').strip('\r\n')
            except:
                string=string.strip('\r\n')
            
            string=striprecursiveprint(string)
            newstrings.append(string)
        if join:
            newstrings='\n'.join(newstrings)
        if len(stringfromhtml)==0:
            newstrings='NULL'
    else:
        try:
            stringfromhtml=unicodedata.normalize('NFKD', stringfromhtml).encode('ascii','ignore').strip('\r\n')
        except:
            stringfromhtml=stringfromhtml.strip('\r\n')
        for rep in stringreplacements.items():
            stringfromhtml=stringfromhtml.replace(rep[0], rep[1])
        newstrings=striprecursiveprint(stringfromhtml)
    return newstrings