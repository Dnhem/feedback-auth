from flask import Flask, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
  return redirect('/register')

@app.route('/secret', methods=['GET', 'POST'])
def show_secret():

  if 'user' not in session:
    flash('Please login first!')
    return redirect('/')

  form = FeedbackForm()
  all_feedback = Feedback.query.all()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data

    new_feedback = Feedback(title=title, content=content, username=session['user'])
    db.session.add(new_feedback)
    db.session.commit()
    flash('Feedback submitted!')
    return redirect('/secret')

  return render_template('/secret.html', form=form, all_feedback=all_feedback)

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
  form = RegisterForm()
  if form.validate_on_submit():
    username = form.username.data
    pwd = form.password.data
    email = form.email.data
    firstname = form.first_name.data
    lastname = form.last_name.data

    new_user = User.register(username,pwd,email,firstname,lastname)
    db.session.add(new_user)
    try:
      db.session.commit()
    except IntegrityError:
      form.username.errors.append('Username taken, please choose another')
      form.email.errors.append('Email already exists!')
      return render_template('/register.html', form=form)

    session['user'] = new_user.username
    flash('Welcome, your account has been created!')
    return redirect('/secret')
  return render_template('/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
  form = LoginForm()

  if form.validate_on_submit():
    username = form.username.data
    pwd = form.password.data
    user = User.authenticate(username, pwd)

    if user:
      flash(f'Welcome back {user.username}!')
      session['user'] = user.username
      return redirect('/secret')
    else:
      form.username.errors = ['Invalid username/password']

  return render_template('/login.html', form=form)

@app.route('/logout')
def logout():
  session.pop('user')
  flash('Goodbye!')
  return redirect('/login')