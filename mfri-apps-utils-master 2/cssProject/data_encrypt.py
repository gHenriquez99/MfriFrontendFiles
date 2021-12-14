#import random
#import json
#import base64
#import time
#import datetime
from cryptography.fernet import Fernet

from mfri.utils.data_encode import decode_context, encode_context
from mfri.utils.json_functions import serialize_json_data_to_string, deserialize_json_data_from_string

def CreateEncryptKey():

    Encrypt_Key = b'GkXH85gvHxRG7zMrpWvPBHQJSlNxcILTN4Gc5cmSV48=' #for development and testing only #Fernet.generate_key()
    #Encrypt_Key = Fernet.generate_key()
    return Encrypt_Key

def EncryptContext(context_data=None, encryption_key=None, encode_data_before=True):
    
    if not context_data:
        return None

    if not encryption_key:
        return None
        #encryption_key = EncryptKey()

    if encode_data_before:
        context_data = str.encode(encode_context(context_data=context_data))
    else:
        context_data = serialize_json_data_to_string(json_data=context_data)

    error_message = None
    try:
        encryptor = Fernet(encryption_key)
        encrypted_context = encryptor.encrypt( context_data)
    except Exception as e:
        #return None
        error_message = e
    
    if error_message:
        assert False
        
    encrypted_context_string = encrypted_context.decode("utf-8") 
    return encrypted_context_string

def DecryptContext(encrypted_context=None, encryption_key=None, decode_data_after=True):
    
    if not encrypted_context:
        assert False
        return None

    if not encryption_key:
        assert False
        return None
        #encryption_key = EncryptKey()

    encrypted_context = bytes(encrypted_context, 'utf-8')

    error_message = None
    try:
        decryptor = Fernet(encryption_key)
        deecrypted_context = decryptor.decrypt(encrypted_context)
    except Exception as e:
        #return None
        error_message = e

    if error_message:
        assert False

    if decode_data_after:
        decoded_data = decode_context(raw_context=deecrypted_context)
        
        #if isinstance(decoded_data,str):
        #    decoded_data_string = destring_json_data(string_data=decoded_data)
            #assert False
        #assert False

        return decoded_data
    else:
        #assert False
        if isinstance(decoded_data,str):
            decoded_data = deserialize_json_data_from_string(string_data=deecrypted_context)
        return decoded_data

    return deecrypted_context





















