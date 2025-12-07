import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from event_finder import app, db, bcrypt
from event_finder.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PostFilterForm
from event_finder.models import User, Post, Category
#from event_finder.geo import get_coordinates
from flask_login import login_user, current_user, logout_user, login_required
from geopy.geocoders import Nominatim


@app.route("/")
@app.route("/home/")
def home():
    view = request.args.get('view', 'list')
    form = PostFilterForm(request.args)    
    query = Post.query
#Query only future in the next 3 weeks
    if form:

        if form.title_word.data:
            query = query.filter(Post.title.ilike(f"%{form.title_word.data}%"))
        if form.city.data:
            query = query.filter(Post.address.ilike(f"%{form.city.data}%"))
        if form.category.data:
            query = query.filter_by(category_id=form.category.data)

    if view == "map":

            query = query.filter(Post.latitude != None, Post.longitude != None)
            posts = query.all()

            results = [
                {
                    "id": p.id,
                    "latitude": p.latitude,
                    "longitude": p.longitude,
                    "title": p.title,
                    "address": p.address,
                    "event_date": p.event_date,
                    "url": url_for('post', post_id=p.id)
                }
                for p in posts
            ]
    else:
        page = request.args.get('page', 1, type=int) #1 is the default value for 1. type is the accepted data type as an input
        results = query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=results, view=view, form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success') #success is a bootstrap class for alerts
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'] )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #(hashed pass from db, hashed pass inserted)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #this method returns both, the file name and the file extension, but we are dropping the first one
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_event_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #this method returns both, the file name and the file extension, but we are dropping the first one
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/event_pics', picture_fn)
    
    output_size = (300, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_profile_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)    
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

geolocator = Nominatim(user_agent="event_finder")

def get_coordinates(address):
    location = geolocator.geocode(address, country_codes="", addressdetails=True) #addressdetails include relevant details like 'city'
    if location == None:
        raise ValueError('Please enter an address in Germany')
    lat = location.raw['lat']
    lon = location.raw['lon']
    return [lat, lon]

@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            if form.picture.data:
                image = save_event_picture(form.picture.data)
            else:
                image = None
            lat = get_coordinates(form.address.data)[0]
            lon = get_coordinates(form.address.data)[1]
            post = Post(title=form.title.data, address=form.address.data,
                        latitude=lat, longitude=lon, event_date=form.event_date.data,
                        duration_minutes=form.duration_minutes.data, image=image,
                        content=form.content.data, category_id=form.category.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your quest has been created!', 'success')
            return redirect(url_for('home'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Event')

@app.route("/post/<int:post_id>", methods = ['GET']) # route with a variable inside. With "int:" we specify what kind of variable are we expecting
def post(post_id):
    post = Post.query.get_or_404(post_id) #this new method returns a 404 if the post_id doesnt exist
    lat = post.latitude
    lon = post.longitude
    image = url_for('static', filename='event_pics/' + post.image)
    if post.duration_minutes:
        duration_hours = post.duration_minutes // 60
        duration_mins = post.duration_minutes % 60
    else:
        duration_hours = None
        duration_mins = None
    return render_template('post.html', title=post.title, post=post, lat=lat, lon=lon, image=image, duration_hours=duration_hours, duration_mins=duration_mins)

@app.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #http response for forbidden route
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            post.image = save_event_picture(form.picture.data)
        post.title = form.title.data
        post.content = form.content.data
        post.address = form.address.data
        post.event_date = form.event_date.data
        post.duration_minutes = form.duration_minutes.data
        post.category_id = form.category.data
        db.session.commit() # here we dont use db.session.add because we are not creating new data, but updating it
        flash('Your quest was updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.address.data = post.address
        form.event_date.data = post.event_date
        form.duration_minutes.data = post.duration_minutes
        form.category.data = post.category_id
    return render_template('create_post.html', title='Update Quest',
                           form=form, legend='Update Quest')

@app.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your quest was deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) #1 is the default value for 1. type is the accepted data type as an input
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
