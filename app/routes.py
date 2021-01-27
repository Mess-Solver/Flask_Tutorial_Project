from . import app
from flask import render_template,flash,redirect,url_for
from .forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    title='MyPage'
    user={'username':'Kamran'}
    posts=[{'user':{'username':'Shyam'}, 'body':"This is first post"},
           {'user':{'username':'Ram'},'body':'This is second post'},
           ]
    return render_template('index.html',title=title,user=user,posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    title="Login"

    return  render_template("login.html",title=title,form=form)