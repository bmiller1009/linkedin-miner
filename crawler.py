import logging
import urllib2

from globals import LOG_NAME, COOKIE_PATH
from tagparser import TagFactory, SemiKnownTagParser
from urllib2 import URLError
from parserhelper import ParserHelper as ph

#Core engine of the application.  Takes in a url, makes the request, 
#parses, and persists the html data in the response
class Crawler:
    
    _contacts_regex = "<li id='vcard-recently-[0-9]' class='vcard[^>]*>\s*(.*\n)*?\s*</li>"
    
    def __init__(self):        
    
        self.logger = logging.getLogger(LOG_NAME)
        
        try:
            with open(COOKIE_PATH) as f:
                self.cookie = f.readlines()
        except IOError as exc:
            raise IOError("%s: %s" % (COOKIE_PATH, exc.strerror))
            
    #HTTP request/response which pulls the html for a specific user list on the
    #"Who's Viewed Your Profile" section of the LinkedIn homepage. 
    def post(self, url):
        
        self.logger.info("Beginning HTTP Post.  URL='{0}'".format(url))

        user_agent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"   
        request = urllib2.Request(url)
        request.add_header("User-Agent", user_agent)
        request.add_header("Cookie", self.cookie)
        
        try:
            response = urllib2.urlopen(request)
        except URLError as exc:
            self.logger.error(exc.strerror)
            raise ValueError("Error occurred on attempt to open URL: %s" %
                             exc.strerror)
        else:
            html = response.read()
            response.close()
        
        self.logger.info("HTTP Post complete.")

        return html
    
    #Determines the contact type (known, semi-known or anonymous)
    #then parses and persists the captured data
    def save_contacts(self, html_match, entry_id=0):
        
        self.logger.info("Parsing contact...")
        
        for contact in ph.get_contacts(html_match, self._contacts_regex):
            tp = TagFactory.get_tag_parser(contact)
            
            #If the entry_id is not 0 we know it came from
            #a semi-known profile, and we set the property
            #accordingly
            if entry_id != 0:
                tp.semi_known_id = entry_id
            
            tp.save()
        
            #For semi-known tags, we pass the semi-known URL through 
            #recursively and crawl profiles returned
            if isinstance(tp, SemiKnownTagParser):
                post_html = self.post(tp.semi_known_url)
                self.save_contacts(post_html, tp.id)
        
        self.logger.info("Parsing contact complete...")