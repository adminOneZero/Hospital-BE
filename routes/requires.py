from functools import wraps
from flask import session , redirect , url_for
def login_required(f): # this funnction to make any @route must have login session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			# flash("you must be logged frist","danger")
			return redirect(url_for('login.login_func'))
	return wrap

def admin_required(f): # this funnction to make any @route must have login session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if session['username'] == "admin":
			return f(*args,**kwargs)
		else:
			return render_template('error/404.html')
	return wrap

def logout_required(f): # this funnction to make any @route must have logout session to execute action
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' not in session:
			return f(*args,**kwargs)
		else:
			# flash("you must be logout frist","dark")
			# return redirect(url_for('login.login_func'))
			return 'no'
	return wrap
