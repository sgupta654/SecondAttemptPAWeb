"""
from flask import *
from flask.ext.mysqldb import MySQL

app = Flask(__name__, template_folder='views')
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
mysql.init_app(app)
"""
"""
from flask import *
from flask.ext.mysqldb import MySQL
from flask import current_app

editalbums = Blueprint('editalbums', __name__, template_folder='views')

app = Flask(__name__, template_folder='views')
"""
"""
@app.route('/albums/edit')
def editalbums():
	if request.form['op'] == 'add':
		username = request.form['username']
		title = request.form['title']
		cursor = mysql.connection.cursor()
		cursor.execute('''INSERT INTO group36.Album VALUES (albumid, title, created, lastupdated, username)''') #values???? string stuff
		######DELETE FROM OTHER TABLES
	if request.form['op'] == 'delete':
		albumid = request.form['albumid']
		cursor - mysql.connection.cursor()
		cursor.execute('''DELETE FROM group36.Album WHERE albumid = albumid''')	#string stuff
	#username = request.args.get('username')
	#cursor = mysql.connection.cursor()
	#cursor.execute('''SELECT * FROM group36.Album WHERE username = %s''', (username))
	#albums = cursor.fetchall()
	#return render_template("editalbums.html", albums = albums, username = username)
	return

@app.route('/album/edit')
def editalbum():
	if request.form['op'] == 'delete':
		picid = request.form['picid']
		cursor = mysql.connection.cursor()
		cursor.execute('''DELETE FROM group36.Photos WHERE picid = picid''') #string
	#if request.form['op'] == 'add':
		################
	albumid = request.args.get('albumid')
	cursor = mysql.connection.cursor()
	cursor.execute('''SELECT * FROM group36.Contain WHERE albumid = %s''', albumid)
	pics = cursor.fetchall()
#	return render_template("album.html", pics = pics)
	return render_template("editalbum.html", pics = pics, albumid = albumid)

"""

