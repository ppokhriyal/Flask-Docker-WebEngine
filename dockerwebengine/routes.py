from flask import render_template, url_for, flash, redirect, request, abort, session
from dockerwebengine import app
from dockerwebengine.forms import LoginForm




#Docker Login
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login Unsuccessful. Please check the username and password','danger')
	return render_template('login.html',title='Docker Login')