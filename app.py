import flask
import urldb
import random

app = flask.Flask(__name__)
#TODO: improve database management using the g object
urldb = urldb.URLDB("small_url.db")

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if flask.request.method == "POST":
        random_code = generate_random_code()
        urldb.insert_url(flask.request.form["url_input"], random_code)
        return flask.render_template("code_show.html", code=random_code)
    else:
        return flask.render_template("main.html", registered_urls = urldb.get_many_urls())
 
@app.route("/<code>")
def redirect_to_code(code):
    print(code)
    original_url, short_code, date = urldb.get_url(code)
    return flask.redirect(original_url)

def generate_random_code():
    LENGTH = 4
    CHOICES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    code = ""
    for i in range(LENGTH):
        code += random.choice(CHOICES)
    return code;

