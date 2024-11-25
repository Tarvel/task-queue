from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.wtform import RegisterForm, LoginForm
from app.models import User
from app import bcrypt, db
from app.route import tasks
from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint('auth', __name__,
               template_folder='templates',
               static_folder='static')

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pwrd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username = form.username.data
        email = form.email.data
        
        user = User(username=username, email=email, password=hashed_pwrd)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect(url_for('task.index'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            
            next_page = request.args.get('next')
            flash(f'Welcome {user.username}')
            return redirect(next_page) if next_page else redirect(url_for('task.index'))
        else:
            flash('username or password incorrect')

    return render_template("login.html", form=form)

@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))