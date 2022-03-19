import os
import hashlib
import requests
from authlib.jose import jwt

SSO_SECRET = os.getenv('SSO_SECRET')

def getUserDetails(token):
    """
    This function takes a JWT from Core and authenticates the user
    """
    decoded_token = jwt.decode(token, SSO_SECRET)
    post_url = decoded_token['post_url']
    # Key to get user details
    key = f'{SSO_SECRET}{token}'
    encoded_key = hashlib.sha512(key.encode('utf-8')).hexdigest()
    # API request header
    header = {
        'Content-Type':'application/json',
        'Accept':'*/*',
        "Accept-Encoding":'gzip, deflate, br',
        'Connection':'keep-alive',
        "User-Agent":"",
    }
    # API Request parameters
    data = {
        "key":encoded_key,
        "jwt":token
    }
    # API Request
    user_details = requests.post(post_url, headers=header, json=data).json()
    return user_details