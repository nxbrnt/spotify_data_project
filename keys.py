#Replace with valid values for Spotify API, 
#or create and populate secret_keys.py
client_id = ''
secret = ''
redirect_uri = ''

try:
    from secret_keys import *
except Exception:
    pass