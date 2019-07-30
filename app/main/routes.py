from flask import render_template, request, session, redirect, url_for
from bson import ObjectId
from bcrypt import hashpw, gensalt
from datetime import datetime

from app.config import S3_LOCATION, API_ADDRESS, PORT
from app.main.database import DB
from app.main import bp
from app.models.photo import Photo
from app.models.user import User
from app.helpers import agent_s3


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def index():
    if 'email' in session:
        print(request.args.get("sort"))
        photos_collection = DB.collection("photos")
        if photos_collection.count() == 0:
            return render_template('album.html', total=0, to_review=False)
        # FIXME: move to database class
        photos_id = photos_collection.find({'accepted': True}).sort('created_at', -1)
        if photos_id.count() == 0:
            return render_template('album.html', total=0, to_review=False)
        api_address = str(API_ADDRESS) + ':' + str(PORT)
        return render_template('album.html', photos=photos_id, api_address=api_address, storage_url=str(S3_LOCATION),
                               total=photos_id.count(), to_review=False)
    return render_template('sign-in.html')


@bp.route('/login', methods=['POST'])
def login():
    (success, resp) = DB.validate("users", {'email': request.form['email'], 'password': request.form['password']})
    if success:
        session['email'] = request.form['email']
        return redirect(url_for('main.index', user_id=resp))
    return render_template('sign-in.html', error=resp)


@bp.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('sign-in.html')


@bp.route('/pending')
def pending():
    collection = DB.collection("photos")
    photos = collection.find({'accepted': False}).sort('_id', 1)
    count = photos.count()
    return render_template('album.html', photos=photos, storage_url=str(S3_LOCATION), total=count, to_review=True)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        hashpass = hashpw(request.form['password'].encode('utf-8'), gensalt())
        user = User(name, email, hashpass)
        success = user.insert()
        if success:
            return redirect(url_for('main.index'))
    return render_template('sign-up.html', error=error)


# FIXME: Deprecated! Only for test purposes
@bp.route('/upload', methods=['POST'])
def upload():
    if 'new_photo' in request.files:
        photo_data = request.files['new_photo']
        new_photo = Photo(data=photo_data)
        success = new_photo.insert()
        if success:
            return redirect(url_for('main.index'))
    return 'Done!'


@bp.route('/u', methods=['POST'])
def upload_photo():
    if 'user_photo' not in request.files:
        # FIXME: throw an error to inform the user
        pass
    file_obj = request.files['user_photo']
    if file_obj.filename == '':
        # FIXME: throw an error to inform the user
        pass
    if file_obj and allowed_file(file_obj.filename):
        photo_obj = Photo(data=file_obj)
        success = photo_obj.insert()
        if success:
            file_obj.filename = photo_obj.filename()
            output = agent_s3.upload_file_to_s3(file_obj)
            # Link for the image in S3
            return redirect(url_for('main.index'))
    # FIXME: throw an error to inform the user
    return 'TODO!'


@bp.route('/review/<action>/<filename>')
def review(action, filename):
    if action == "accept":
        print("file " + filename + " accepted")
        # FIXME: if the object isn't found redirect adding an error parameter
        DB.update("photos", {"filename": filename}, {'$set': {"accepted": True}})
    elif action == "reject":
        print("file " + filename + " rejected")
        # FIXME: if the object isn't found redirect adding an error parameter
        DB.delete("photos", {"filename": filename})
    return redirect(url_for('main.pending'))


@bp.route('/like/<file_id>')
def like(file_id):
    # FIXME: if the object isn't found redirect adding an error parameter
    DB.update("photos", {"_id": ObjectId(file_id)}, {'$inc': {"counter_like": 1}})
    # FIXME: add some return
    return {}
