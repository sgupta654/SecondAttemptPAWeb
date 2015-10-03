"""
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')

@pic.route('/pic')
def pic_route():
	return render_template("pic.html")
"""