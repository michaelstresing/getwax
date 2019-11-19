from flask_oauthlib.client import OAuth, OAuthException
from flask import Flask, redirect, url_for, session, request, render_template, flash, redirect
from flask import current_app as app, request
# from . import oath_client
from urllib.parse import quote

# oauth = OAuth(app)
# spotify = oauth.remote_app( "spotify",
#                             consumer_key=app.config['CLIENT_ID'],
#                             consumer_secret=app.config['CLIENT_SECRET'],
#                             request_token_params={'scope': 'user-read-email'},
#                             base_url='https://accounts.spotify.com',
#                             request_token_url=None,
#                             access_token_url='/api/token',
#                             authorize_url='https://accounts.spotify.com/authorize'
#                             )
# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
# Server-side Parameters
CLIENT_SIDE_URL = "https://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/login/authorized".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": app.config['REDIRECT_URI'],
    "scope": SCOPE,
    "state": STATE,
    "show_dialog": SHOW_DIALOG_str,
    "client_id": app.config['CLIENT_ID']
}

@app.route('/')
def index():
    url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/login/authorized")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    print(profile_data)

# @app.route('/login')
# def login():

#     if spotify.authorize:ç
#         del spotify

#     callback = url_for(
#         'spotify_authorized',
#         next=request.args.get('next') or request.referrer or None,
#         _external=True
#     )
#     return spotify.authorize(callback=callback)

# @app.route('/login/authorized')
# def spotify_authorized():
#     resp = spotify.authorized_response()
#     print(resp)
#     if resp is None:
#         return f"Access denied: reason={request.args['error_reason']} error={request.args['error_description']}"

#     if isinstance(resp, OAuthException):
#         return f"Access denied: {resp.message}"

#     session['oauth_token'] = (resp['access_token'], '')
#     me = spotify.get('/me')
#     return f"{resp}"

# @spotify.tokengetter
# def get_spotify_oauth_token():
#     return session.get('oauth_token')