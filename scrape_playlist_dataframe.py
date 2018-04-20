#Imports here for writefile magic only. Not Pythonic.
import pandas as pd
import spotipy
import spotipy.util as util

#Max number per request:
#Artists: 50, Albums: 20, TracksFromPlaylist: 100, Features: 100.

#For now, limiting number of tracks per request to the minimum (20).
#Could reduce from ~6000*4/20=1200 requests to ~6000*2/100 + 6000/50 + 6000/20 
#= 120+120+300=540 requests.
#So roughly half the number of requests, but current code is cleaner.

#explain what im doing here in markdown. that i need to pull tracks, but need 
#to also pull other stuff manually since the track info is simplified, and that
#i need to unpack the dictionaries into columns.

def scrape_playlist_raw(sp, username, playlist_id):
    
    #Scrape tracks
    results = sp.user_playlist_tracks(username, playlist_id, limit=20) 
    
    tracks = [ x['track'] for x in results['items'] ]
    
    results_ids = [ x['id'] for x in tracks ]
    features = sp.audio_features( results_ids )
    
    #This only pulls first artist id per track for now.
    results_ids_artist = [ x['artists'][0]['id'] for x in tracks ] 
    artists = sp.artists( results_ids_artist )['artists']
    results_ids_album = [ x['album']['id'] for x in tracks ]
    albums = sp.albums( results_ids_album )['albums']
    
    while results['next']:
        
        results = sp.next(results)
        
        results_tracks = [ x['track'] for x in results['items'] ]
        results_ids = [ x['id'] for x in results_tracks ]
        results_features = sp.audio_features( results_ids )
        results_ids_artist = [ x['artists'][0]['id'] for x in results_tracks ]
        results_artists = sp.artists( results_ids_artist )['artists']
        results_ids_album = [ x['album']['id'] for x in results_tracks ]
        results_albums = sp.albums( results_ids_album )['albums']
        
        tracks.extend( results_tracks )
        features.extend( results_features )
        artists.extend( results_artists )
        albums.extend( results_albums )
    
    return tracks, features, artists, albums


def tracks_dataframe(tracks):
    #Construct tracks dataframe
    df_tracks = pd.DataFrame(tracks)

    #Drop unwanted columns
    cols = ['album', 'artists', 'duration_ms', 'external_ids', 'external_urls',
            'href', 'type', 'uri'] 
    df_tracks.drop(cols, axis=1, inplace=True)
    
    return df_tracks


def features_dataframe(features, ids):
    
    """
    ids need to be specified in order to fill the 'id' field in missing dicts
    """
    
    #Fill missing feature dicts
    #This uses the first dictionary in the list as a template
    #*Assumes first dictionary isn't missing.*
    none_dict = { key:None for key in features[0] }
    for i,x in enumerate(features):
        if x is None:
            none_dict['id'] = ids[i]
            features[i] = none_dict
    
    #Construct features dataframe    
    df_features = pd.DataFrame(features)

    #Convert duration from milliseconds to minutes
    df_features['duration_mins'] = df_features['duration_ms']/60000
    
    #Drop unwanted columns
    cols = ['id', 'analysis_url', 'track_href', 'type', 'uri', 'duration_ms']
    df_features.drop(cols, axis=1, inplace=True)
    
    return df_features
    
def artists_dataframe(artists):
    #Construct tracks dataframe
    df_artists = pd.DataFrame(artists)
    
    #Pull total number of followers from 'followers' dictionary
    df_artists['num_followers'] = df_artists['followers'].transform( 
        lambda x: x['total'] )
    
    #Capitalize genre names
    def strings_to_titles(list_of_strings):
        return [string.title() for string in list_of_strings]
    df_artists['genres'] = df_artists.genres.transform( 
        lambda x: strings_to_titles(x) )
    
    #Drop unwanted columns
    cols = ['num_followers','genres','images','name','popularity','id']
    df_artists = df_artists[cols]
    
    return df_artists

def albums_dataframe(albums):
    #Construct tracks dataframe
    df_albums = pd.DataFrame(albums)
    
    #Construct integer release year column
    df_albums['release_year'] = df_albums.release_date.str[0:4].astype('int')
    
    #Float month/day columns. To allow for missing (NaN) info
    df_albums['release_month'] = pd.to_numeric( 
        df_albums.release_date.str[5:7], errors='coerce')
    df_albums['release_day'] = pd.to_numeric( 
        df_albums.release_date.str[8:10], errors='coerce')
    
    #Drop unwanted columns
    cols = ['album_type', 'images', 'label', 'name', 'popularity', 
            'release_year', 'release_month', 'release_day']
    df_albums = df_albums[cols]
    
    return df_albums
    
def scrape_playlist_dataframe(sp, username, playlist_id):
    
    #Scrape tracks, features, artists, albums as lists, derive ids
    tracks, features, artists, albums = scrape_playlist_raw(sp, username, 
                                                            playlist_id)
    ids = [ x['id'] for x in tracks ]
    
    #Build tracks and features dataframes
    df_tracks = tracks_dataframe(tracks)
    df_features = features_dataframe(features, ids)
    df_artists = artists_dataframe(artists)
    df_albums = albums_dataframe(albums)
    
    #Join into one dataframe
    df = df_tracks.join(df_features).join(df_artists, rsuffix='_artist').join(
        df_albums, rsuffix='_album')
    
    #Consider separating out images dataframe, perhaps use a flag argument
    
    return df