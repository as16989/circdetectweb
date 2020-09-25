from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file, jsonify
from flask_jsglue import JSGlue
import os
import cv2
import numpy as np
import math
import urllib.request
import requests
import validators
from werkzeug.utils import secure_filename

app = Flask(__name__)
jsglue = JSGlue(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_HEADERS'] = ['image/png', 'image/jpg', 'image/jpeg']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    delete_existing_files();
    return render_template('index.html')

@app.route('/uploadfile', methods=['POST'])
def upload_files():
    delete_existing_files();
    if 'file' in request.files:
        print('doing the choose file ting')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(filepath)
            return detector(filepath)

    elif 'url' in request.form:
        delete_existing_files();
        print('doing the URL ting')
        uploaded_url = request.form['url']
        if (not(validators.url(uploaded_url))):
            return jsonify(paths=['nothing'])
        uploaded_splitted = uploaded_url.split('/')[-1]
        path = 'uploads/' + uploaded_splitted
        print(path)
        filename = secure_filename(uploaded_splitted)
        if filename != '':
            r = requests.get(uploaded_url)
            if r.headers['content-type'] not in app.config['UPLOAD_HEADERS']:
                print('filetype not supported')
                return jsonify(paths=['nothing'])
            with open(path, 'wb') as file:
                file.write(r.content)
            return detector(path)

    return jsonify(paths=['nothing'])

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename, as_attachment=True)

@app.route('/downloads/<filename>')
def download(filename):
    print('MY HEAD')
    print(os.path.join(app.config['UPLOAD_PATH'],filename))
    return send_file(os.path.join(app.config['UPLOAD_PATH'],filename), filename, as_attachment=True)

#------------------------------------------------------------

def delete_existing_files():
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        filename2 = os.path.join(app.config['UPLOAD_PATH'],filename)
        if os.path.exists(filename2):
            os.remove(filename2)
        else:
            print("The file " + filename + " does not exist")

def detector(img_path):
    print('YOUR HEAD' + img_path)
    imgcolor = cv2.imread(img_path)
    img = cv2.cvtColor(imgcolor, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)

    blur = cv2.blur(img,(3,3))
    edges = cv2.Canny(img,50,150)
    cv2.imwrite('cannypy.jpg',edges)

    gxKernel = np.array([[1.0,0.0,-1.0],[2.0,0.0,-2.0],[1.0,0.0,-1.0]])
    gyKernel = np.array([[1.0,2.0,1.0],[0.0,0.0,0.0],[-1.0,-2.0,-1.0]])

    gx = cv2.filter2D(blur, 6, gxKernel)
    gy = cv2.filter2D(blur, 6, gyKernel)

    graddir = cv2.phase(gy,gx)
    graddirnorm = cv2.normalize(graddir, None, 0, 360, norm_type=cv2.NORM_MINMAX, dtype=0)
    cv2.imwrite('dirpy.jpg',graddirnorm)

    height = np.size(img, 0)
    width = np.size(img, 1)

    print('height ' + str(height) + ' width ' + str(width))

    distMax = round(math.sqrt(height**2 + width**2))
    thetaVals = np.arange(-90,89)
    rhoVals   = np.arange(-distMax,distMax)
    acc       = np.zeros((rhoVals.size, thetaVals.size), dtype=np.uint64)

    accCirc = np.zeros((img.shape[0], img.shape[1], distMax))
    lower = 20
    higher = np.minimum(width,height)

    print('Generating Circle Hough Space...')

    for y in range(height):
        for x in range(width):
            if edges[y,x]== 255:
                for r in range(lower,higher):
                    a = round(abs((y - r * math.cos(graddir[y,x]))))
                    b = round(abs((x - r * math.sin(graddir[y,x]))))
                    if a < img.shape[0] and a > -img.shape[0]:
                        if b < img.shape[1] and b > -img.shape[1]:
                            accCirc[a,b,r] += 1

    thresholdCirc = round(np.amax(accCirc) * 0.9)
    circles = []
    tempx=tempy=0

    print('Cropping Image...')

    resultArray = []

    for y in range(height):
        for x in range(width):
            for r in range(lower,higher,1):
                if accCirc[y,x,r] >= thresholdCirc:
                    if (not(abs(x-tempx) < 10 or abs(y-tempy) < 10) and x > r and y > r):
                        tempx=x
                        tempy=y
                        print('a circle was found... apparently... at' + str(x) + ',' + str(y) + ' with radius ' + str(r))
                        crop_img = imgcolor[y-r:y+r+1, x-r:x+r+1]
                        path = './uploads'
                        finalpath = os.path.join(path, 'cropped' + str(x) + 'by' + str(y) + '.jpg')
                        cv2.imwrite(finalpath, crop_img)
                        resultArray.append(finalpath)
                        circles.append((x,y,r))
                        print('Saved to ' + "cropped" + str(x) + "by" + str(y) + ".jpg")

    if os.path.exists(img_path):
        os.remove(img_path)
    else:
        print("The file does not exist")

    return jsonify(paths=resultArray)
