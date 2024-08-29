from flask import Flask, render_template
from youtube_lyrics import get_lyrics


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/get_lyrics', methods=['GET'])
def get_lyrics():
    return get_lyrics()