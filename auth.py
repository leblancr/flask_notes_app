from flask import Blueprint, render_template, request, flash


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', text='testing')


@auth.route('/logout')
def logout():
    return render_template('login')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

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
            flash("account created")

    return render_template('sign_up.html')

