from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

oauth = OAuth(app)

facebook = oauth.register(
    name='facebook',
    client_id=os.environ.get("FACEBOOK_CLIENT_ID"),
    client_secret=os.environ.get("FACEBOOK_CLIENT_SECRET"),
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email'},
)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f"Hola {user['name']} ({user.get('email','No email')})"
    return '<a href="/login">Login con Facebook</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return facebook.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = facebook.authorize_access_token()
    resp = facebook.get('me?fields=id,name,email')
    user_info = resp.json()
    session['user'] = user_info
    return redirect('/')

if __name__ == '__main__':
    app.run()
