import re

#Utility class for matching and parsing HTML strings using regular expressions
class ParserHelper:
    
    @staticmethod
    #Returns the first match of a regular expression
    def regex_return_first_match(html, pattern):
        
        r = re.search(pattern, html)

        if r:
            return html[r.start():r.end()]
        else:
            return ''

    @staticmethod
    #Gets the text between tags.
    def get_text_between_tags(tag):

        clean_tag = ParserHelper.clean_data(tag)
        start_tag = clean_tag.index('>')
        final_string = ''

        for c in clean_tag[start_tag + 1:]:
            if c == '<':
                break

            final_string += c

        return ParserHelper.clean_data(final_string)
    
    @staticmethod
    #Removes unwanted characters from the html string
    def clean_data(data):
        data = data.strip()
        data = data.replace("amp;", '')

        return data
