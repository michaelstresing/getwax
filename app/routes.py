from flask_oauthlib.client import OAuth, OAuthException
from flask import Flask, redirect, url_for, session, request, render_template, flash, redirect, g
from flask import current_app as app
from urllib.parse import quote
import json
import requests

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = f"{CLIENT_SIDE_URL}:{PORT}/callback"
SCOPE = "user-read-email playlist-read-private user-follow-read user-library-read user-top-read playlist-modify-private playlist-modify-public"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "state": STATE,
    "show_dialog": SHOW_DIALOG_str,
    "client_id": app.config['CLIENT_ID']
}
@app.route('/')
def index():

    return render_template("index.html")

@app.route('/auth')
def auth():
    print(auth_query_parameters)
    url_args = "&".join([f"{key}={quote(val)}" for key, val in auth_query_parameters.items()])
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    
    # Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
    }

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    authorization_header = {"Authorization": f"Bearer {access_token}"}
    
    # store the access token in the session 
    session['access_token'] = access_token

    return redirect('/')

@app.route("/profile")
def profile():

    # Use the access token to access Spotify API
    at = session["access_token"]
    authorization_header = {"Authorization": f"Bearer {at}"}

    # Access the Spotify API
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data_raw = json.loads(profile_response.text)

    # Format and trim output
    profile_data = {
        "name": profile_data_raw["display_name"],
        "email": profile_data_raw["email"],
        "picture": profile_data_raw["images"][0]["url"]
    }

    return profile_data

@app.route("/library")
def library():

    # Use the access token to access Spotify API
    at = session["access_token"]
    authorization_header = {"Authorization": f"Bearer {at}"}

    # Get library data
    user_library_api_endpoint = f"{SPOTIFY_API_URL}/me/tracks"
    library_response = requests.get(user_library_api_endpoint, headers=authorization_header)
    library_data_raw = json.loads(library_response.text)

    # Format and trim output
    library_data = {
        "items": [],
        "itemcount": 0
    }

    for item in library_data_raw["items"]:

        id = {}
        id["artist"] = item["track"]["album"]["artists"][0]["name"]
        id["album"] = item["track"]["album"]["name"]
        id["song"] = item["track"]["name"]
        id["image"] = item["track"]["album"]["images"][0]["url"]

        library_data["items"].append(id)
        library_data["itemcount"] += 1

    return library_data