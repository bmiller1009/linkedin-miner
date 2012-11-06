from entryrecord import EntryRecord
from globals import LINKEDIN_URL
from parserhelper import ParserHelper

(Anon, Semiknown, Known) = range(1,4)

#This class handles parsing logic for anonymous contacts
class AnonTagParser(object):
    
    def save(self):
        
        entry_record = EntryRecord()
        
        entry_record.entry_type_id = Anon
        entry_record.entry_name = 'Anonymous LinkedIn User'
        entry_record.semi_known_main_entry_id = 0
        
        return entry_record.save()

#This class handles parsing logic for semi-known contacts
class SemiKnownTagParser(object):

    def __init__(self, html):
        self.id = 0
        self.html = html
        self.entry_record = EntryRecord()
        self.REGEX = "<a href='/wvmx/profile/redherring?[^>]*>.*</a>"

    @property
    def main_entry_id(self):
        return self.entry_record.entry_id

    @property
    def semi_known_url(self):
        return self.entry_record.profile_url

    def save(self):
        
        self.entry_record.entry_type_id = Semiknown
        self.entry_record.entry_name = self.get_description()
        self.entry_record.profile_url = self.get_url()
        self.entry_record.semi_known_main_entry_id = 0

        self.id = self.entry_record.save()
        
        return self.id

    #Parses the semi-known description from a contact in the html list
    def get_description(self): 

        tag = ParserHelper.match_first_pattern(self.html, self.REGEX)
        return ParserHelper.extract_tag_text(tag)

    #Gets the semi known URL
    def get_url(self):

        tag = ParserHelper.match_first_pattern(self.html, self.REGEX)
    
        start_index = tag.index("href='/")
        title_index = tag.index("trk=")
        
        #TODO:  Clean this up
        return LINKEDIN_URL + \
            ParserHelper.clean_data(tag[start_index + 7:title_index])

#This class handles parsing logic for fully identified contacts
class IdentTagParser(object):

    def __init__(self, html):
        self.entry_record = EntryRecord()
        self.html = html
        self.semi_known_id = 0

    #Parses the tag
    def save(self):
        
        self.entry_record.entry_type_id = Known
        self.entry_record.entry_name = self.name()
        self.entry_record.profile_url = self.profile_url()
        self.entry_record.job_title = self.job_title().replace("'", "")
        self.entry_record.location = self.extract_metric("location").replace("'", "")
        self.entry_record.region = self.extract_metric("industry").replace("'", "")
        self.entry_record.semi_known_main_entry_id = self.semi_known_id
        self.entry_record.shares_groups = self.shares_groups()
        self.entry_record.shares_connections = self.shares_connections()

        return self.entry_record.save()

    #Gets the name of the entry
    def name(self):
        
        pattern = " title='View profile'>.*</a>"
        tag = ParserHelper.match_first_pattern(self.html, pattern)
        return ParserHelper.extract_tag_text(tag)

    #Gets the profile URL
    def profile_url(self):
        
        pattern = "<a href=(.*)/profile[^>]*>"
        url = "{0}profile/view?id=".format(LINKEDIN_URL)
        tag = ParserHelper.match_first_pattern(self.html, pattern)

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
    def job_title(self):
        
        pattern = "<dd class='title'>.*</dd>"
        tag = ParserHelper.match_first_pattern(self.html, pattern)
        return ParserHelper.extract_tag_text(tag)
    
    #Gets location and industry of contact
    def extract_metric(self, pattern_value):
        pattern = "<span class='{0}'>.*</span>".format(pattern_value)
        tag = ParserHelper.match_first_pattern(self.html, pattern)
        return ParserHelper.extract_tag_text(tag)
    
    #Gets the entry shares groups
    def shares_groups(self):
        if self.html.find("<div class='shared-groups'>") != -1:
            return 1
        else:
            return 0

    #Gets the entry shares connections
    def shares_connections(self):
        if self.html.find("<div class='shared-connections'") != -1:
            return 1
        else:
            return 0

class TagFactory:
    
    @staticmethod
    def get_tag_parser(html):
        
        if html.find("wvmx-anonymous-photo") != -1:
            return AnonTagParser()
        elif html.find("wvmx_profile_redherring") != -1:
            return SemiKnownTagParser(html)
        else:
            return IdentTagParser(html)