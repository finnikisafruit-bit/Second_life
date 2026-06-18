from flask import Flask, render_template, url_for


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/basket")
def basket():
    return render_template("basket.html")


@app.route("/my_announcement")
def my_announcement():
    return render_template("my_announcement.html")


@app.route("/create_announcement")
def create_announcement():
    return render_template("create_announcement.html")


if  __name__ == '__main__':
    app.run(debug=True)