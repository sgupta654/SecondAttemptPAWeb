"""
from flask import Flask
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

albums = Blueprint('albums', __name__, template_folder='views')

app = Flask(__name__, template_folder='views')

#main = Blueprint('main', __name__, template_folder='views')
"""
"""
@albums.route('/albums')
def main_route():
	username = request.args.get('username')
	cursor = mysql.connection.cursor()
	cursor.execute('''SELECT * FROM group36.Album WHERE username = %s''', (username))
	albums = cursor.fetchall()
	return render_template("albums.html", albums = albums)


"""