from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from src.main import db,login_manager
from src.forms.login import LoginForm,RegisterForm
from src.models.user import User


auth = Blueprint('auth', __name__,url_prefix='/admin')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
  
    if form.validate_on_submit():
        
      
        user = User.query.filter_by(email=form.email.data).first()
      
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('auth.register'))
    return render_template('login.html', title='Login', form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            db.session.add(User(
                email=form.email.data, 
                password=form.password.data
                )
            )
            db.session.commit()
            flash('Successfully Registered', 'success')
            return redirect(url_for('home.home'))
        else: 
            flash('User Already Registered. Please Login', 'warning')
            return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Register', form=form)
    
    
    
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.home'))