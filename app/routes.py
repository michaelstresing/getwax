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
REDIRECT_URI = f"{CLIENT_SIDE_URL}:{PORT}/login/authorized"
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
    print(auth_query_parameters)
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    print(url_args)
    return redirect(auth_url)

@app.route("/login/authorized")
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
    # print(post_request)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    authorization_header = {"Authorization": f"Bearer {access_token}"}

    # Get profile data
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get library data
    user_library_api_endpoint = f"{SPOTIFY_API_URL}/me/tracks"
    library_response = requests.get(user_library_api_endpoint, headers=authorization_header)
    library_data = json.loads(library_response.text)
    
    return authorization_header

@app.route("/profile")
def profile():
    response_data = json.loads(requests.get(f"{CLIENT_SIDE_URL}:{PORT}/login/authorized"))

    # Use the access token to access Spotify API
    authorization_header = {"Authorization": f"Bearer {access_token}"}

    print(callback)
    print("HELLO")

    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    return profile_data