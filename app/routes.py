from flask_oauthlib.client import OAuth, OAuthException
from flask import Flask, redirect, url_for, session, request, render_template, flash, redirect
from flask import current_app as app, request
from . import oath_client

oauth = OAuth(app)
spotify = oauth.remote_app( "spotify",
                            consumer_key=app.config['CLIENT_ID'],
                            consumer_secret=app.config['CLIENT_SECRET'],
                            request_token_params={'scope': 'user-read-email'},
                            base_url='https://accounts.spotify.com',
                            request_token_url=None,
                            access_token_url='/api/token',
                            authorize_url='https://accounts.spotify.com/authorize'
                            )

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": app.config['REDIRECT_IR'],
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": app.config['CLIENT_ID']
}

@app.route('/')
def index():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route('/login')
def login():

    if spotify.authorize:
        del spotify

    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)

@app.route('/login/authorized')
def spotify_authorized():
    resp = spotify.authorized_response()
    print(resp)
    if resp is None:
        return f"Access denied: reason={request.args['error_reason']} error={request.args['error_description']}"

    if isinstance(resp, OAuthException):
        return f"Access denied: {resp.message}"

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/me')
    return f"{resp}"

@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')