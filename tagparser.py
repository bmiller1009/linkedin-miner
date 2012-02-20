import abc
from entryrecord import EntryRecord
from globals import *
from parserhelper import ParserHelper
import logging

class TagParser(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, html):
        self._html = html
        self._entry_record = EntryRecord()
        self._logger = logging.getLogger(LOG_NAME) 

    @abc.abstractmethod
    #protected abstract method: Parses the html in the tag
    def _parse_tag(self, input):
        return

    #Enumeration for different parsed html tags
    (Anon, Semiknown, Known) = range(1,4)
    
    @property
    def html(self):
        return self._html
    
    @property
    def entry_record(self):
        return self._entry_record

    @entry_record.setter
    def entry_record(self, value):
        self._entry_record = value
    
    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._entry_record = value

    #Persists the parsed html data to the database
    def save_tag_contents(self):
        self._entry_record = self._parse_tag(self)
        entry_id = self._entry_record.save()
        return entry_id        

    def __repr__(self):
        return "[TagParser: EntryRecord={0}]".format(self._entry_record)

#This class handles parsing logic for anonymous contacts
class AnonTagParser(TagParser):

    def __init__(self, html):
        TagParser.__init__(self, html)
    
    #Parses the tag
    def _parse_tag(TagParser, self):
        
        try:

            TagParser.entry_record.entry_type_id = TagParser.Anon
            TagParser.entry_record.entry_name = 'Anonymous LinkedIn User'
            TagParser.entry_record.profile_url = ''
            TagParser.entry_record.entry_job_title = ''
            TagParser.entry_record.entry_location = ''
            TagParser.entry_record.entry_region = ''
            TagParser.entry_record.semi_known_main_entry_id = 0

            return TagParser.entry_record
       
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

#This class handles parsing logic for semi-known contacts
class SemiKnownTagParser(TagParser):

    def __init__(self, html):
        TagParser.__init__(self, html)
        self.SEMI_REGEX_PATTERN = "<a href='/wvmx/profile/redherring?[^>]*>.*</a>"

    @property
    def main_entry_id(TagParser):
        return TagParser.entry_record.entry_id

    @property
    def semi_known_url(TagParser):
        return TagParser.entry_record.profile_url

    #Parses the tag
    def _parse_tag(TagParser, self):

        try:

            TagParser.entry_record.entry_type_id = TagParser.Semiknown
            TagParser.entry_record.entry_name = self.get_semi_known_description(TagParser)
            TagParser.entry_record.profile_url = self.get_semi_known_url(TagParser)
            TagParser.entry_record.entry_job_title = ''
            TagParser.entry_record.entry_location = ''
            TagParser.entry_record.entry_region = ''
            TagParser.entry_record.semi_known_main_entry_id = 0
    
            return TagParser.entry_record
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

    #Parses the semi-known description from a contact in the html list
    def get_semi_known_description(self, TagParser): 
        
        try:
            
            tag = ParserHelper.regex_return_first_match(TagParser.html, self.SEMI_REGEX_PATTERN)
            return ParserHelper.get_text_between_tags(tag)
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

    #Gets the semi known URL
    def get_semi_known_url(self, TagParser):
        
        try:
            
            tag = ParserHelper.regex_return_first_match(TagParser.html, self.SEMI_REGEX_PATTERN)
        
            start_index = tag.index("href='/")
            title_index = tag.index("trk=")
            
            return LINKEDIN_URL + ParserHelper.clean_data(tag[start_index + 7:title_index])
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

#This class handles parsing logic for fully identified contacts
class IdentTagParser(TagParser):

    def __init__(self, html, semi_known_id):
        TagParser.__init__(self, html)

        if semi_known_id == None:
            self.semi_known_id = 0
        else:
            self.semi_known_id = semi_known_id

    #Parses the tag
    def _parse_tag(TagParser, self):
        
        try:

            TagParser.entry_record.entry_type_id = TagParser.Known
            TagParser.entry_record.entry_name = self.get_entry_name()
            TagParser.entry_record.profile_url = self.get_profile_url()
            TagParser.entry_record.entry_job_title = self.get_entry_job_title()
            TagParser.entry_record.entry_location = self.get_entry_location()
            TagParser.entry_record.entry_region = self.get_entry_industry()
            TagParser.entry_record.semi_known_main_entry_id = self.semi_known_id
            TagParser.entry_record.shares_groups = self.get_entry_shares_groups()
            TagParser.entry_record.shares_connections = self.get_entry_shares_connections()

            return TagParser.entry_record
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

    #Gets the name of the entry
    def get_entry_name(TagParser):

        try:

            tag = ParserHelper.regex_return_first_match(TagParser.html, " title='View profile'>.*</a>")
            return ParserHelper.get_text_between_tags(tag)

        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

    #Gets the profile URL
    def get_profile_url(TagParser):

        try:

            url_prefix = LINKEDIN_URL + "profile/view?id="
            tag = ParserHelper.regex_return_first_match(TagParser.html, "<a href='/profile[^>]*>")

            index_of_string = ''
            title_string = ''

            if tag.find("view?id"):
                index_of_string = "id="
                title_string = "&amp;authType"
            elif tag.find("viewProfile=&amp"):
                index_of_string = "key="
                title_string = "&amp;authToken"

            offset = len(index_of_string)

            start_index = tag.index(index_of_string)
            title_index = tag.index(title_string)

            return url_prefix + ParserHelper.clean_data(tag[start_index + offset:title_index])
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

    #Gets the entry job title
    def get_entry_job_title(TagParser):
        
        try:

            tag = ParserHelper.regex_return_first_match(TagParser.html, "<dd class='title'>.*</dd>")
            return ParserHelper.get_text_between_tags(tag)
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise
    
    #Gets the entry location
    def get_entry_location(TagParser):
        
        try:
        
            tag = ParserHelper.regex_return_first_match(TagParser.html, "<span class='location'>.*</span>")
            return ParserHelper.get_text_between_tags(tag)
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise

    #Gets the entry industry
    def get_entry_industry(TagParser):
        
        try:

            tag = ParserHelper.regex_return_first_match(TagParser.html, "<span class='industry'>.*</span>")
            return ParserHelper.get_text_between_tags(tag)
        
        except:
            TagParser.logger.error(sys.exc_info()[0])
            raise
    
    #Gets the entry shares groups
    def get_entry_shares_groups(TagParser):
        if TagParser.html.find("<div class='shared-groups'>") != -1:
            return 1
        else:
            return 0

    #Gets the entry shares connections
    def get_entry_shares_connections(TagParser):
        if TagParser.html.find("<div class='shared-connections'") != -1:
            return 1
        else:
            return 0

class TagFactory:
    
    @staticmethod
    def get_tag_parser(html, semi_known_id):
        
        if html.find("Anonymous LinkedIn User") != -1:
            return AnonTagParser(html)
        elif html.find("redherring") != -1:
            return SemiKnownTagParser(html)
        else:
            return IdentTagParser(html, semi_known_id)
