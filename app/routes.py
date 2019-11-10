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

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    # if session['oauth_token']:
    #     del session['oauth_token']

    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)

@app.route('/login/authorized')
def spotify_authorized():
    resp = spotify.authorized_response()
    if resp is None:
        return f"Access denied: reason={request.args['error_reason']} error={request.args['error_description']}"

    if isinstance(resp, OAuthException):
        return f"Access denied: {resp.message}"

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/v1/me')
    # return f"{me}"
    return f"Logged in as id={me.data['email']} name={me.data['display_name']} redirect={request.args.get['next']}"

@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')