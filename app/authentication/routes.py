from forms import UserLoginForm, UserSignupForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            user = User(first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid form data')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                return redirect(url_for('site.profile'))
            else:
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data')
    return render_template('signin.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))