import flask
import urldb
import random

app = flask.Flask(__name__)
urldb.init_app(app)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    db = urldb.get_db()

    if flask.request.method == "POST":
        random_code = generate_random_code()
        db.insert_url(flask.request.form["url_input"], random_code)
        return flask.render_template("code_show.html", code=random_code)
    else:
        registered_urls = db.get_many_urls()
        return flask.render_template("main.html", registered_urls=registered_urls)


@app.route("/<code>")
def redirect_to_code(code):
    db = urldb.get_db()

    original_url, short_code, date = db.get_url(code)
    return flask.redirect(original_url)


def generate_random_code():
    LENGTH = 4
    CHOICES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    code = ""
    for i in range(LENGTH):
        code += random.choice(CHOICES)
    return code
