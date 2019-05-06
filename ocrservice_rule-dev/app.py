#!flask/bin/python
from flask import abort, jsonify, request, Flask, Response,make_response, redirect
import os
import cv2
import subprocess
from werkzeug.utils import secure_filename
import json
import pytesseract
import attr
import numpy as np
import math
from scipy import ndimage
from Business import Business
from flask import render_template

#my module
import repository as repo
from viewmodels.IndexVM import IndexVM
from viewmodels.AboutVM import AboutVM 
from viewmodels.CreateAppVM import CreateAppVM

app = Flask(__name__)

@app.route("/getbyappid")
def get_by_app_id():
    pass

@app.route("/getbyform", methods = ["GET", "POST"])
def get_by_form():
    if "file" not in request.files:
        abort(400)
    conf_val = 0.75
    if "conf_val" in request.form:
        conf_val = float(request.form["conf_val"])
    features = request.form.getlist("features")
    tmp_features = []
    for fea in features:
        if len(fea) != 0:
            tmp_features.append(fea)
    features = tmp_features
    file = request.files["file"]
    
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lang = "vie"
    if "lang" in request.form:
        lang = request.form["lang"]

    res = {}
    if "features" not in request.form or len(features) == 0:
        return pytesseract.image_to_string(img, lang = lang).replace("\n", "<br>")

    rules = request.form.getlist("rules")

    if "split" in rules:
        h, w = img.shape
        blocks1 = pytesseract.image_to_string(img[0:int(h), 0:w//2], lang = lang).split('\n')
        blocks2 = pytesseract.image_to_string(img[0:int(h), w//2:], lang = lang).split('\n')
        res1 = Business.get_result(features, blocks1, rules, conf_val)
        res2 = Business.get_result(features, blocks2, rules, conf_val)
        res1.update(res2)
        res = res1
    else:
        blocks = pytesseract.image_to_string(img, lang = lang).split("\n")
        res = Business.get_result(features, blocks, rules, conf_val)
    json_string = json.dumps(res, ensure_ascii = False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response

@app.route("/")
def index():
    model = IndexVM()
    app_id = request.args.get("app_id", "")
    app = repo.get_app(app_id)
    if app != None:
        model.set_features(app["features"])
        if "rules" in app:
            model.set_rules(app["rules"])
    else:
        model.features = []
    return render_template("index.html", model = model)


@app.route("/apps/add")
def add_app():
    return render_template("add_app.html", model = CreateAppVM())

@app.route("/apps/create", methods = ["POST", "GET"])
def create_app():
    rules = request.form.getlist("rules")
    features = request.form.getlist("features")
    name = request.form["name"]
    app = {"rules": rules, "features": features, "name": name}
    repo.add_app(app)
    return redirect("/")

@app.route("/about")
def about_us():
    return render_template("about.html", model = AboutVM())

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
    