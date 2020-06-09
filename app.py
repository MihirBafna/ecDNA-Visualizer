from flask import Flask, render_template, redirect, request, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/input')
def input():
    return render_template('input.html')


app.config["IMAGE_UPLOADS"] = "static/img"
app.config["ALLOWED_INPUT_IMAGE_EXTENSIONS"] = ["TIF", "TIFF"]
app.config["ALLOWED_OUTPUT_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "TIF", "TIFF"]

def imglist(filepath):  # get image data after ecSeg is run
    print(os.listdir(filepath))
    imagelist = []
    for file in os.listdir(filepath):
        if file.endswith(".png"):
            imagelist.append(file)
    return(imagelist)

def allowed_image(filename, inout):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if inout and ext.upper() in app.config["ALLOWED_INPUT_IMAGE_EXTENSIONS"]:
            return True
    elif not inout and ext.upper() in app.config["ALLOWED_OUTPUT_IMAGE_EXTENSIONS"]:
            return True
    else:
        return False

@app.route('/uploadInput', methods=["GET","POST"])
def uploadInput():
    if request.method == "POST":
        if request.files:
            folder = request.files.getlist("input-folder-2[]")
            timestamped = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            folderpath = os.path.join(app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, "orig")
            os.makedirs(folderpath)
            for file in folder:
                print(file.filename)
                if file.filename == "":
                    print("ERROR: File has no filename")
                    return redirect(request.url)
                if allowed_image(file.filename, True):
                    path = os.path.join(
                        app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, file.filename)
                    file.save(path)
                    print("Image saved" +path)
                else:
                    print("not allowed")
    # RUN ECSEG HERE
    # *
    # *
    # *
    #
    #     imagelist = imglist((os.path.join(app.config["IMAGE_UPLOADS"], "ecSegOutput"+timestamped)))
    # return render_template('visualize.html'+'/'+str(imagelist[0]))
    return redirect(request.url)

@app.route('/uploadecSeg', methods=["GET","POST"])
def uploadecSeg():
    if request.method == "POST":
        if request.files:
            folder = request.files.getlist("input-folder-3[]")
            timestamped = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            folderpath = os.path.join(
                app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, "orig")
            os.makedirs(folderpath)
            os.mkdir(os.path.join(
                app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, "dapi2"))
            os.mkdir(os.path.join(
                app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, "ecSeg"))
            for file in folder:
                print(file.filename)
                if file.filename == "":
                    print("ERROR: File has no filename")
                    return redirect(request.url)
                if allowed_image(file.filename, False):
                    path = os.path.join(
                        app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, '/'.join(file.filename.split('/')[1:]))
                    file.save(path)
                    print(file.filename+" saved")
                else:
                    print("not allowed")
    path = os.path.join(app.config["IMAGE_UPLOADS"], "ecSegOutput", timestamped, "orig")+'/'
    session['folder']=timestamped
    session['imagelist'] = imglist(path)
    session['imagename'] = session['imagelist'][0]
    return redirect('/visualize')


@app.route('/visualize/<img>')
def newimgselect(img):
    session['imagename'] = img
    return redirect('/visualize')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html', images=session['imagelist'], folder=session['folder'], imgname=session['imagename'])


@app.route('/mpDetector')
def mpDetector():
    return render_template('mpDetector.html')

if __name__ == "__main__":
    app.run(debug=True)
