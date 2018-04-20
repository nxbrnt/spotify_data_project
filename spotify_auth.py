#Imports here for writefile magic only. Not Pythonic.
import pandas as pd
import spotipy
import spotipy.util as util

def spotify_auth( auth_dict ):
    
    """Obtain a Spotify authorization token"""
    
    client_id = auth_dict['client_id']
    secret = auth_dict['secret']
    redirect_uri = auth_dict['redirect_uri']
    scope = auth_dict['scope']
    username = auth_dict['username']

    #If Chrome doesn't redirect, find redirect url using 
    #Chrome Developer Tools (Details TBA)
    token = util.prompt_for_user_token(username, scope,client_id, secret, 
                                       redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        print('Successfully received auth token.')
    else:
        print('Cannot get token for' + username + '.')
        return
    
    return sp