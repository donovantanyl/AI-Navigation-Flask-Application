import json
import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import bus_detection
import label_automation
from classes.lta_api import bus_order
from classes.roboflow_api import RoboflowAPI
import multiprocessing

app = Flask(__name__, template_folder='templates')
CORS(app, origins=["http://172.20.10.*","http://192.168.*","http://localhost:5000"])
app.debug = True

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
output_dir = os.path.join(app.instance_path, 'outputs')
os.makedirs(output_dir, exist_ok=True)
models_dir = os.path.join(app.instance_path, 'models')
os.makedirs(models_dir, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", )


@app.route("/bus_navigation")
def bus_navigation():
    return render_template("bus_navigation.html", )


@app.route("/start_bus_detection", methods=['GET', 'POST'])
def start_bus_detection():
    if request.method == "POST":
        bus_code = str(request.form.get("code"))
        print(bus_code)
        api_thread = multiprocessing.Process(target=bus_order, args=(bus_code, "8w9wm+lqSE+R720jfwR+Ew=="))
        detection_thread = multiprocessing.Process(target=bus_detection.run,
                                                   args=("instance/models/bus_v2.pt",0))
        #arg 0 for webcam, or put files e.g. instance/uploads/bus_vid_part2.mp4


        #api_thread.start()
        detection_thread.start()
    return jsonify(message="Success",
                   statusCode=200)


@app.route("/bus_result", methods=['GET', 'POST'])
def bus_result():
    json_file = open("live_data/bus_labels.json", "r")
    result = json.load(json_file)
    return jsonify(message="Success",
                   statusCode=200,
                   data=result)


@app.route("/training")
def training():
    return render_template("training.html", )


@app.route("/projects/<api_key>", methods=['GET', 'POST'])
def projects(api_key):
    rbf = RoboflowAPI(api_key)
    if request.method == "GET":
        list_projects = rbf.get_projects()
        return jsonify(message="Success",
                       statusCode=200,
                       data=list_projects)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "GET":  # Get all videos in the uploads folder
        vid_list = []
        for videos in os.listdir(uploads_dir):
            if videos.endswith(".mp4"):
                vid_list.append(videos)
        return jsonify(message="Success",
                       statusCode=200,
                       data=vid_list)

    if request.method == "POST":
        fd = request.form
        folder = fd.get("folder")
        api_key = fd.get("apiKey")
        project = fd.get("project")
        print(folder, api_key, project)
        rbf = RoboflowAPI(api_key)
        rbf.set_project(project)
        uploaded = rbf.upload_image(f"{output_dir}/{folder}")
        return jsonify(message="Success",
                       statusCode=200,
                       data=uploaded)


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        vid = request.form.get("vid")
        model_used = request.form.get("model")
        folder = label_automation.run(weights=f"instance/models/{model_used}", source=f"instance/uploads/{vid}")
        print(folder)
        return jsonify(message="Success",
                       statusCode=200,
                       data=folder)


@app.route("/models", methods=['GET', 'POST'])
def models():
    if request.method == "GET":  # Get all models in the models folder
        mod_list = []
        for m in os.listdir(models_dir):
            if m.endswith(".pt"):
                mod_list.append(m)
        return jsonify(message="Success",
                       statusCode=200,
                       data=mod_list)


if __name__ == "__main__":
    app.run()
