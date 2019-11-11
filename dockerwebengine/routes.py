import docker
from docker import errors
import logging
import json
import requests
from cpuinfo import get_cpu_info
from psutil import virtual_memory
from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
from dockerwebengine import app, db, bcrypt, login_manager			
from dockerwebengine.forms import LoginForm, SearchImageForm
from dockerwebengine.models import User
from flask_login import login_user, current_user, logout_user, login_required



#Docker API Connection Global variables
apiclient = docker.APIClient(base_url='unix://var/run/docker.sock')
client = docker.from_env()

#Docker Refresh System Information
@app.route('/dockerinfo')
def docker_info():

	info_dict = {}

	#CPU / Memory Information
	cpu = get_cpu_info()
	mem = virtual_memory()
	ram = mem.total / 1024 / 1024 / 1024

	#Docker API Low Level
	dockerinfo = apiclient.version()


	info_dict['ramsize'] = ram
	info_dict['cpuinfo'] = cpu.get('count')
	info_dict['docker_version'] = dockerinfo.get('Version')
	info_dict['docker_api_version'] = dockerinfo.get('ApiVersion')
	info_dict['os'] = dockerinfo.get('Os')
	info_dict['arch'] = dockerinfo.get('Arch')
	info_dict['kernel_version'] = dockerinfo.get('KernelVersion')
	info_dict['image_count'] = len(apiclient.images())
	info_dict['container_count'] = len(apiclient.containers(all=True))
	info_dict['volume_count'] = len(client.volumes.list())
	info_dict['network_count'] = len(apiclient.networks())

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
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
	infodict = docker_info()
	return render_template('dashboard.html',title='Dashboard',infodict=infodict)
	return jsonify({'result':'success'})

@app.route('/refresh',methods=['POST'])
def refresh():
	infodict = docker_info()
	return jsonify({'result':'success','imagerefresh':infodict.get('image_count'),'containerrefresh':infodict.get('container_count'),
		'volumerefresh':infodict.get('volume_count'),'networkrefresh':infodict.get('network_count')}) 

#Docker Local Images
@app.route('/local_images',methods=['GET','POST'])
@login_required
def local_images():
	infodict = docker_info()
	return render_template('local_image.html',title='Images',infodict=infodict,apiimage=apiclient.images(),client=client)


#Docker Pull Image
@app.route('/pull_image',methods=['GET','POST'])
def pull_image():
	if request.method == "POST":
		len_search_text = len(apiclient.search(request.form['searchimage']))

	return render_template('pull_image.html',len_search_text=len_search_text)	

#Docker Remove Image request
@app.route('/delete_image/<id>',methods=['GET','POST'])
def del_image(id):

	try:
		
		apiclient.remove_image(id)
		infodict = docker_info()

		return jsonify({'result':'success','imagerefresh':infodict.get('image_count')})

	except Exception as e:
		print (str(e))
		return jsonify({'result':'fail','msg':str(e)})

#Logout
@app.route('/logout')
def logout():
	logout_user()	
	return redirect(url_for('login'))