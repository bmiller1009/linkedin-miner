from globals import *
from tagparser import *
import logging
import urllib
import urllib2
import re
import sys

#Core engine of the application.  Takes in a url, makes the request, parses, and persists the html data in the response
class Crawler:
	
    def __init__(self):		
	
        self.logger = logging.getLogger(LOG_NAME)

        try:
	    f = open(COOKIE_PATH)
	except:
            self.logger.error(sys.exc_info()[0])
	else:
	    self.cookie = f.readlines()
	    f.close()		

    #HTTP request/response which pulls the html for a specific user list on the "Who's Viewed Your Profile" section of the LinkedIn homepage. 
    def post(self, url, semi_known_id):
        
        self.logger.info("Beginning HTTP Post.  URL='"+ url + "'")

	pagedata = ''
	user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'	
	request = urllib2.Request(url)
	request.add_header('User-Agent', user_agent)
	request.add_header('Cookie', self.cookie)
	    
        try:
	    response = urllib2.urlopen(request)
        except:
            self.logger.error(sys.exc_info()[0])
        else:
	    pagedata = response.read()
        
        self.logger.info("HTTP Post complete.")

	self.get_contacts(pagedata.replace("\"","'"), semi_known_id)		
        
    #Loops through all of the contacts found in the requested html text
    def get_contacts(self, html, semi_known_id):
        
        self.logger.info("Extracting contacts from captured html...")
        
        try:

	    pattern = "<li id='vcard-recently-[0-9]' class='vcard[^>]*>\s*(.*\n)*?\s*</li>"	
		
	    for match in re.finditer(pattern, html):
                self.determine_parse(html[match.start():match.end()], semi_known_id)
        
        except:
            self.logger.error(sys.exc_info()[0])
            raise

        self.logger.info("Extraction of contacts from html is complete.")
    
    #Determines the contact type (known, semi-known or anonymous) then parses and persists the captured data
    def determine_parse(self, html_match, semi_known_id):
        
        self.logger.info("Parsing contact...")
        
        try:

            tp = TagFactory.get_tag_parser(html_match, semi_known_id)
            entry_id = tp.save_tag_contents()
            
            #For semi-known tags, we pass the semi-known URL through recursively and crawl profiles returned
            if isinstance(tp, SemiKnownTagParser):
                self.post(tp.semi_known_url, entry_id)
        
        except:
            self.logger.error(sys.exc_info()[0])
            raise

        self.logger.info("Parsing contact complete...")
