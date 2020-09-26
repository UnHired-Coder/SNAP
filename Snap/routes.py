from Snap.models import User, Post, Comments
from flask import render_template,redirect,url_for,request
from Snap.forms import RegistrationForm, LoginForm,PostForm,UpdateAccountForm
from Snap import app, db, bcrypt
from flask_login import login_user, current_user, login_required,logout_user
import os
import secrets
from PIL import Image
from PIL import Image



from flask import Flask, session, jsonify
from flask_oauthlib.client import OAuth

from flask_socketio import SocketIO

#socketio = SocketIO()
async_mode=None

socketio = SocketIO(app, async_mode=async_mode)




print('3')
@login_required
@app.route("/home",methods=['GET','POST'])
def home():
    user=User.query.all()
    posts = Post.query.all()
    #comments = Comments.query.all()
    return render_template('home.html',title='Home', posts=posts,user=user)
print('3')


@app.route("/about")
def about():
    return render_template('about.html',title='About')

print('3')
@app.route("/register",methods=['GET','POST'])
def register():
     if current_user.is_authenticated:
        return redirect(url_for('home'))
     form = RegistrationForm()
     if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
     return render_template("register.html", title='Register', form=form)

print('2')
@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return  redirect(url_for('home'))
    return render_template("login.html", title="Login", form=form)



























app.config['GOOGLE_ID'] = "612662773449-dvcnkiev2n9q3if6pp0jdrsp8j94k6a0.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "aSg4XneVXt6LwzksGY9j6bC3"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

print('2')

@app.route('/login_google')
def login_google():
    return google.authorize(callback=url_for('authorized', _external=True))

print('2')
@app.route('/logout')
def logout():
    session.pop('google_token', None)
    logout_user()
    return redirect(url_for('login'))

print('2')
@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')

    user = User.query.filter_by(email=me.data.get('email')).first()
    if user and bcrypt.check_password_hash(user.password, me.data.get('id')):
        login_user(user)
        return  redirect(url_for('home'))

    hashed_password = bcrypt.generate_password_hash(me.data.get('id')).decode('utf-8')
    user = User(username=me.data.get('name'), email=me.data.get('email'), password=hashed_password,image_url=me.data.get('picture'),bio='Hi this is me')
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=False)
    return  redirect(url_for('home'))

print('2')
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


def save_picture_profile(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (400,350)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:

            picture_file = save_picture_profile(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email .data
        current_user.bio = form.bio .data
        current_user.Link_facebook = form.link.data
        db.session.commit()

    #    flash(f'your account has been updated! ')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio .data= current_user.bio
        form.link.data=current_user.Link_facebook
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account",form=form ,image_file = image_file)




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    output_size = (400,350)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn




@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        picture_file='default.jpg'
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        post = Post( title=form.title.data, content= form.content.data, user_id=current_user.id, tag=form.tag.data ,post_file=picture_file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create_post.html', title= 'NewPost', form=form)







@app.route('/account/<int:post_id>',methods=['GET','POST'])
@login_required
def user_account(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:

            picture_file = save_picture_profile(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email .data
        current_user.bio = form.bio .data
        current_user.Link_facebook = form.link.data
        db.session.commit()

    #    flash(f'your account has been updated! ')
        return redirect(url_for('user_account',post_id=post.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio .data= current_user.bio
        form.link.data=current_user.Link_facebook
    image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
    return render_template("user_account.html",post=post,form=form,image_file=image_file)















@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)



def messageRecived():
    print( 'message was received!!!' )

@socketio.on( 'my event_is' )
def handle_my_custom_event( json ):
    print("---------------initialize data here------------------")


@socketio.on( 'my event' )
def handle_my_custom_event( json ):
    post = Post.query.filter_by(id=json.get('post_id')).first_or_404()
    if json.get('action') == 'like':
        current_user.like_post(post)
        db.session.commit()
    if json.get('action') == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    print( '-----------------------------------------recived my event:---------------------------- ' + str( json ) )
    print( 'recived my event:------------- ' + str( json.get('post_id')) )



    socketio.emit( 'my response', json, callback=messageRecived )






@socketio.on( 'my fevent' )
def handle_my_custom_fevent( json ):
    user = User.query.filter_by(id=json.get('user_id')).first_or_404()
    if json.get('action') == 'follow':
        current_user.follow_user(user.id)
        db.session.commit()
    if json.get('action') == 'unfollow':
        current_user.unfollow_user(user.id)
        db.session.commit()
    print( '-----------------------------------------recived my event:---------------------------- ' + str( json ) )
    print( 'recived my event:------------- ' + str( json.get('user_id')) )



    socketio.emit( 'my fresponse', json, callback=messageRecived )










@socketio.on( 'my_comment event' )
def handle_my( json ):
    post = Post.query.filter_by(id=json.get('post_id')).first_or_404()

    post.make_comment(json.get('message'))
    db.session.commit()
    print( '==================recived my event:=========== ' + str( json ) )
    socketio.emit( 'my_comment response', json, callback=messageRecived )






@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post= post)



@app.route("/search")
def search():
    q = request.args.get('query')
    susers=User.query.whoosh_search(q).all()
    res = True
    if len(susers) == 0:
        res = False
    return render_template('search_results.html', users=susers,result = res)
