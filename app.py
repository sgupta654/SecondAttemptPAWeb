from flask import *
from flask_mysqldb import MySQL
from datetime import datetime

import os.path
#import os.urandom

#path to the images folder to store uploaded pictures
UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'bmp', 'gif'])


app = Flask(__name__, template_folder='views', static_folder='images')
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'my_password'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'group36pa2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql.init_app(app)

@app.route('/ilrj0i/pa1/')
def main_route():

	# The next line gets the global application object
	#app = current_app._get_current_object()
	# The following code gets the mysql object from app and creates a connection/cursor
	#connection = app.mysql.connect()
	"""
	cursor = mysql.connection.cursor()
	cursor.execute('''SELECT * FROM User''')
	users = cursor.fetchall()
	return render_template("index.html", users = users)
	"""


	cursor = mysql.connection.cursor()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	if 'username' in session:
		if datetime.datetime.now() - session['lastactivity'] > datetime.timedelta(minutes=5):
			##############logout
			logout()
		session['lastactivity'] = datetime.datetime.now()
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



@app.route('/ilrj0i/pa1/user', methods=['GET'])
def signup():
	if 'username' in session:
		if datetime.datetime.now() - session['lastactivity'] > datetime.timedelta(minutes=5):
			####
			logout()
		session['lastactivity'] = datetime.datetime.now()
		username = session['username']
		return render_template("edituser.html", username = username, login = "yes")
	return render_template("user.html", login = "no")

@app.route('/ilrj0i/pa1/user', methods=['POST'])
def createaccount():
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
		return render_template("user.html")
	query = '''INSERT INTO User VALUES (''' + "'" + username + "', '" + firstname + "', '" + lastname + "', '" + password + "', '" + email + "')"
	cursor.execute(query)
	mysql.connection.commit()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums)


@app.route('/ilrj0i/pa1/user/edit', methods=['GET'])
def edituserget():
	return render_template("edituser.html", username = username)

@app.route('/ilrj0i/pa1/user/edit', methods=['POST'])
def edituserpost():
	username = request.form['username']
	firstname = request.form['firstname']
	lastname = request.form['lastname']
	password = request.form['password']
	email = request.form['email']
	cursor = mysql.connection.cursor()
	query = '''UPDATE USER SET firstname=''' + "'" + firstname + "', lastname=" + "'" + lastname + "', password=" + "'" + password + "', email=" + "'" + email + "' WHERE username=" + "'" + username + "'"
	cursor.execute(query)
	mysql.connection.commit()
	return render_template("edituser.html", username = username)

@app.route('/ilrj0i/pa1/user/login', methods=['GET'])
def userloginget():
	return render_template("login.html")

@app.route('/ilrj0i/pa1/user/login', methods=['POST'])
def userloginpost():
	session['username'] = request.form['username']
	session['lastactivity'] = datetime.now().time()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums)

@app.route('/ilrj0i/pa1/user/delete', methods=['POST'])
def deleteuser():
	username = request.form['username']
	cursor = mysql.connection.cursor()
	query = '''DELETE FROM User WHERE username=''' + "'" + username + "'"
	cursor.execute(query)
	mysql.connection.commit()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums)

@app.route('/ilrj0i/pa1/user/logout')
def logout():
	session.pop('username', None)
	session.pop('lastactivity', None)
	cursor = mysql.connection.cursor()
	query = '''SELECT * FROM Album WHERE access="public"'''
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("index.html", albums = albums)

@app.route('/ilrj0i/pa1/albums')
def albumsss():
	username = request.args.get('username')
	cursor = mysql.connection.cursor()
	query = '''SELECT * FROM Album WHERE username=''' + "'" + username + "'"
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("albums.html", albums = albums, username = username)

@app.route('/ilrj0i/pa1/album')
def albumfunc():
	#import pdb; pdb.set_trace()
	albumid = request.args.get('id')
	cursor = mysql.connection.cursor()
	#import pdb; pdb.set_trace()
	query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
	#query = '''SELECT Contain.*, Photo.url FROM Contain INNER JOIN Photo ON Contain.picid=Photo.picid WHERE albumid=''' + "'" + albumid + "'"
	cursor.execute(query)
	pics = cursor.fetchall()
	#query = '''SELECT picid FROM Contain WHERE albumid=''' + "'" + albumid + "'"
	#cursor.execute(query)
	#pics_in_album = cursor.fetchall()
	#pics = []
	#for picid in pics_in_album:
	#	query = '''SELECT url FROM Photo WHERE picid=''' + "'" + picid + "'"
	#	cursor.execute(query)
	#	picsssss = cursor.fetchall()
	#	pics.append(picsssss[0])

	return render_template("album.html", pics = pics, albumid = albumid)
	#return render_template("album.html", albumid = albumid, pics = pics, pics_in_album = pics_in_album)

@app.route('/ilrj0i/pa1/pic')
def pic():
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
	return render_template("pic.html", picarr = picarr, albumid = albumid)
	#return render_template("test.html", picarr = returnpic, albumid = albumID)

@app.route('/ilrj0i/pa1/albums/edit', methods=['POST'])
def editalbums():
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
		return render_template("editalbums.html", albums = albums, username = username)
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
		return render_template("editalbums.html", albums = albums, username = username)
	#username = request.args.get('username')
	#cursor = mysql.connection.cursor()
	#cursor.execute('''SELECT * FROM group36.Album WHERE username = %s''', (username))
	#albums = cursor.fetchall()
	#return render_template("editalbums.html", albums = albums, username = username)

@app.route('/ilrj0i/pa1/albums/edit', methods=['GET'])
def vieweditalbums():
	username = request.args.get('username')
	cursor = mysql.connection.cursor()
	query = '''SELECT * FROM Album WHERE username=''' + "'" + username + "'"
	cursor.execute(query)
	albums = cursor.fetchall()
	return render_template("editalbums.html", albums = albums, username = username)

########################################
#definition to check for allowed extension/filetype
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#definition for the pic hashing function
def secure_filename(filename):
	#import pdb; pdb.set_trace()
	now = datetime.now()
	return (filename.rsplit('.', 1)[0] + "_" + str(now.year) + str(now.month) + str(now.day) + "_" + str(now.hour) + str(now.minute) + str(now.second))

@app.route('/ilrj0i/pa1/album/edit', methods=['POST'])
def editalbum():
	if (request.form['op'] == 'revokeaccess'):
		albumid = request.form['albumid']
		username = request.form['username']
		cursor = mysql.connection.cursor()
		query = '''DELETE FROM AlbumAccess WHERE username=''' + "'" + username + "'"
		cursor.execute(query)
		mysql.connection.commit()
		query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		accessors = cursor.fetchall()
		query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		pics = cursor.fetchall()
		return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors)

	if (request.form['op'] == 'addaccess'):
		albumid = request.form['albumid']
		username = request.form['username']
		cursor = mysql.connection.cursor()
		query = '''INSERT INTO AlbumAccess (albumid, username) VALUES (''' + "'" + albumid + "','" + username + "')"
		cursor.execute(query)
		mysql.connection.commit()
		query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		accessors = cursor.fetchall()
		query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		pics = cursor.fetchall()
		return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors)

	if (request.form['op'] == 'delete'):
		albumid = request.form['albumid']
		returnpicid = request.form['picid']
		cursor = mysql.connection.cursor()
		query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		accessors = cursor.fetchall()
		query = '''DELETE FROM Photo WHERE picid=''' + "'" + returnpicid + "'"#INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.picid=''' + "'" + picid + "'"#'''' AND Contain.albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		mysql.connection.commit()
		query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
		cursor.execute(query)
		pics = cursor.fetchall()
		return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors)

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
			cursor = mysql.connection.cursor()

			query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
			cursor.execute(query)
			accessors = cursor.fetchall()

			albumid = str(request.form['albumid'])
			#print picid
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
			query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
			cursor.execute(query)
			pics = cursor.fetchall()
			#import pdb; pdb.set_trace()
			mysql.connection.commit()
			return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors)


		#return render_template("test.html", picid = picid, albumid = albumid, pics = pics)
	#if request.form['op'] == 'add':
		################

@app.route('/ilrj0i/pa1/album/edit', methods=['GET'])
def viewalbum():
	albumid = request.args.get('id')
	cursor = mysql.connection.cursor()

	#access stuff
	query = '''SELECT username FROM AlbumAccess WHERE albumid=''' + "'" + albumid + "'"
	cursor.execute(query)
	accessors = cursor.fetchall()

	query = '''SELECT * FROM Photo INNER JOIN Contain ON Contain.picid=Photo.picid WHERE Contain.albumid=''' + "'" + albumid + "'"
	cursor.execute(query)
	pics = cursor.fetchall()
	#query = '''SELECT * FROM Contain WHERE albumid=''' + "'" + albumid + "'"
	#cursor.execute(query)
	#pics_in_album = cursor.fetchall()
	#pics = []
	#for pic in pics_in_album :
	#	query = '''SELECT url FROM Photo WHERE picid=''' + "'" + pic[1] + "'"
	#	cursor.execute(query)
	#	picsssss = cursor.fetchall()
	#	pics.append(picsssss[0])
	return render_template("editalbum.html", pics = pics, albumid = albumid, accessors = accessors)
	#return render_template("editalbum.html", pics = pics, pics_in_album = pics_in_album, albumid = albumid)

#app.secret_key = os.urandom(24)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.run(debug=True)
		# listen on external IPs
		#app.run(host='localhost', port=5636, port=5736, debug=True)

