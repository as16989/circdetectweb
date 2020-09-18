from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file
import os
import cv2
import numpy as np
import math
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    #files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html')

@app.route('/uploadfile', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(filepath)
        detector(filepath)
    return redirect(url_for('result'))

@app.route('/uploadfromurl', methods=['POST'])
def upload_from_url():
    print('TESTINGTON MUTHAFUCKA')

    uploaded_url = request.form['url']
    print(uploaded_url)
    path = 'uploads/' + uploaded_url.split('/')[-1]
    print(path)
    uploaded_file, headers = urllib.request.urlretrieve(uploaded_url, path)
    print(uploaded_file)
    filename = secure_filename(uploaded_file)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
        print('AOSIDJOASIDJ' + filepath)
        detector(uploaded_file)

    return redirect(url_for('result'))

@app.route('/result')
def result():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('result.html', files=files)

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename, as_attachment=True)

@app.route('/downloads/<filename>')
def download(filename):
    print('MY HEAD')
    print(os.path.join(app.config['UPLOAD_PATH'],filename))
    return send_file(os.path.join(app.config['UPLOAD_PATH'],filename), filename, as_attachment=True)

#------------------------------------------------------------

def detector(img_path):
    print('YOUR HEAD' + img_path)
    imgcolor = cv2.imread(img_path)
    #print('YOUR HEAD after imread' + imgcolor)
    img = cv2.cvtColor(imgcolor, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("test.jpg", img)
    img = cv2.equalizeHist(img)

    #Canny

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
    distMax = round(math.sqrt(height**2 + width**2))
    thetaVals = np.arange(-90,89)
    rhoVals   = np.arange(-distMax,distMax)
    acc       = np.zeros((rhoVals.size, thetaVals.size), dtype=np.uint64)

    accCirc = np.zeros((img.shape[0], img.shape[1], distMax))
    lower = 20
    higher = 150

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

    found = False

    for y in range(height):
        for x in range(width):
            for r in range(20,150,1):
                if accCirc[y,x,r] >= thresholdCirc:
                    if (not(abs(x-tempx) < 10 or abs(y-tempy) < 10)):
                        found = True
                        tempx=x
                        tempy=y
                        #cv2.circle(imgcolor, (x,y), r, color=(255,255,0), thickness = 2)
                        crop_img = imgcolor[y-r:y+r+1, x-r:x+r+1]
                        path = './uploads'
                        cv2.imwrite(os.path.join(path, 'cropped' + str(x) + 'by' + str(y) + '.jpg'), crop_img)
                        circles.append((x,y,r))
                        print('Saved to ' + "cropped" + str(x) + "by" + str(y) + ".jpg")

    if (found):
        print('Finished!')
    else:
        print('No circular objects found in image.')
