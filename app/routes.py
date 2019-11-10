from flask_oauthlib.client import OAuth, OAuthException
from flask import Flask, redirect, url_for, session, request, render_template, flash, redirect
from flask import current_app as app, request
from .config import client_id, client_secret, redirect_uri


spotify = OAuth.remote_app( 'spotify',
                            consumer_key=client_id,
                            consumer_secret=client_secret,
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
        return f'Access denied: {resp.message}'

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/me')
    return f"Logged in as id={me.data['id']} name={me.data['name']} redirect={request.args.get('next')}"

@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')