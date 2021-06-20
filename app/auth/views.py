
from flask import render_template,redirect,url_for,flash,request
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm, SignUpForm
from .. import db, photos
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Log In | Blogg"
    return render_template('auth/login.html',login_form = login_form,title=title)


@auth.route('/register',methods = ["GET","POST"])
def register():
    registration_form = SignUpForm()
    if registration_form.validate_on_submit():
        filename = photos.save(registration_form.profile.data)
        profile_pic_path = f'img/{filename}'
        user = User(email = registration_form.email.data, fname= registration_form.fname.data, lname=registration_form.lname.data, username = registration_form.username.data, profile_pic_path=profile_pic_path, password = registration_form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Blogg.","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))

    title = 'Sign Up | Blogg'
    return render_template('auth/register.html', registration_form = registration_form, title = title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))
