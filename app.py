from flask import *
from flask_mysqldb import MySQL
from functools import wraps
from datetime import datetime, timedelta

import os.path
#import os.urandom

#path to the images folder to store uploaded pictures
UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'bmp', 'gif'])

app = Flask(__name__, template_folder='views', static_folder='images')
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Natal13!'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'group36pa2'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql.init_app(app)

#put this line before the route for the url
#   /ilrj0i/pa2
#i.e. for /user => /ilrj0i/pa2


def check_auth(username, password):
	cursor = mysql.connection.cursor()
	query = '''SELECT password FROM User WHERE username=''' + "'" +  username + "'"
	cursor.execute(query)
	dbpassword = cursor.fetchall()
	return dbpassword[0][0] == password

def authenticate():
	return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		print("hey")
		print(auth.username)
		print(auth.password)
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated


@app.route('/ilrj0i/pa2/', methods=['GET'])
def main_route():

	# The next line gets the global application object
	#app = current_app._get_current_object()
	# The following code gets the mysql object from app and creates a connection/cursor
	#connection = app.mysql.connect()
	#"""
	#cursor = mysql.connection.cursor()
	#cursor.execute('''SELECT * FROM User''')
	#users = cursor.fetchall()
	#return render_template("index.html", users = users)
	#"""
	#import pdb; pdb.set_trace()
	cursor = mysql.connection.cursor()
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		cursor = mysql.connection.cursor()
		query = '''SELECT * FROM Album WHERE access="public"'''
		cursor.execute(query)
		albums = cursor.fetchall()
		return render_template("index.html", albums = albums, username = username, login = "yes")
	cursor = mysql.connection.cursor()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	"""if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes = 5):
			##############logout
			logout()
		session['lastactivity'] = datetime.now()
		#username = session['username']
		query =  '''SELECT * FROM Album INNER JOIN AlbumAccess ON AlbumAccess.albumid=Album.albumid WHERE AlbumAccess.username=''' + "'" + username + "'"
		cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums, login = "no")"""


	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			##############logout
			logout()
		session['lastactivity'] = datetime.now()
		username = session['username']
		query =  '''SELECT * FROM Album INNER JOIN AlbumAccess ON AlbumAccess.albumid=Album.albumid WHERE AlbumAccess.username=''' + "'" + username + "'"
		cursor.execute(query)
		#######own albums?
		albumsadd = cursor.fetchall()
		albums = albums + albumsadd
		####login yes = html will load the "logged in as" navbar
		return render_template("index.html", albums = albums, username = username, login = "yes")
	return render_template("index.html", albums = albums, login = "no")

#if op==signin
#OTHER AUTHENTICATION SHIT!!!

@app.route('/ilrj0i/pa2/', methods=['POST'])
def userloginpost():
	#checks database for username
	username = request.form['username']
	password = request.form['password']
	cursor = mysql.connection.cursor()
	query = '''SELECT password FROM User WHERE username=''' + "'" +  username + "'"
	cursor.execute(query)
	dbpassword = cursor.fetchall()
	if len(dbpassword) == 0:
		return render_template("login.html", username = "no", login = "no")
	if dbpassword[0][0] != password:
		return render_template("login.html", password = "no", login = "no")

	session['username'] = username
	session['lastactivity'] = datetime.now()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor = mysql.connection.cursor()
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums, username = username, login = "yes")

@app.route('/ilrj0i/pa2/user', methods=['GET'])
def signup():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		return render_template("edituser.html", username = username, login = "yes")
	return render_template("user.html", login = "no")

@app.route('/ilrj0i/pa2/user', methods=['POST'])
def createaccount():
	###session?
	username = request.form['username']
	firstname = request.form['firstname']
	lastname = request.form['lastname']
	password = request.form['password']
	email = request.form['email']
	#####check if username already exists
	cursor = mysql.connection.cursor()
	query = '''SELECT username FROM User WHERE username=''' + "'" + username + "'"
	cursor.execute(query)
	user = cursor.fetchall()
	if len(user) > 0:
		return render_template("user.html", username = "no", login = "no")
	query = '''INSERT INTO User VALUES (''' + "'" + username + "', '" + firstname + "', '" + lastname + "', '" + password + "', '" + email + "')"
	cursor.execute(query)
	mysql.connection.commit()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums, username = username, login = "yes")


@app.route('/ilrj0i/pa2/user/edit', methods=['GET'])
@requires_auth
def edituserget():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		return render_template("edituser.html", username = username, login = "yes")
	return render_template("login.html", login = "no")

@app.route('/ilrj0i/pa2/user/edit', methods=['POST'])
@requires_auth
def edituserpost():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		username = request.form['username']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor()
		query = '''UPDATE User SET firstname=''' + "'" + firstname + "', lastname=" + "'" + lastname + "', password=" + "'" + password + "', email=" + "'" + email + "' WHERE username=" + "'" + username + "'"
		cursor.execute(query)
		mysql.connection.commit()
		return render_template("edituser.html", username = username, login = "yes")
	return render_template("login.html", login = "no")

@app.route('/ilrj0i/pa2/user/login', methods=['GET'])
def userloginget():
	return render_template("login.html", login = "no")



@app.route('/ilrj0i/pa2/user/delete', methods=['POST'])
@requires_auth
def deleteuser():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		username = request.form['username']
		cursor = mysql.connection.cursor()
		query = '''DELETE FROM User WHERE username=''' + "'" + username + "'"
		cursor.execute(query)
		mysql.connection.commit()
		query = '''SELECT * FROM Album WHERE access="public"'''
		cursor.execute(query)
		albums = cursor.fetchall()
		return render_template("index.html", albums = albums, login = "no")
	return render_template("login.html", login = "no")


@app.route('/ilrj0i/pa2/user/logout')
@requires_auth
def logout():
	if 'username' in session:
		#if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
		#	logout()
		#session['lastactivity'] = datetime.now()
		#username = session['username']
		session.pop('username', None)
		session.pop('lastactivity', None)
		cursor = mysql.connection.cursor()
		query = '''SELECT * FROM Album WHERE access="public"'''
		cursor = mysql.connection.cursor()
		cursor.execute(query)
		albums = cursor.fetchall()
		return render_template("index.html", albums = albums, login = "no")
	return render_template("login.html", login = "no")


@app.route('/ilrj0i/pa2/albums')
@requires_auth
def albumsss():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		cursor = mysql.connection.cursor()
		query = '''SELECT * FROM Album WHERE username=''' + "'" + username + "'"
		cursor.execute(query)
		albums = cursor.fetchall()
		return render_template("albums.html", albums = albums, username = username, login = "yes")
	return render_template("login.html", login = "no")


@app.route('/ilrj0i/pa2/album')
def albumfunc():
	#import pdb; pdb.set_trace()

	albumid = request.args.get('id')
	cursor = mysql.connection.cursor()
	#import pdb; pdb.set_trace()
	query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
	#query = '''SELECT Contain.*, Photo.url FROM Contain INNER JOIN Photo ON Contain.picid=Photo.picid WHERE albumid=''' + "'" + albumid + "'"
	cursor.execute(query)
	pics = cursor.fetchall()
	query = '''SELECT title FROM Album WHERE albumid=''' + "'"+albumid+"'"
	cursor.execute(query)
	album_name = cursor.fetchall()
	query = '''SELECT username FROM Album WHERE albumid=''' + "'"+albumid+"'"
	cursor.execute(query)
	album_owner = cursor.fetchall()
	username = ""

	#query = '''SELECT picid FROM Contain WHERE albumid=''' + "'" + albumid + "'"
	#cursor.execute(query)
	#pics_in_album = cursor.fetchall()
	#pics = []
	#for picid in pics_in_album:
		#query = '''SELECT url FROM Photo WHERE picid=''' + "'" + picid + "'"
		#cursor.execute(query)
		#picsssss = cursor.fetchall()
		#pics.append(picsssss[0])

#	return render_template("album.html", pics = pics, albumid = albumid, album_name = album_name, album_owner = album_owner, access = access)

	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		albumid = request.args.get('id')
		cursor = mysql.connection.cursor()
		#import pdb; pdb.set_trace()
		query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
		#query = '''SELECT Contain.*, Photo.url FROM Contain INNER JOIN Photo ON Contain.picid=Photo.picid WHERE albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		pics = cursor.fetchall()
		access = False
		if username == album_owner[0][0]:
			access = True
		return render_template("album.html", pics = pics, albumid = albumid, username = username, album_name = album_name, album_owner = album_owner, access = access, login = "yes")

	access = False
	if username == album_owner[0][0]:
		access = True

	return render_template("login.html", album_name = album_name, album_owner = album_owner, access = access, login = "no")

	#return render_template("album.html", albumid = albumid, pics = pics, pics_in_album = pics_in_album)

@app.route('/ilrj0i/pa2/pic')
def pic():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
		return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		requestpicid = request.args.get('id')
		albumid = request.args.get('albid')
		#import pdb; pdb.set_trace()

		"""
		navigation = request.args.get('doit')

		if navigation == "true":
			previousreq = request.args.get('prev')
			nextreq = request.args.get('nex')

			cursor = mysql.connection.cursor()
			seqnumquery = '''SELECT sequencenum FROM Contain INNER JOIN Photo ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumID + "'" + AND Photo.picid = ''' + "'"
			sequencenumreturn = cursor.fetchall()

			if previousreq == "-1":
		"""

		cursor = mysql.connection.cursor()
		query = '''SELECT * FROM Photo WHERE picid =''' + "'" + requestpicid + "'"
		cursor.execute(query)

		picarr = cursor.fetchall()
		#return str(picarr)
		return render_template("pic.html", picarr = picarr, albumid = albumid, username = username, login = "yes")
	return render_template("login.html", login = "no")

	picarr = cursor.fetchall()

	query = '''SELECT username FROM Album WHERE albumid=''' + "'"+albumid+"'"
	cursor.execute(query)
	album_owner = cursor.fetchall()
	current_user = session['username']

	#import pdb; pdb.set_trace()
	access = False
	if current_user == album_owner[0][0]:
		access = True
		caption = request.form['caption']
		if (len(caption) > 0):
			lastupdated = str(datetime.now().date())
			query = '''UPDATE Album SET lastupdated=''' + "'"+lastupdated+"'" + "'WHERE albumid ='" + "'"+albumid+"'"
			cursor.execute(query)
			query = '''UPDATE Contain SET caption=''' + "'"+caption+"'" + "'WHERE albumid='" + "'"+albumid+"'"
			cursor.execute(query)
			mysql.connection.commit()

	query = '''SELECT title FROM Album WHERE albumid=''' + "'"+albumid+"'"
	cursor.execute(query)
	album_name = cursor.fetchall()

	query = '''SELECT caption FROM Contain WHERE picid=''' + "'"+requestpicid+"'"
	cursor.execute(query)
	caption = cursor.fetchall

	#return str(picarr)
	return render_template("pic.html", picarr = picarr, albumid = albumid, album_name = album_name, username = album_owner, access = access, caption = caption)
	#return render_template("test.html", picarr = returnpic, albumid = albumID)

@app.route('/ilrj0i/pa2/albums/edit', methods=['POST'])
@requires_auth
def editalbums():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		if (request.form['op'] == 'add'):
			#import pdb; pdb.set_trace()
			created = str(datetime.now().date())
			##############################################datetime.datetime.now().date()?
			lastupdated = str(datetime.now().date())
			username = request.form['username']
			title = request.form['title']
			access = request.form['access']
			cursor = mysql.connection.cursor()
			query = '''INSERT INTO Album (title, created, lastupdated, username, access) VALUES (''' + "'" + title + "', '" + created + "', '" + lastupdated + "', '" + username + "', '" + access + "')"
			cursor.execute(query)
			mysql.connection.commit()
			query = '''SELECT * FROM Album WHERE username=''' + "'" + username + "'"
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("editalbums.html", albums = albums, username = username, login = "yes")
			#return render_template("test.html", query = query)

			######DELETE FROM OTHER TABLES
		if (request.form['op'] == 'delete'):
			albumid = request.form['albumid']
			username = request.form['username']
			cursor = mysql.connection.cursor()
			query = '''DELETE FROM Album WHERE albumid=''' + "'" + albumid + "'" #and user?
			cursor.execute(query)	#string stuff
			mysql.connection.commit()
			query = '''SELECT * FROM Album WHERE username=''' + "'" + username + "'"
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("editalbums.html", albums = albums, username = username, login = "yes")
	return render_template("login.html", login = "no")

@app.route('/ilrj0i/pa2/albums/edit', methods=['GET'])
@requires_auth
def vieweditalbums():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		cursor = mysql.connection.cursor()
		query = '''SELECT * FROM Album WHERE username=''' + "'" + username + "'"
		cursor.execute(query)
		albums = cursor.fetchall()
		return render_template("editalbums.html", albums = albums, username = username, login = "yes")
	return render_template("login.html", login = "no")


########################################
#definition to check for allowed extension/filetype
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#definition for the pic hashing function
def secure_filename(filename):
	#import pdb; pdb.set_trace()
	now = datetime.now()
	return (filename.rsplit('.', 1)[0] + "_" + str(now.year) + str(now.month) + str(now.day) + "_" + str(now.hour) + str(now.minute) + str(now.second))

@app.route('/ilrj0i/pa2/album/edit', methods=['POST'])
@requires_auth
def editalbum():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		albumid = request.form['albumid']
		cursor = mysql.connection.cursor()
		if (request.form['op'] == 'revokeaccess'):
			username = request.form['username']#############
			query = '''DELETE FROM AlbumAccess WHERE username=''' + "'" + username + "'"
			cursor.execute(query)
			mysql.connection.commit()

		if (request.form['op'] == 'addaccess'):
			username = request.form['username']################
			query = '''INSERT INTO AlbumAccess (albumid, username) VALUES (''' + "'" + albumid + "','" + username + "')"
			cursor.execute(query)
			mysql.connection.commit()

		if (request.form['op'] == 'delete'):
			returnpicid = request.form['picid']
			query = '''DELETE FROM Photo WHERE picid=''' + "'" + returnpicid + "'"#INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.picid=''' + "'" + picid + "'"#'''' AND Contain.albumid=''' + "'" + albumid + "'"
			cursor.execute(query)
			mysql.connection.commit()

		if (request.form['op'] == 'add'):
			file = request.files['file']
			#print file.filename
			if (file and allowed_file(file.filename)):
				#import pdb; pdb.set_trace()
				picid = str(secure_filename(file.filename))
				format = str(file.filename.rsplit('.', 1)[1])
				filename = str(picid + "." + format)
				file.save(os.path.join(UPLOAD_FOLDER, filename))
				url = str(picid + "." + format)
				date = str(datetime.now().date())
				query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
				cursor.execute(query)
				accessors = cursor.fetchall()				#print picid
				query = '''INSERT INTO Photo (picid, url, format, date) VALUES ('''+"'"+picid+"','"+url+"', '"+format+"', '"+date+"')"
				cursor.execute(query)
				select = '''SELECT sequencenum FROM Contain WHERE albumid =''' + "'"+albumid+"'"
				cursor.execute(select)
				#import pdb; pdb.set_trace()
				seqnum = cursor.fetchall()
				if not seqnum :
					nseqnum = [0]
				else :
					nseqnum = max(seqnum)
				sequencenum = nseqnum[0] + 1
				sequencenum = str(sequencenum)
				#import pdb; pdb.set_trace()
				query = '''INSERT INTO Contain (albumid, picid, sequencenum) VALUES ('''+"'"+albumid+"', '"+picid+"', '"+sequencenum+"')"
				cursor.execute(query)
				mysql.connection.commit()

		query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		accessors = cursor.fetchall()
		query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		pics = cursor.fetchall()
		return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors, login = "yes")
	return render_template("login.html", login = "no")



		#return render_template("test.html", picid = picid, albumid = albumid, pics = pics)
	#if request.form['op'] == 'add':
		################

@app.route('/ilrj0i/pa2/album/edit', methods=['GET'])
@requires_auth
def viewalbum():
	if 'username' in session:
		if datetime.now() - session['lastactivity'] > timedelta(minutes=5):
			####
			session.pop('username', None)
			session.pop('lastactivity', None)
			cursor = mysql.connection.cursor()
			query = '''SELECT * FROM Album WHERE access="public"'''
			cursor = mysql.connection.cursor()
			cursor.execute(query)
			albums = cursor.fetchall()
			return render_template("index.html", albums = albums, login = "no")
		session['lastactivity'] = datetime.now()
		username = session['username']
		albumid = request.args.get('id')
		cursor = mysql.connection.cursor()

		#access stuff
		query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		accessors = cursor.fetchall()

		query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		pics = cursor.fetchall()
		return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors, login = "yes")
	return render_template("login.html", login = "no")

	#return render_template("editalbum.html", pics = pics, pics_in_album = pics_in_album, albumid = albumid)

#app.secret_key = os.urandom(24)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.run(debug=True)
		# listen on external IPs
		#app.run(host='localhost', port=5636, port=5736, debug=True)

