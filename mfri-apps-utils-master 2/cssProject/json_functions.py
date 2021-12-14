#import random
import json
#import base64
#import time
#import datetime

def serialize_json_data_to_string(json_data=None):

    if not json_data:
        return None

    try:
        json_string = json.dumps(json_data).encode("utf-8")
    except:
        return None

    return json_string

def deserialize_json_data_from_string(string_data=None):

    if not string_data:
        return None

    try:
        json_data = json.loads(string_data)
    #except ValueError:
    except Exception as e:
        return None
        #return u'Nerb %s %s' % (string_date_type, e)
    #bob = str(string_data)
    #decoded_string_data = string_data.decode('UTF-8')
    #bob_again_type = type(bob_again)
    #first_element_of_bob_again = bob_again[0]

    #json_data = json.loads(string_data)
    #first_element_of_json_data = json_data[0]
    #json_data_type = type(json_data)
    #assert False
    #json_data = json.loads(string_data)
    #json_data_type_1 = type(json_data)
    #string_data_2 = ''.join(json_data)
    #string_data_type_2 = type(json_data)
    #assert False

    return json_data





















