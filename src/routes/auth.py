from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from src.main import db, bcrypt,login_manager
from src.forms.login import LoginForm
from src.models.user import User


auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
  
    if form.validate_on_submit():
        
        # db.session.add(User(email="apkvandagadde2@gmail.com", password="24111999"))
        # db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
      
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.login'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))