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

main = Blueprint('main', __name__, template_folder='views')



#main = Blueprint('main', __name__, template_folder='views')
"""
"""
@main.route('/')
def main_route():

	# The next line gets the global application object
	app = current_app._get_current_object()
	# The following code gets the mysql object from app and creates a connection/cursor
	connection = app.mysql.connect()
	cursor = connection.cursor()
	cursor.execute('''SELECT username FROM group36.User''')
	users = cursor.fetchall()
	return render_template("index.html", users = users)
"""