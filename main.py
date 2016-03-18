import pickle
import os
from flask import *
import requests
import numpy
from PIL import Image, ImageFilter
import functions
from werkzeug import secure_filename
import flask
import io, urllib2
import gzip
import pickle


def load_obj(name ):
    with open(name+'.pkl', 'rb') as f:
        return pickle.load(f)

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

colorDict = load_obj("static/colorDict_4colors")
dict_url_image = load_obj("static/dict_url_image")

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/api', methods=['GET'])
def apis():
    d = {"public_url":"not_provided"}
    if request.method == 'GET':
        try:
            url = request.args.get('url')
            filename = functions.modifyImage(url, dict_url_image, colorDict, api = True)
            d["public_url"] = "https://s3-eu-west-1.amazonaws.com/emojimosaic/emojifiedimages/" + filename
            return flask.jsonify(**d) 
        except AttributeError:
            pass
    return flask.jsonify(**d) 



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filename = "https://s3-eu-west-1.amazonaws.com/emojimosaic/emojifiedimages/puppy.png"
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("static/images/", filename))
            filename = "static/images/" + filename
            filename = functions.modifyImage(filename, dict_url_image, colorDict)

    return render_template('index.html', filename=filename)


if __name__ == "__main__":

    app.run(debug=True )