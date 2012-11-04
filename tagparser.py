import abc
from entryrecord import EntryRecord
from globals import LOG_NAME, LINKEDIN_URL
from parserhelper import ParserHelper
import logging

class TagParser(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, html):
        self.html = html
        self.entry_record = EntryRecord()
        self.logger = logging.getLogger(LOG_NAME) 
        self.id = 0

    @abc.abstractmethod
    #protected abstract method: Parses the html in the tag
    def _parse_tag(self, html_tag):
        return

    #Enumeration for different parsed html tags
    (Anon, Semiknown, Known) = range(1,4)

    #Persists the parsed html data to the database
    def save(self):
        self._entry_record = self._parse_tag(self)
        self.id = self.entry_record.save()       

    def __repr__(self):
        return "[TagParser: EntryRecord={0}]".format(self._entry_record)

#This class handles parsing logic for anonymous contacts
class AnonTagParser(TagParser):

    def __init__(self, html):
        TagParser.__init__(self, html)
    
    def _parse_tag(self, TagParser):
        
        TagParser.entry_record.entry_type_id = TagParser.Anon
        TagParser.entry_record.entry_name = 'Anonymous LinkedIn User'
        TagParser.entry_record.profile_url = ''
        TagParser.entry_record.entry_job_title = ''
        TagParser.entry_record.entry_location = ''
        TagParser.entry_record.entry_region = ''
        TagParser.entry_record.semi_known_main_entry_id = 0
    
        return TagParser.entry_record

#This class handles parsing logic for semi-known contacts
class SemiKnownTagParser(TagParser):

    def __init__(self, html):
        TagParser.__init__(self, html)
        self.REGEX = "<a href='/wvmx/profile/redherring?[^>]*>.*</a>"

    @property
    def main_entry_id(TagParser):
        return TagParser.entry_record.entry_id

    @property
    def semi_known_url(TagParser):
        return TagParser.entry_record.profile_url

    def _parse_tag(self, TagParser):

        TagParser.entry_record.entry_type_id = TagParser.Semiknown
        TagParser.entry_record.entry_name = self.get_description(TagParser)
        TagParser.entry_record.profile_url = self.get_url(TagParser)
        TagParser.entry_record.entry_job_title = ''
        TagParser.entry_record.entry_location = ''
        TagParser.entry_record.entry_region = ''
        TagParser.entry_record.semi_known_main_entry_id = 0

        return TagParser.entry_record

    #Parses the semi-known description from a contact in the html list
    def get_description(self, TagParser): 

        tag = ParserHelper.match_first_pattern(TagParser.html, self.REGEX)
        return ParserHelper.extract_tag_text(tag)

    #Gets the semi known URL
    def get_url(self, TagParser):

        tag = ParserHelper.match_first_pattern(TagParser.html, self.REGEX)
    
        start_index = tag.index("href='/")
        title_index = tag.index("trk=")
        
        #TODO:  Clean this up
        return LINKEDIN_URL + \
            ParserHelper.clean_data(tag[start_index + 7:title_index])

#This class handles parsing logic for fully identified contacts
class IdentTagParser(TagParser):

    def __init__(self, html):
        TagParser.__init__(self, html)

        self.semi_known_id = 0

    #Parses the tag
    def _parse_tag(self, TagParser):
        
        TagParser.entry_record.entry_type_id = TagParser.Known
        TagParser.entry_record.entry_name = self.name(TagParser)
        TagParser.entry_record.profile_url = self.profile_url(TagParser)
        TagParser.entry_record.job_title = self.job_title(TagParser).replace("'", "")
        TagParser.entry_record.location = self.location(TagParser).replace("'", "")
        TagParser.entry_record.region = self.industry(TagParser).replace("'", "")
        TagParser.entry_record.semi_known_main_entry_id = self.semi_known_id
        TagParser.entry_record.shares_groups = self.shares_groups(TagParser)
        TagParser.entry_record.shares_connections = self.shares_connections(TagParser)

        return TagParser.entry_record

    #Gets the name of the entry
    def name(self, TagParser):
        
        pattern = " title='View profile'>.*</a>"
        tag = ParserHelper.match_first_pattern(TagParser.html, pattern)
        return ParserHelper.extract_tag_text(tag)

    #Gets the profile URL
    def profile_url(self, TagParser):
        
        pattern = "<a href=(.*)/profile[^>]*>"
        url = "{0}profile/view?id=".format(LINKEDIN_URL)
        tag = ParserHelper.match_first_pattern(TagParser.html, pattern)

        index_of_string = ''
        title_string = ''

        if tag.find("view?id"):
            index_of_string = "id="
            title_string = "&amp;authType"
        elif tag.find("viewProfile=&amp"):
            index_of_string = "key="
            title_string = "&amp;authToken"

        offset = len(index_of_string)

        start_index = offset + tag.index(index_of_string)
        title_index = tag.index(title_string)
        
        return url + ParserHelper.clean_data(tag[start_index:title_index])

    #Gets the entry job title
    def job_title(self, TagParser):
        
        pattern = "<dd class='title'>.*</dd>"
        tag = ParserHelper.match_first_pattern(TagParser.html, pattern)
        return ParserHelper.extract_tag_text(tag)

    #Gets the entry location
    def location(self, TagParser):
        
        pattern = "<span class='location'>.*</span>"
        tag = ParserHelper.match_first_pattern(TagParser.html, pattern)
        return ParserHelper.extract_tag_text(tag)

    #Gets the entry industry
    def industry(self, TagParser):
        
        pattern = "<span class='industry'>.*</span>"
        tag = ParserHelper.match_first_pattern(TagParser.html, pattern)
        return ParserHelper.extract_tag_text(tag)

    #Gets the entry shares groups
    def shares_groups(self, TagParser):
        if TagParser.html.find("<div class='shared-groups'>") != -1:
            return 1
        else:
            return 0

    #Gets the entry shares connections
    def shares_connections(self, TagParser):
        if TagParser.html.find("<div class='shared-connections'") != -1:
            return 1
        else:
            return 0

class TagFactory:
    
    @staticmethod
    def get_tag_parser(html):
        
        if html.find("wvmx-anonymous-photo") != -1:
            return AnonTagParser(html)
        elif html.find("wvmx_profile_redherring") != -1:
            return SemiKnownTagParser(html)
        else:
            return IdentTagParser(html)