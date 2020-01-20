from flask import Flask, jsonify, request
import requests

from dotenv import load_dotenv
load_dotenv()
import os

TICKETMASTER_KEY = os.getenv("TICKETMASTER_KEY")
SPOT_CLIENT_ID = os.getenv("SPOT_CLIENT_ID")
SPOT_CLIENT_SECRET = os.getenv("SPOT_CLIENT_SECRET")
CRYPT_KEY = os.getenv("CRYPT_KEY")

from cryptography.fernet import Fernet
key_byte = CRYPT_KEY.encode("utf-8")
fern = Fernet(key_byte)

app = Flask(__name__)

# homepage route
@app.route('/')
def home():
  print("Bye console")

  # key = Fernet.generate_key()
  # key_string = key.decode("utf-8")
  
  # m = Fernet(key_byte)
  test_string = "Hello it's me"
  test_token = fern.encrypt(bytes(test_string, encoding='utf-8'))
  test_token_encrypted_string = test_token.decode("utf-8")
  test_token_byte = test_token_encrypted_string.encode("utf-8")
  # test_token_2 = m.encrypt(b"Second token test")
  
  # print("Key string coming:")
  # print(key_string)
  print(test_token)
  print(test_token_byte)
  print(test_token_encrypted_string)
  print(fern.decrypt(test_token).decode("utf-8"))
  print(fern.decrypt(test_token_byte).decode("utf-8"))
  # print(test_token_2)
  # print(m.decrypt(test_token_2).decode("utf-8"))

  return "Hello world!"

@app.route('/api/token', methods=['POST'])
def swap_token():
  code = request.form["code"]

  redirect_uri = "up-next-quick-start://spotify-login-callback"
  get_token_url = "https://accounts.spotify.com/api/token"
  get_token_body = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri,
    'client_id': SPOT_CLIENT_ID,
    'client_secret': SPOT_CLIENT_SECRET
  }
  get_token_response = requests.post(get_token_url, data=get_token_body)
  
  get_token_response_data = get_token_response.json()
  access_token = get_token_response_data["access_token"]
  refresh_token = get_token_response_data["refresh_token"]
  expires_in = get_token_response_data["expires_in"]

  refresh_token_encrypted = fern.encrypt(bytes(refresh_token, encoding='utf-8'))
  refresh_token_encrypted_string = refresh_token_encrypted.decode("utf-8")

  token_swap_response_body = {
    "access_token": access_token,
    "expires_in": expires_in,
    "refresh_token": refresh_token_encrypted_string
  }

  return(jsonify(token_swap_response_body))

@app.route('/api/refresh_token', methods=['POST'])
def refresh_token():
  passed_refresh_token_string = request.form["refresh_token"]
  print(passed_refresh_token_string)
  passed_refresh_token_byte = passed_refresh_token_string.encode("utf-8")
  decrypted_refresh_token = fern.decrypt(passed_refresh_token_byte).decode("utf-8")

  refresh_token_url = "https://accounts.spotify.com/api/token"
  refresh_token_body = {
    'grant_type': 'refresh_token',
    'refresh_token': decrypted_refresh_token,
    'client_id': SPOT_CLIENT_ID,
    'client_secret': SPOT_CLIENT_SECRET
  }

  refresh_token_response = requests.post(refresh_token_url, data=refresh_token_body)
  refresh_token_response_data = refresh_token_response.json()
  print(refresh_token_response_data)
  access_token = refresh_token_response_data["access_token"]
  expires_in = refresh_token_response_data["expires_in"]
  if "refresh_token" in refresh_token_response_data:
    refresh_token = refresh_token_response_data["refresh_token"]
  else:
    refresh_token = decrypted_refresh_token

  refresh_token_encrypted = fern.encrypt(bytes(refresh_token, encoding='utf-8'))
  refresh_token_encrypted_string = refresh_token_encrypted.decode("utf-8")

  refresh_token_response_body = {
    "access_token": access_token,
    "expires_in": expires_in,
    "refresh_token": refresh_token_encrypted_string
  }

  return(jsonify(refresh_token_response_body))
  
@app.route('/playlists/new', methods=['POST'])
def add_playlist():

  # ~~~~~ USER INPUT ~~~~~
  input_city = request.args.get("city")
  input_access_token = request.args.get("accessToken")
  input_playlist_name = request.args.get("playlistName")
  input_genre_id = request.args.get("genreId")

  # ~~~~~ FAILED RESPONSE TEMPLATE ~~~~~
  failed_response = {
    "events_found": "false",
    "playlist_uri": "",
    "playlist_url": ""
  }
  
  # ~~~~~ TICKETMASTER SEARCH ~~~~~
  tm_url = "https://app.ticketmaster.com/discovery/v2/events.json"
  tm_params = {
    "apikey": TICKETMASTER_KEY,
    "city": input_city,
    "segmentId": "KZFzniwnSyZfZ7v7nJ",
    "genreId": input_genre_id,
    "sort": "date,asc",
    "size": 50
  }
  r = requests.get(tm_url, params=tm_params)
  events_data = r.json()
  if "_embedded" not in events_data or "events" not in events_data["_embedded"]:
    # failed_response = {
    #   "events_found": "false",
    #   "playlist_uri": "",
    #   "playlist_url": ""
    # }
    return jsonify(failed_response)

  events_list = events_data["_embedded"]["events"]
  artist_names = []
  for event in events_list:
    if "attractions" in event["_embedded"] and "name" in event["_embedded"]["attractions"][0]:
      artist_names.append(event["_embedded"]["attractions"][0]["name"])

  # data = {}
  # data["artists"] = artist_names

  # ~~~~~ SPOTIFY ARTIST ID SEARCH ~~~~~
  spot_auth_token = input_access_token
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
    print(artist_id_response)
    artist_id_response_data = artist_id_response.json()
    print(artist_id_response.json())
    if artist_id_response_data["artists"]["total"] != 0:
      artist_ids.append(artist_id_response_data["artists"]["items"][0]["id"])

  # ~~~~~ SPOTIFY ARTIST TOP SONG SEARCH ~~~~~
  
  playlist_song_uris = []
  top_song_params = {
    "country": "from_token"
  }

  if len(artist_ids) == 0:
    # failed_response = {
    #   "events_found": "false",
    #   "playlist_uri": "",
    #   "playlist_url": ""
    # }
    return jsonify(failed_response)

  for artist_id in artist_ids:
    id = artist_id
    top_song_url = "https://api.spotify.com/v1/artists/{id}/top-tracks".format(id=id)
    top_song_response = requests.get(top_song_url, headers=spot_headers, params=top_song_params)
    top_song_response_data = top_song_response.json()

    if "tracks" in top_song_response_data and len(top_song_response_data["tracks"]) != 0: 
      top_song_uri = top_song_response_data["tracks"][0]["uri"]
      if top_song_uri not in playlist_song_uris:
        playlist_song_uris.append(top_song_uri)

  print(playlist_song_uris)

  if len(playlist_song_uris) == 0:
    # failed_response = {
    #   "events_found": "false",
    #   "playlist_uri": "",
    #   "playlist_url": ""
    # }
    return jsonify(failed_response)

  # ~~~~~ SPOTIFY GET CURRENT USER'S ID ~~~~~

  spotify_user_url = "https://api.spotify.com/v1/me"
  user_response = requests.get(spotify_user_url, headers=spot_headers)
  user_response_data = user_response.json()
  if "id" in user_response_data:
    user_id = user_response_data["id"]
  else:
    return jsonify(failed_response)

  # ~~~~~ SPOTIFY PLAYLIST CREATION ~~~~~

  playlist_creation_headers = {
    "Authorization": "Bearer {spot_auth_token}".format(spot_auth_token = spot_auth_token)
    # "Content-Type": "application/json"
  }

  playlist_creation_json = {
    "name": input_playlist_name,
    "public": "false"
  }

  playlist_creation_url = "https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id = user_id)

  new_playlist_response = requests.post(playlist_creation_url, headers=playlist_creation_headers, json=playlist_creation_json)
  new_playlist_response_data = new_playlist_response.json()
  if "uri" in new_playlist_response_data and "id" in new_playlist_response_data and "external_urls" in new_playlist_response_data and "spotify" in new_playlist_response_data["external_urls"]:
    new_playlist_uri = new_playlist_response_data["uri"]
    new_playlist_id = new_playlist_response_data["id"]
    new_playlist_url = new_playlist_response_data["external_urls"]["spotify"]
  else:
    return jsonify(failed_response)

  # ~~~~~ SPOTIFY ADD SONGS TO PLAYLIST ~~~~~

  add_songs_url = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(playlist_id = new_playlist_id)

  add_songs_json = {
    "uris": playlist_song_uris
  }
  add_songs_response = requests.post(add_songs_url, headers=spot_headers, json=add_songs_json)
  # add_songs_response_headers = add_songs_response.headers

  # print(add_songs_response_headers)
  print(add_songs_response.status_code)

  data_to_return = {
    "events_found": "true",
    "playlist_uri": new_playlist_uri,
    "playlist_url": new_playlist_url
  }

  if add_songs_response.status_code == 201:
    return jsonify(data_to_return)
  else:
    return jsonify(failed_response)


if __name__ == '__main__':
  app.run(port=5000)