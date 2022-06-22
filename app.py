from bottle import run, template, request, route, error, response, redirect
import secrets, bottle, utils
import sqlalchemy as sql
from sqlalchemy.dialects.mysql import insert
from datetime import datetime, timedelta
##pip install mysql-connector-python bottle SQLAlchemy

##IT's either API creation OR automate function.


engine = sql.create_engine('mysql+mysqlconnector://root:@localhost/bottle') ##username:password@host:port/database
metadata = sql.MetaData(bind=engine)

SecretKey = "1YDfBk-gk2lqXAHn0vWZtx1rO2WYq_9x1gFyuMWO7Hw"

def flash(msg, tag="info"):
	response.set_cookie("notification", f"{tag}:::● {msg}" if not "●" in msg else f"{tag}::: {msg}")

def is_logged(conn=engine.connect()):
	sid = request.get_cookie("sid", secret=SecretKey)
	if sid:
		sessions = sql.Table('sessions', metadata, autoload = True)
		query = conn.execute(sql.select(sessions).where(sessions.c.id == sid, sessions.c.data == utils.hasher(request.get_header("User-Agent")+request.remote_addr))).first()
		if query is not None:
			if query._asdict()['created_at'] + timedelta(days=2) > datetime.now():
				return True, query._asdict()['email']
		return False, None
	return False, None

def get_user():
	conn = engine.connect()
	check, email = is_logged(conn)
	if check:
		users = sql.Table('users', metadata, autoload = True)
		query = conn.execute(sql.select(users.c.id, users.c.email, users.c.username, users.c.is_activated).where(users.c.email == email)).first()
		return query._asdict()
	return None

@route('/', method="GET")
def index():
	user = get_user()
	return template('indexTemplate', user=user)

@route('/apps', method="GET")
def apps():
	user = get_user()
	if user:
		conn = engine.connect()
		apps = sql.Table('apps', metadata, autoload = True)
		appsList = conn.execute(sql.select(apps).where(apps.c.user == user["id"])).fetchall()
		return template('appsTemplate', user=user, appsList=appsList)
	else:
		flash("You need to login first")
		redirect("/login")

@route('/apps/create', method=["GET", "POST"])
def appsCreate():
	user = get_user()
	if user:
		if request.method == "GET":
			csrf = secrets.token_hex(16)
			response.set_cookie("csrf", csrf, secret=SecretKey, httponly=True, secure=True, path="/apps/create", SameSite="Strict")
			return template('appsCreateTemplate', csrf=csrf, user=user)
		if request.method == "POST":
			csrf = request.get_cookie("csrf", secret=SecretKey)
			userCsrf = request.forms.get("csrfmiddlewaretoken")
			
			title = request.forms.get('title')
			letype = request.forms.get('type')
			data = request.forms.get('data')
			
			FormErrors = utils.FormValidator(title, "title") +  utils.FormValidator(letype, "letype") +  utils.FormValidator(data, "data")
			
			if FormErrors:
				flash("<br>".join(FormErrors), "error")
				redirect("/apps/create")
			
			else:
				if csrf == userCsrf and userCsrf and csrf:
					conn = engine.connect()
					apps = sql.Table('apps', metadata, autoload = True)
					conn.execute(apps.insert().values(user=user["id"], title=title, letype=letype, data=data))
					
					flash("Created successfuly.", "success")
					redirect("/apps")
				
				else:
					flash("There was an error, try again.", "error")
					redirect("/apps/create")
			
	else:
		flash("You need to login first")
		redirect("/login")

@route('/login', method=["GET", "POST"])
def login():
	logged, _ = is_logged()
	if not logged:
		if request.method == "GET":
			csrf = secrets.token_hex(16)
			response.set_cookie("csrf", csrf, secret=SecretKey, httponly=True, secure=True, path="/login", SameSite="Strict")
			return template('loginTemplate', csrf=csrf)
			
		if request.method == "POST":
			csrf = request.get_cookie("csrf", secret=SecretKey)
			userCsrf = request.forms.get("csrfmiddlewaretoken")
			
			email = request.forms.get('email')
			password = request.forms.get('password')
			
			FormErrors = utils.FormValidator(email, "email")
			
			conn = engine.connect()
			users = sql.Table('users', metadata, autoload = True)
			query = conn.execute(sql.select(users).where(users.c.email == email)).first()
			
			if FormErrors:
				flash("<br>".join(FormErrors), "error")
				redirect("/login")
			elif query is None:
				flash("Email doesn't exist. create a new account if you don't have one.", "error")
				redirect("/login")
			else:
				if csrf == userCsrf and userCsrf and csrf:
					csrf = secrets.token_hex(16)
					response.set_cookie("csrf", csrf, secret=SecretKey, httponly=True, secure=True, path="/login", SameSite="Strict")

					query = conn.execute(sql.select(users).where(users.c.email == email, users.c.password == utils.sign(SecretKey, password))).first()
					if query is not None:
						session_id = secrets.token_hex(24)
						sessions = sql.Table('sessions', metadata, autoload = True)
						
						user_agent = request.get_header("User-Agent")
						ip_address = request.remote_addr
						if user_agent and ip_address:
							conn.execute(insert(sessions).values(id=session_id, email=email, data=utils.hasher(user_agent+ip_address)).on_duplicate_key_update(id=session_id, data=utils.hasher(user_agent+ip_address)))
							response.set_cookie("sid", session_id, secret=SecretKey, httponly=True, secure=True, path="/", SameSite="Strict")
						
							flash(f"Welcome back {query._asdict()['username']}.", "success")
							redirect("/")
						else:
							flash("There was an error, please try again later.", "error")
							redirect("/login")
					else:
						flash("Email or password is incorrect.", "error")
						redirect("/login")
				else:
					
					flash("There was an error, try again.", "error")
					redirect("/login")
	else:
		flash(f"You are already logged in.")
		redirect("/")

@route('/signup', method=["GET", "POST"])
def signup():
	logged, _ = is_logged()
	if not logged:
		if request.method == "GET":
			csrf = secrets.token_hex(16)
			response.set_cookie("csrf", csrf, secret=SecretKey, httponly=True, secure=True, path="/signup", SameSite="Strict")
			return template('signupTemplate', csrf=csrf)
			
		if request.method == "POST":
			csrf = request.get_cookie("csrf", secret=SecretKey)
			userCsrf = request.forms.get("csrfmiddlewaretoken")
			
			email = request.forms.get('email')
			username = request.forms.get('username')
			password = request.forms.get('password')
			
			FormErrors = utils.FormValidator(email, "email") + utils.FormValidator(username, "username") + utils.FormValidator(password, "password")
			
			conn = engine.connect()
			users = sql.Table('users', metadata, autoload = True)
			query = conn.execute(sql.select(users).where(users.c.email == email)).first()
			
			if FormErrors:
				flash("<br>".join(FormErrors), "error")
				redirect("/signup")
			elif query is not None:
				flash("Email already used, Login or create a new account.", "error")
				redirect("/signup")
			else:
				if csrf == userCsrf and userCsrf and csrf:
					csrf = secrets.token_hex(16)
					response.set_cookie("csrf", csrf, secret=SecretKey, httponly=True, secure=True, path="/signup", SameSite="Strict")
					
					conn.execute(users.insert().values(email=email, username=username, password=utils.sign(SecretKey, password)))
					
					flash("signuped.", "success")
					redirect("/login")
				else:
					
					flash("There was an error, please try again.", "error")
					redirect("/signup")
	else:
		flash(f"You are already logged in.")
		redirect("/")

@route('/logout', method="GET")
def logout():
	logged, email = is_logged()
	if logged:
		response.delete_cookie("sid")
		conn = engine.connect()
		sessions = sql.Table('sessions', metadata, autoload = True)
		conn.execute(sessions.delete().where(sessions.c.email == email))
		
	flash("Logged out successfuly.", "success")
	redirect("/")


@error(404)
def error404(error):
	return 'Nothing here, sorry'
   
### apprently /example and /example/ are two different URLs 
class StripPathMiddleware(object):
	def __init__(self, app):
		self.app = app
	def __call__(self, e, h):
		e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
		return self.app(e,h)


bottle.DEBUG = True

app = bottle.app()
myapp = StripPathMiddleware(app)
bottle.run(app=myapp, host='localhost', port=9999)
