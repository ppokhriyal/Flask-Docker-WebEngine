from flask import render_template, url_for, flash, redirect, request, abort, session
from dockerwebengine import app, db, bcrypt, login_manager
from dockerwebengine.forms import LoginForm
from dockerwebengine.models import User
from flask_login import login_user, current_user, logout_user, login_required




#Docker Login
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('dashboard'))
		else:	
			flash('Login Unsuccessful. Please check the username and password','danger')
	return render_template('login.html',title='Docker Login',form=form)

#Docker Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html',title='Dashboard')	


#Logout
@app.route('/logout')
def logout():
	logout_user()	
	return redirect(url_for('login'))