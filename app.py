from flask import Flask, jsonify
import requests

from dotenv import load_dotenv
load_dotenv()
import os
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TICKETMASTER_KEY = os.getenv("TICKETMASTER_KEY")


app = Flask(__name__)

# homepage route
@app.route('/')
def home():
  print("Hi console")
  return "Hello world!"

@app.route('/playlists/new', methods=['GET'])
def add_playlist():
  
  # ~~~~~ TICKETMASTER SEARCH ~~~~~
  tm_url = "https://app.ticketmaster.com/discovery/v2/events.json"
  tm_params = {
    "apikey": TICKETMASTER_KEY,
    "city": "Seattle",
    "segmentId": "KZFzniwnSyZfZ7v7nJ",
    "genreId": "KnvZfZ7vAev",
    "sort": "date,asc",
    "size": 50
  }
  r = requests.get(tm_url, params=tm_params)
  events_data = r.json()
  events_list = events_data["_embedded"]["events"]
  artist_names = []
  for event in events_list:
    if "attractions" in event["_embedded"] and "name" in event["_embedded"]["attractions"][0]:
      artist_names.append(event["_embedded"]["attractions"][0]["name"])

  data = {}
  data["artists"] = artist_names

  # ~~~~~ SPOTIFY ARTIST ID SEARCH ~~~~~
  spot_auth_token = AUTH_TOKEN
  spot_search_url = "https://api.spotify.com/v1/search"
  spot_headers = {
    "Authorization": "Bearer {spot_auth_token}".format(spot_auth_token = spot_auth_token)
  }
  spot_search_params = {
    "type": "artist",
    "limit": 1,
  }

  artist_ids = []
  for artist in artist_names:
    spot_search_params["q"] = artist
    artist_id_response = requests.get(spot_search_url, headers=spot_headers, params=spot_search_params)
    artist_id_response_data = artist_id_response.json()
    if artist_id_response_data["artists"]["total"] != 0:
      artist_ids.append(artist_id_response_data["artists"]["items"][0]["id"])

  # ~~~~~ SPOTIFY ARTIST TOP SONG SEARCH ~~~~~
  
  playlist_song_uris = []
  top_song_params = {
    "country": "from_token"
  }

  for artist_id in artist_ids:
    id = artist_id
    top_song_url = "https://api.spotify.com/v1/artists/{id}/top-tracks".format(id=id)
    top_song_response = requests.get(top_song_url, headers=spot_headers, params=top_song_params)
    top_song_response_data = top_song_response.json()
    top_song_uri = top_song_response_data["tracks"][0]["uri"]
    if top_song_uri not in playlist_song_uris:
      playlist_song_uris.append(top_song_uri)

  print(playlist_song_uris)

  # ~~~~~ SPOTIFY GET CURRENT USER'S ID ~~~~~

  spotify_user_url = "https://api.spotify.com/v1/me"
  user_response = requests.get(spotify_user_url, headers=spot_headers)
  user_response_data = user_response.json()
  user_id = user_response_data["id"]

  # ~~~~~ SPOTIFY PLAYLIST CREATION ~~~~~
  # Remember to save playlist url to return

  playlist_creation_headers = {
    "Authorization": "Bearer {spot_auth_token}".format(spot_auth_token = spot_auth_token)
    # "Content-Type": "application/json"
  }

  playlist_creation_json = {
    "name": "Env Playlist",
    "public": "false"
  }

  playlist_creation_url = "https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id = user_id)

  new_playlist_response = requests.post(playlist_creation_url, headers=playlist_creation_headers, json=playlist_creation_json)
  new_playlist_response_data = new_playlist_response.json()
  new_playlist_uri = new_playlist_response_data["uri"]
  new_playlist_id = new_playlist_response_data["id"]

  # ~~~~~ SPOTIFY ADD SONGS TO PLAYLIST ~~~~~

  add_songs_url = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(playlist_id = new_playlist_id)

  add_songs_json = {
    "uris": playlist_song_uris
  }
  add_songs_response = requests.post(add_songs_url, headers=spot_headers, json=add_songs_json)
  add_songs_response_headers = add_songs_response.headers

  print(add_songs_response_headers)

  data_to_return = {
    "playlist_uri": new_playlist_uri
  }

  return data_to_return


if __name__ == '__main__':
  app.run(port=5000)