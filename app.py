from flask import Flask, render_template, request, jsonify
import bus_detection, label_automation
import os
from classes.roboflow_api import RoboflowAPI

app = Flask(__name__, template_folder='templates')
app.debug = True

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
output_dir = os.path.join(app.instance_path, 'outputs')
os.makedirs(output_dir, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", )


@app.route("/bus_navigation")
def bus_navigation():
    bus_detection.run()
    return render_template("bus_navigation.html", )


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
        folder = label_automation.run(source=f"instance/uploads/{vid}")
        print(folder)
        return jsonify(message="Success",
                       statusCode=200,
                       data=folder)


if __name__ == "__main__":
    app.run()
