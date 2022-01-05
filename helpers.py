import os
import requests
import urllib.parse

from flask import redirect, session
from functools import wraps

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/welcome")
        return f(*args, **kwargs)
    return decorated_function


def search_song(song):
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        results = sp.search(q='track:' + song, type='track', market='IE', limit='20')
        items = results['tracks']['items']
        limit = results['tracks']['limit']
        total = results['tracks']['total']
        albums = []
        arts = []
        artists = []
        names = []
        ids = []
        amount = min(limit, total)

        for i in range(amount):

            album = items[i]['album']['name']
            art = items[i]['album']['images'][0]['url']
            artist = items[i]['artists'][0]['name']
            name = items[i]['name']
            id = items[i]['id']

            albums.append(album)
            arts.append(art)
            artists.append(artist)
            names.append(name)
            ids.append(id)

        info = [albums,arts,artists,names,ids]

        return info

    except requests.RequestException:
        return None

def search_song_by_id(song_id):
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        song_id = (song_id.strip())
        track = sp.track(track_id=song_id, market='IE')

        album = track['album']['name']
        art = track['album']['images'][0]['url']
        artist = track['artists'][0]['name']
        name = track['name']

        info = {
        "album":album,
        "art":art,
        "artist":artist,
        "name":name
        }
        
        return info

    except:
        return None
