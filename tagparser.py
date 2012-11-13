from entryrecord import EntryRecord
from globals import LINKEDIN_URL
from parserhelper import ParserHelper as ph

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
        self._id = 0
        self._html = html
        self._entry_record = EntryRecord()
        self._REGEX = "<a href='/wvmx/profile/redherring?[^>]*>.*</a>"

    @property
    def main_entry_id(self):
        return self._entry_record.entry_id

    @property
    def semi_known_url(self):
        return self._entry_record.profile_url

    def save(self):
        
        self._entry_record.entry_type_id = Semiknown
        self._entry_record.entry_name = self._get_description()
        self._entry_record.profile_url = self._get_url()
        self._entry_record.semi_known_main_entry_id = 0

        self.id = self._entry_record.save()
        
        return self.id

    #Parses the semi-known description from a contact in the html list
    def _get_description(self): 

        tag = ph.match_first_pattern(self._html, self._REGEX)
        return ph.extract_tag_text(tag)

    #Gets the semi known URL
    def _get_url(self):

        tag = ph.match_first_pattern(self._html, self._REGEX)
    
        start_index = tag.index("href='/")
        title_index = tag.index("trk=")
        
        #TODO:  Clean this up
        return LINKEDIN_URL + \
            ph.clean_data(tag[start_index + 7:title_index])

#This class handles parsing logic for fully identified contacts
class IdentTagParser(object):

    def __init__(self, html):
        self._entry_record = EntryRecord()
        self._html = html
        self._semi_known_id = 0

    #Parses the tag
    def save(self):
        
        self._entry_record.entry_type_id = Known
        self._entry_record.entry_name = self._name()
        self._entry_record.profile_url = self._profile_url()
        self._entry_record.job_title = self._job_title().replace("'", "")
        self._entry_record.location = self._extract_metric("location").replace("'", "")
        self._entry_record.region = self._extract_metric("industry").replace("'", "")
        self._entry_record.semi_known_main_entry_id = self._semi_known_id
        self._entry_record.shares_groups = self._shares_groups()
        self._entry_record.shares_connections = self._shares_connections()

        return self._entry_record.save()

    #Gets the name of the entry
    def _name(self):
        
        pattern = " title='View profile'>.*</a>"
        tag = ph.match_first_pattern(self._html, pattern)
        return ph.extract_tag_text(tag)

    #Gets the profile URL
    def _profile_url(self):
        
        pattern = "<a href=(.*)/profile[^>]*>"
        url = "{0}profile/view?id=".format(LINKEDIN_URL)
        tag = ph.match_first_pattern(self._html, pattern)

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
        
        return url + ph.clean_data(tag[start_index:title_index])
        
    #Gets the entry job title
    def _job_title(self):
        
        pattern = "<dd class='title'>.*</dd>"
        tag = ph.match_first_pattern(self._html, pattern)
        return ph.extract_tag_text(tag)
    
    #Gets location and industry of contact
    def _extract_metric(self, pattern_value):
        pattern = "<span class='{0}'>.*</span>".format(pattern_value)
        tag = ph.match_first_pattern(self._html, pattern)
        return ph.extract_tag_text(tag)
    
    #Gets the entry shares groups
    def _shares_groups(self):
        if self._html.find("<div class='shared-groups'>") != -1:
            return 1
        else:
            return 0

    #Gets the entry shares connections
    def _shares_connections(self):
        if self._html.find("<div class='shared-connections'") != -1:
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