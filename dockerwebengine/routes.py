import docker
from cpuinfo import get_cpu_info
from psutil import virtual_memory
from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
from dockerwebengine import app, db, bcrypt, login_manager			
from dockerwebengine.forms import LoginForm
from dockerwebengine.models import User
from flask_login import login_user, current_user, logout_user, login_required



#Docker API Connection Global variables
apiclient = docker.APIClient(base_url='unix://var/run/docker.sock')
client = docker.from_env()

#Docker Refresh System Information
@app.route('/dockerinfo',methods=['POST'])
def docker_info():

	info_dict = {}

	#CPU / Memory Information
	cpu = get_cpu_info()
	mem = virtual_memory()
	ram = mem.total / 1024 / 1024 / 1024

	#Docker API Low Level
	dockerinfo =apiclient.version()

	info_dict['ramsize'] = ram
	info_dict['cpuinfo'] = cpu.get('count')
	info_dict['docker_version'] = dockerinfo.get('Version')
	info_dict['docker_api_version'] = dockerinfo.get('ApiVersion')
	info_dict['os'] = dockerinfo.get('Os')
	info_dict['arch'] = dockerinfo.get('Arch')
	info_dict['kernel_version'] = dockerinfo.get('KernelVersion')

	return info_dict

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
	infodict = docker_info()

	return render_template('dashboard.html',title='Dashboard',infodict=infodict)


#Logout
@app.route('/logout')
def logout():
	logout_user()	
	return redirect(url_for('login'))