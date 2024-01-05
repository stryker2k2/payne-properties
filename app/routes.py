from flask import render_template, flash, request, redirect, url_for, session
# from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Users, Posts, Properties
from app.webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm, PropertyForm
from functools import wraps
import uuid as uuid
import os

## Routes ##
# Root Route
@app.route('/')
def index():
    # return redirect(url_for('posts'))
    return render_template('index.html')

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            # Check Password Hash
            if check_password_hash(user.password_hash, form.password.data):
                # login_user(user)

                session["id"] = user.id
                session["is_admin"] = user.is_admin

                flash('Login Successful')                
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password')
        else:
            flash('Invalid Username')
    return render_template('login.html', form = form)

def session_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if "id" not in session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return decorated

# Dashboard Page Route
@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
@session_required
def dashboard():
    form = UserForm()
    # id = session["id"]
    id = session["id"]
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']

        # Check for pre-existing profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']
        
            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save Profile Pic
            saver = request.files['profile_pic']
            
            # Override profile_pic to be just a String in Database
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                if saver:
                    saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                    flash("User Updated Successfully")
                    return render_template('dashboard.html',
                        form = form,
                        name_to_update = name_to_update)
                else:
                    flash("Request File Error!")
                    return render_template('dashboard.html',
                    form = form,
                    name_to_update = name_to_update)
            except:
                flash("Database Error!")
                return render_template('dashboard.html',
                    form = form,
                    name_to_update = name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template('dashboard.html',
                form = form,
                name_to_update = name_to_update)
    else:
        return render_template('dashboard.html',
                form = form,
                name_to_update = name_to_update,
                id = id)


# Admin Route
@app.route('/admin')
# @app.route('/admin')
# @login_required
@session_required
def admin():
    propertyForm = PropertyForm()
    userForm = UserForm()
    id = session["id"]  
    if id == app.config['ADMIN_ID'] or session["is_admin"]:
        tenants = Users.query.order_by(Users.date_added)
        properties = Properties.query.order_by(Properties.id)
        return render_template('admin.html',
                               properties = properties,
                               tenants = tenants,
                               propertyForm = propertyForm,
                               userForm = userForm)
    else:
        flash('You must be an administrator to access this page')
        return redirect(url_for('dashboard'))
    
# Admin Route
@app.route('/admin', methods=['POST'])
# @app.route('/admin')
# @login_required
@session_required
def admin_post():
    propertyForm = PropertyForm()  
    userForm = UserForm()
    id = session["id"] 
    if id == app.config['ADMIN_ID'] or session["is_admin"]:
        print(userForm.name.data, userForm.username.data, userForm.email.data, userForm.is_admin.data)
        if propertyForm.validate_on_submit():
            print('[+] Adding Property to Database')
            property = Properties(name = propertyForm.name.data,
                                  address = propertyForm.address.data,
                                  rent = propertyForm.rent.data)
            db.session.add(property)
            db.session.commit()
            flash('Property Added Successfully!')        
        elif userForm.validate_on_submit():
            # Hash the Password
            hashed_pw = generate_password_hash(userForm.password_hash.data, "sha256")
            user = Users(name = userForm.name.data,
                username = userForm.username.data,
                email = userForm.email.data,
                password_hash = hashed_pw)
            print('\n[+] Adding User to Database')
            db.session.add(user)
            db.session.commit()
            flash('User Added Successfully!')
        else:
            flash('Error Validating Form!')
        return redirect(url_for('admin')) 
    else:
        flash('You must be an administrator to access this page')
        return redirect(url_for('dashboard'))












# Logout Page Route
@app.route('/logout', methods=['GET', 'POST'])
# @login_required
@session_required
def logout():
    # logout_user()
    # session.pop('id', None)
    # session.pop('is_admin', None)
    session.clear()

    flash('Succesfully Logged Out')
    return redirect(url_for('login'))


# Blog Home Page
@app.route('/posts')
def posts():
    # Grab all posts from database 
    # newest first = order_by(Posts.date_posted.desc())
    # oldest first = order_by(Posts.date_posted)
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template('posts.html', posts = posts)


# Add User Page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    email = None
    form = UserForm()
    # Validate Form
    # https://flask-wtf.readthedocs.io/en/0.15.x/form/
    if form.validate_on_submit():
        name = Users.query.filter_by(email=form.email.data).first()
        if name is None:
            # Hash the Password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name = form.name.data,
                username = form.username.data,
                email = form.email.data,
                password_hash = hashed_pw)
            print('\n[+] Adding User to Database')
            db.session.add(user)
            db.session.commit()
            flash('User Added Successfully!')
        else:
            print('[!] Error adding User to Database')
            print(form.name.errors)
            flash('Failed to Add User!')
        name = form.name.data
        email = form.email.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
    this_user = Users.query.filter_by(email=email).first()
    return render_template('add_user.html',
        form = form, 
        name = name,
        this_user = this_user)


# Password Test Page
# @app.route('/test_pw', methods=['GET', 'POST'])
# def test_pw():
#     email = None
#     password = None
#     pw_to_check = None
#     passed = None
#     form = PasswordForm()
#     # Validate Form
#     # https://flask-wtf.readthedocs.io/en/0.15.x/form/
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password_hash.data
#         form.email.data = ''
#         form.password_hash.data = ''
#         # Lookup user by email address
#         pw_to_check = Users.query.filter_by(email=email).first()
#         # Check Hashed Password
#         passed = check_password_hash(pw_to_check.password_hash, password)
#     return render_template('test_pw.html',
#         email = email,
#         password = password,
#         pw_to_check = pw_to_check,
#         passed = passed,
#         form = form)


# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
# @login_required
@session_required
def update(id):
    if session["id"] == id or session["id"] == app.config['ADMIN_ID'] or session["is_admin"]:
        form = UserForm()
        name_to_update = Users.query.get_or_404(id)
        if request.method == 'POST':
            name_to_update.name = request.form['name']
            name_to_update.email = request.form['email']
            name_to_update.username = request.form['username']
            name_to_update.is_admin = request.form['is_admin']
            try:
                db.session.commit()
                flash("User Updated Successfully")
                return render_template('update.html',
                    form = form,
                    name_to_update = name_to_update,
                    id = id)
            except:
                flash("Database Error!")
                return render_template('update.html',
                    form = form,
                    name_to_update = name_to_update,
                    id = id)
        else:
            return render_template('update.html',
                    form = form,
                    name_to_update = name_to_update,
                    id = id)
    else:
        flash("You do not have permission to update this user!")
        return redirect(url_for('dashboard'))


# Delete Record from Database
@app.route('/delete/<int:id>')
# @login_required
@session_required
def delete(id):
    if session["id"] == id or session["id"] == app.config['ADMIN_ID'] or session["is_admin"]:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!")

            tenants = Users.query.order_by(Users.date_added)
            return render_template('add_user.html',
                form = form, 
                name = name,
                tenants = tenants)

        except:
            flash("Deleting User Error!")
            return render_template('add_user.html',
                form = form, 
                name = name,
                tenants = tenants)
    else:
        flash("You do not have permission to delete that user!")
        return redirect(url_for('dashboard'))


# JSON Page
@app.route('/date')
def get_current_date():
    return {"Date": date.today()}


# Post Page
@app.route('/add-post', methods=['GET', 'POST'])
# @login_required
@session_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = session["id"]
        post = Posts(title=form.title.data, 
            content=form.content.data,
            poster_id=poster,
            slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
        form.slug.data = ''

        # Add Post data to Database
        db.session.add(post)
        db.session.commit()
        flash("Blog Post submitted successfully!")

    # Redirect to webpage
    return render_template('add_post.html', form=form)


# View Individual Post Page
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


# Edit Post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
@session_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        #Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post was updated successfully")
        return redirect(url_for('post', id=post.id))
    if session["id"] == post.poster_id or session["id"] == app.config['ADMIN_ID'] or session["is_admin"]:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You are not authorized to edit that post")
        return redirect(url_for('posts', posts=posts))


# Pass params/args to base.html then to navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Search Route
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('search.html', 
            form=form,
            searched=post.searched,
            posts=posts)


# Delete Post
@app.route('/posts/delete/<int:id>')
# @login_required
@session_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    # id = session["id"]
    if session["id"] == post_to_delete.poster_id or session["id"] == app.config['ADMIN_ID'] or session["is_admin"]:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Post deleted successfully!')
            # Grab all posts from database and display
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts = posts)
        except:
            flash('There was an issue deleting that post')
            # Grab all posts from database and display
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts = posts)
    else:
        flash('You are not authorized to delete that post')
        # Grab all posts from database and display
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts = posts)


## Custom Error Page(s) ##
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500