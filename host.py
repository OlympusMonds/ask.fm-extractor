from flask import Flask, url_for, redirect
from extract import extract

ask_flask = Flask(__name__)

@ask_flask.route("/")
def index():
    return ("<h1> Ask.fm extractor </h1><p>"
            "To use this site, add a /username after the .com</br>"
            "For example olympusmonds.pythonanywhere.com/olympusmonds")


@ask_flask.route("/<username>")
def extract_for_user(username):
    print("Request for {}".format(username))

    html = True
    if html:
        output = extract(username, newline="<br/>")
    else:
        output = extract(username)
    return output


if __name__ == "__main__":
    ask_flask.debug = False 
    ask_flask.run()



