import scrapy

from ClimbFinder_Scraper.items import Climb
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import unicodedata
import string

# save info to .csv using: scrapy crawl ClimbFinder -o climbs.csv -t csv
climbtype=['Trad', 'Sport', 'Ice', 'Aid', 'Mixed', 'Alpine', 'Boulder', 'TR']



class ClimbfinderScraper(CrawlSpider):
    name = "ClimbFinder_orig"
    rules = [Rule(LinkExtractor(allow=['\/v\/.+\/\d+']), callback='parse_items', follow=True)]
    def __init__(self):
        super(ClimbfinderScraper, self).__init__()
        self.allowed_domains = ["mountainproject.com"]
        self.start_urls = ["http://www.mountainproject.com/v/new-york/105800424"]
  	
    #f = open('climbs.csv', 'rU')
    #lines = f.readlines()
    #f.close
    #start_urls = []
    #for line in lines:
    #   start_urls.append('http://www.mountainproject.com' + line)
	
    
    def parse_items(self, response):

        
        sel = Selector(response)
        pagetype=checkpagetype(sel, response.url)
        print '******************************' 
        print '************' + pagetype  + '************'
        print '******************************' 
        
        if pagetype=='climb':
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
        
        	#description
            descrip1=sel.xpath('//h3[contains(text(),"Description")]/following-sibling::div/text()').extract()
            descrip2=sel.xpath('//h3[contains(text(),"Description")]/following-sibling::p[1]/text()').extract()
        	
            if len(descrip1)>0: 
                climb['description']=[par for par in descrip1 if par!=' ']
            elif len(descrip2)>0: 
                climb['description']=[par for par in descrip2 if par!=' ']
            else:
                climb['description']='unavailable'
            
        	#protection
            prot1=sel.xpath('//h3[contains(text(),"Protection")]/following-sibling::div/text()').extract()
            prot2=sel.xpath('//h3[contains(text(),"Protection")]/following-sibling::p[1]/text()').extract()
            if len(prot1)>0:            
                climb['protection']=prot1[0]
            elif len(prot2)>0:
                climb['protection']=prot2[0]
            else:
                climb['protection']='unavailable'
        
        	
            
            #grade
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
            
        
        
            #number of votes
            try: 
                climb['number_of_votes']=sel.xpath('//meta[@itemprop="votes"]/@content').extract()[0]
            except:
            	climb['number_of_votes'] = 'unavailable'
        	
        	
        	#average_rating
            try:
                climb['average_rating']=sel.xpath('//meta[@itemprop="average"]/@content').extract()[0]
            except:
                climb['average_rating']='unrated'
        
        	
        	#climb_type & length
            climb_info=sel.xpath('//td[contains(text(),"Type")]/following-sibling::td[1]/text()').extract()[0].split(',')
            climb['climbtype']=climb_info[0]
            climb['pitches']='1 p' #assume 1 pitch unless designated otherwise
            climb['length']='unavailable'
            for info in climb_info[1:]:
                if 'pitch' in info:            
                    climb['pitches']=info[1:] #weird space before pitch lengths
                elif info not in climbtype and "'" in info:
                    climb['length']=info
        	
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
    elif len(sel.xpath('//h1/text()').extract())>0 and 'personalpage' in url:
        pagetype='xxxclimberinfo'
    elif 'action=ticks' in url and 'printer=1' not in url and '&export=1' not in url and 'breakdown' not in url:
        pagetype='ticks'
    elif 'what=RATING' in url and 'printer=1' not in url and 'printer=1p' not in url:
        pagetype='grades'
    elif 'what=COMMENT' in url and 'printer=1' not in url and 'printer=1p' not in url:
        pagetype='comments'
    elif 'what=SCORE' in url and 'printer=1' not in url and 'printer=1p' not in url:
        pagetype='stars'
    elif 'action=todos' in url:
        pagetype='todos'
    else:
        pagetype='uncategorized'
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