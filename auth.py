from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)  # from flask_login
                flash('login successful', category='success')
                return redirect(url_for('views.home'))  # blueprint and function
            else:
                flash('incorrect password', category='error')
        else:
            flash('email does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    print(current_user.is_authenticated)

    logout_user()
    print(current_user.is_authenticated)
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')  # ids from html form
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('email already exists', category='error')
            return redirect(url_for('views.home', user=user))  # blueprint and function

        fields_valid = True

        if len(email) < 4:
            flash('Email must be longer than 4 characters', category='error')
            fields_valid = False
        if len(first_name) < 2:
            flash('name must be longer than 2 characters', category='error')
            fields_valid = False
        if password1 != password2:
            flash("passwords don\'t match", category='error')
            fields_valid = False
        if len(password1) < 7:
            flash("password must be greater than 6", category='error')
            fields_valid = False
        if fields_valid:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1,
                            method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("account created")
            return redirect(url_for('views.home'))  # blueprint and function

    return render_template('sign_up.html', user=current_user)

