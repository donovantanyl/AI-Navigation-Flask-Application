from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("index.html", )


@app.route("/bus_navigation")
def bus_navigation():
    return render_template("bus_navigation.html", )


if __name__ == "__main__":
    app.run()
