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

    except Exception as e:
        return None

    return json_data





















