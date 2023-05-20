from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from config import Config as SETTING

cid = SETTING.SPOTIFY_CLIENT_ID
secret = SETTING.SPOTIFY_CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = Spotify(client_credentials_manager=client_credentials_manager)