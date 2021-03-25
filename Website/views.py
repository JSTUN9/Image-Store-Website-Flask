# store all the routes of the webserver
from . import db
from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from werkzeug.utils import secure_filename
from .models import Img
from flask_login import login_user, login_required, logout_user, current_user
import base64


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#define that this file is the blueprint of our webserver (stores all the url of our webserver)

views = Blueprint('views', __name__)

@views.route('/') #in the url, if ending is just / (means main homepage) we execute the home() function
@login_required
def home():
    return render_template("home.html", user=current_user)
    
    


@views.route('/upload', methods=['GET', 'POST'])
@login_required 
def upload():
    if request.method == 'POST':
        pic = request.files['pic']

        if not pic:
            return 'No pic uploaded', 400

        if pic and allowed_file(pic.filename):
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            user_id = current_user.id
            base_data=pic.read()
            base_data = base64.b64encode(base_data)
            base_data = base_data.decode("UTF-8")
            img = Img(img=pic.read(), name=filename, mimetype=mimetype,user_id=user_id,base_data=base_data)            
            db.session.add(img)
            db.session.commit()
            flash('Upload sucessful', category='success')
            return redirect(url_for('views.upload'))

        else:
            return 'not valid file format' # add a return button here    
    return render_template("upload.html", user=current_user)

 

@views.route('/two/')
def two():
    return "<h2>Test2<h2>"

