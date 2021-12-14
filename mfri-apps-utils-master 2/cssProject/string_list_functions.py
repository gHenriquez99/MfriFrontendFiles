import re

#string functions

CHARS_WE_CAN_TRANSLATE = {
                            u'\u0009':" " + " " + " " + " " + " ",  
                            u'\u0060':"'", 
                            u'\u2013':'-', 
                            u'\u2014':'-',
                            u'\u2018':"'",
                            u'\u2019':"'",
                            u'\u201A':"'",
                            u'\u201c':'"',
                            u'\u201d':'"',
                            u'\u201E':'"',
                            u'\u2022':'*',
                            u'\u2026':'...',
                            u'\u2028':'',
                            u'\u02C6':'^',
                            u'\u2039':'<',
                            u'\u203A':'>',
                            u'\u2122':'TM',
                            u'\u2264':'<=',
                            u'\u2265':'>=',
                            u'\u02DC':'~',
                            u'\u00A0':' ',
                            u'\u00AB':'<<',
                            u'\u00A9':'(C)',
                            u'\u00AE':'(R)',
                            u'\u00B0':'Deg.',
                            u'\u00B7':'-',
                            u'\u00BC':'1/4',
                            u'\u00BD':'1/2',
                            u'\u00BE':'3/4',
                         }

def RemoveMSWordSpecialChars(string_to_fix=None):

    if not string_to_fix:
        return string_to_fix

    new_string_list = []
    if not re.compile(EXPANDED_STR_VALID_CHAR_RULE).search(string_to_fix): #20190212
        for char in string_to_fix:
            if not re.compile(EXPANDED_STR_VALID_CHAR_RULE).search(char): #20190212
                new_char = CHARS_WE_CAN_TRANSLATE.get(char, char)
                new_string_list.append(new_char)
            else: 
                new_string_list.append(char)

    if len(new_string_list) == 0:
        return string_to_fix
        
    return ''.join(new_string_list)

###
#list functions

def ListifyString(target_string=None, possible_invalid_separators=[';'], legal_separator=',', strip_white_space=True, white_space_to_strip=r'\s+'):

    if not target_string:
        return None

    if type(target_string) is list:
        return target_string

    if not white_space_to_strip:
        white_space_to_strip = r'\s+'

    if strip_white_space:
        target_string = re.sub(white_space_to_strip, '', target_string)
    
    for bogus_separator in possible_invalid_separators:
        target_string = target_string.replace(bogus_separator, legal_separator)
        
    new_list = target_string.split(legal_separator) 
    
    #assert False
    return new_list






