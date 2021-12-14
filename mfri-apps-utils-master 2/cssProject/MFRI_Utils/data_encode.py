#import random
#import json
import base64
#import time
#import datetime

from MFRI_Utils.json_functions import serialize_json_data_to_string, deserialize_json_data_from_string

def decode_context(raw_context=None):

    if not raw_context:
        return None

    try:
        context_decoded = base64.urlsafe_b64decode(raw_context + '='.encode("utf-8") * (4 - len(raw_context) % 4))
    except:
        return None

    context_decoded_dict = deserialize_json_data_from_string(string_data=context_decoded)
    
    if not context_decoded_dict:
        return None

    if type(context_decoded_dict) != dict:
        return context_decoded_dict

    for context_key in context_decoded_dict.keys():
        
        if type(context_decoded_dict[context_key]) == str: 
            context_decoded_dict[context_key] = context_decoded_dict[context_key].strip()

    return context_decoded_dict

def encode_context(context_data=None):
    
    if not context_data:
        return None

    context_json = serialize_json_data_to_string(json_data=context_data)
    if not context_json:
        return None
        
    try:
        context_base64 = base64.urlsafe_b64encode(context_json).decode('utf-8').strip('=')
    except:
        return None

    return context_base64





















