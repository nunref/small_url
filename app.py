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
        urldb.connect()
        urldb.insert_url(flask.request.form["url_input"], random_code)
        urldb.disconnect()
        return flask.render_template("code_show.html", code=random_code)
    else:
        urldb.connect()
        registered_urls = urldb.get_many_urls()
        urldb.disconnect()
        return flask.render_template("main.html", registered_urls = registered_urls)
 
@app.route("/<code>")
def redirect_to_code(code):
    print(code)
    urldb.connect()
    original_url, short_code, date = urldb.get_url(code)
    urldb.disconnect()
    return flask.redirect(original_url)

def generate_random_code():
    LENGTH = 4
    CHOICES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    code = ""
    for i in range(LENGTH):
        code += random.choice(CHOICES)
    return code;

