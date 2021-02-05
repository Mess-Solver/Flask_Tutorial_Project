from . import app
from flask import render_template,flash,redirect,url_for,request
from .forms import EmptyForm,LoginForm,RegistrationForm,EditProfileForm,PostForm
from flask_login import current_user,login_user,login_required,logout_user
from .models import User,Post
from werkzeug.urls import url_parse
from app import db
from datetime import datetime


from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    page=request.args.get('page',1,int)
    form=PostForm()
    if form.validate_on_submit():
        post=Post(body=form.post.data,author=current_user,timestamp=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash("Posted Successfully")
        return redirect(url_for('index'))
    title='MyPage'
    posts=current_user.followed_posts().paginate(page,app.config['POSTS_PER_PAGE'],False)

    next_url = url_for('index', page=posts.next_num) \
               if posts.has_next else None

    prev_url = url_for('index', page=posts.prev_num) \
               if posts.has_prev else None

    return render_template('index.html',title=title,posts=posts.items,form=form,next_url=next_url,prev_url=prev_url)


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data)
        user.create_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html',form=form,title="Register")




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if(user is None or not user.check_password(form.password.data)):
            flash("Invalid Username or Password")
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if next_page is None or url_parse(next_page).netloc!='':
            next_page=url_for('index')
        return redirect(next_page)
    title="Login"

    return  render_template("login.html",title=title,form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
        page=request.args.get('page',1,int)
        form=EmptyForm()
        user=User.query.filter_by(username=username).first_or_404()
        posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,app.config["POSTS_PER_PAGE"],False)
        print(type(posts.items))
        next_url=url_for("user",username=user.username, page=posts.next_num) if posts.has_next else None
        prev_url=url_for("user",username=user.username, page=posts.prev_num) if posts.has_prev else None
        return render_template("user.html",user=user,posts=posts.items,form=form,prev_url=prev_url,next_url=next_url)

@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.utcnow()
        db.session.commit()
@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash("Your Changes Have Been Saved")
        return redirect(url_for('edit_profile'))
    elif(request.method=="GET"):
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
    return render_template("edit_profile.html",form=form,title="Edit Profile")


@app.route('/follow/<username>', methods=['GET','POST'])
@login_required
def follow(username):
    form=EmptyForm()
    if form.validate_on_submit:
        user=User.query.filter_by(username=username).first_or_404()
        if user.username==current_user.username:
            flash("Sorry {}, you cannot follow yourself!!!".format(current_user.username))
        current_user.follow(user)
        db.session.commit()
        flash("You are now following {}".format(user.username))
        return redirect(url_for('user',username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>' ,methods=['GET','POST'])
@login_required
def unfollow(username):
    form=EmptyForm()
    if form.validate_on_submit:
        user=User.query.filter_by(username=username).first_or_404()
        current_user.unfollow(user)
        db.session.commit()
        flash("You have stopped following {}".format(user.username))
        return redirect(url_for('user',username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    page=request.args.get("page",1,int)
    posts=Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html",title="Explore",posts=posts.items,next_url=next_url,prev_url=prev_url) #reusing the template


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

from app.forms import ResetPasswordForm

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.create_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)









