from flask import *
from flask.ext.mysqldb import MySQL

app = Flask(__name__, template_folder='views')
mysql = MySQL()
app.config['MYSQL_USER'] = 'group36'
app.config['MYSQL_PASSWORD'] = 'GOOCH'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'group36'
mysql.init_app(app)

@app.route('/')
def homepage():
	return render_template("index.html")

@app.route('/album')
def album():
	albumid = request.args.get('id')
	cursor = mysql.connection.cursor()
	cursor.execute('''SELECT picid FROM group36.Contain WHERE albumid = ?''', albumid)
	pics_in_album = cursor.fetchall()
	cursor.execute('''SELECT * FROM Photo WHERE picid = ?''', pics_in_album)
	pics = cursor.fetchall()
#	return render_template("album.html", pics = pics)
	return render_template("index.html", albumid = albumid, pics_in_album = pics_in_album)


@app.route('/pic', methods=['GET'])
def pic():
	picid = request.args.get('id')
	cur = mysql.connection.cursor()
	cursor.execute('''SELECT * FROM Photo WHERE picid = ?''', picid)
	pic = cursor.fetchall()
	return render_template("pic.html", pic = pic)


if __name__ == "__main__":
	app.run()
