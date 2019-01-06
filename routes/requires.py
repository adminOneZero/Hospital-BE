# -*- coding: utf-8 -*-

from functools import wraps
from flask import session , redirect , url_for


def login_required(f): # this funnction to make any @route must have login session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session and session['logged_in'] != None:
			return f(*args,**kwargs)
		else:
			return redirect(url_for('login.login_func'))
	return wrap

def admin_required(f): # this funnction to make any @route must have login session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'level' in session['level'] and session['level'] == "1":
			return f(*args,**kwargs)
		else:
			return render_template('error/404.html')
	return wrap

def logout_required(f): # this funnction to make any @route must have logout session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' not in session or  session['logged_in'] == None:
			return f(*args,**kwargs)
		else:
			return redirect(url_for('admin.admin_func'))
	return wrap

def backend_flash(f): # this funnction to make any @route must have login session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'flash' in session:
			return f(*args,**kwargs)
		else:
			session['flash'] = []
			return f(*args,**kwargs)
	return wrap
