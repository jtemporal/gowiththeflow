"""API for go with the flow presentaiton"""
import json

from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template,  redirect, session, url_for
from flask_cors import cross_origin

from config import config
from utils.decorators import requires_auth


app = Flask(__name__)
app.secret_key = config['APP']["SECRET_KEY"]
oauth = OAuth(app)

domain = config['AUTH0']["DOMAIN"]
client_id = config['AUTH0']["CLIENT_ID"]
client_secret = config['AUTH0']["CLIENT_SECRET"]

oauth.register(
    "auth0",
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{domain}/.well-known/openid-configuration'
)


@app.get('/')
def home():
    """unprotected home endpoint"""
    return render_template("home.html")


@app.get('/profile')
def profile():
    """unprotected profile endpoint"""
    return render_template("profile.html", session=session.get('user'),
                           pretty=json.dumps(session.get('user'), indent=4))


@app.get('/door')
@cross_origin(allow_headers=["Content-Type", "Authorization"])
@requires_auth
def door():
    """door endpoint: only those authenticated can access it"""
    return render_template("door.html", session=session.get('user'),
                           pretty=json.dumps(session.get('user'), indent=4))


@app.route("/login")
def login():
    """
    Redirects the user to the Auth0 Universal Login 
    (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback redirect from Auth0
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    """
    Logs the user out of the session and from the Auth0 tenant
    """
    session.clear()
    to_encode = {
        "returnTo": url_for("home", _external=True),
        "client_id": client_id,
    }
    return redirect(
        f"https://{domain}/v2/logout?"
        + urlencode(to_encode, quote_via=quote_plus)
    )
