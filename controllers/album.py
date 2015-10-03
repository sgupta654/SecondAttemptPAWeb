"""
from flask import Flask
from flask.ext.mysqldb import MySQL

app = Flask(__name__, template_folder='views')
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
mysql.init_app(app)
"""
"""from flask import *
from flask.ext.mysqldb import MySQL
from flask import current_app

album = Blueprint('album', __name__, template_folder='views')

app = Flask(__name__, template_folder='views', static_folder='images')
"""
"""
@album.route('/album')
def albumfunc():
	#import pdb; pdb.set_trace()
	albumid = request.args.get('id')
	cursor = mysql.connection.cursor()
	#import pdb; pdb.set_trace()
	cursor.execute('''SELECT picid FROM group36.Contain WHERE albumid = %s''', (albumid))
	pics_in_album = cursor.fetchall()
	pics = []
	for pic in pics_in_album :
		cursor.execute('''SELECT url FROM Photo WHERE picid = %s''', (pic))
		picsssss = cursor.fetchall()
		pics.append(picsssss[0])
#	return render_template("album.html", pics = pics)
	return render_template("album.html", albumid = albumid, pics = pics, pics_in_album = pics_in_album)


@app.route('/pic')
def pic():
	picid = request.args.get('id')
	#cur = mysql.connection.cursor()
	#cursor.execute('''SELECT * FROM Photo WHERE picid = ?''', picid)
	#pics = cursor.fetchall()
	return render_template("pic.html", picid = picid)


if __name__ == "__main__":
	app.run()

"""