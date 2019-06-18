"""
Routes and views for the flask application.
"""


from datetime import datetime
from flask import *
from Image_Detection import app
from Image_Detection.predict import *
import os
import requests
from werkzeug.utils import secure_filename


app.secret_key = 'vzP7jO/N4kXnLsutcCRe6mYBFoJnLevSNbf0uB6J'


@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'home.html',
        title = 'Home Page',
        year = datetime.now().year,
        prediction = '',
        score = ''
    )


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    imagePath = ''
    prediction = ''
    score = 0

    if request.method == 'POST':
        imageUrl = request.form.get('imageUrl', '')
        if imageUrl == '': 
            imageUrl = request.args.get('imageUrl', '')

        if imageUrl == '':
            # check if the post request has the file part or not
            if 'photo' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['photo']

            # if user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('Image_Detection/static/input', filename))
                imagePath = '/static/input/' + filename
                prediction, score = predictVGG('Image_Detection' + imagePath)
        else:
            r = requests.get(imageUrl)
            filename = secure_filename(imageUrl)
            f = open(os.path.join('Image_Detection/static/input', filename), "wb")
            f.write(r.content)
            imagePath = '/static/input/' + filename
            prediction, score = predictVGG('Image_Detection' + imagePath)

    return render_template(
        'home.html',
        title = 'Home Page',
        year = datetime.now().year,
        imagePath = imagePath,
        prediction = prediction,
        score = score
    )