import re

#Utility class for matching and parsing HTML strings using regular expressions
class ParserHelper:
    
    @staticmethod
    #Returns the first match of a regular expression
    def match_first_pattern(html, pattern):

        r = re.search(pattern, html)

        if r:
            return html[r.start():r.end()]
        else:
            return ''

    @staticmethod
    #Gets the text between tags.
    def extract_tag_text(tag):
            
        start_tag_idx = tag.index('>')
        str_len = tag[start_tag_idx + 1:].index('<')

        tag_text = ''.join(c for c in tag[start_tag_idx + 1:start_tag_idx + str_len + 1])
        
        return ParserHelper.clean_data(tag_text)
    
    @staticmethod
    #Loops through all of the contacts found in the requested html text
    def get_contacts(html, pattern):
        
        html = html.replace("\"","'")
        match_strings = []
        
        for match in re.finditer(pattern, html):
            match_strings.append(html[match.start():match.end()])
        
        return match_strings
    
    @staticmethod
    def clean_data(data):
        data = data.strip()
        data = data.replace("amp;", '')
    
        return data