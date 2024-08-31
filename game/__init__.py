import build
from flask import Flask, jsonify, render_template, request
import getLyrics


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/enterArtist")
def get_lyrics():
    return render_template("enterArtist.html")

@app.route("/guessLyrics", methods=["GET", "POST"])
def guess_lyrics():
    if request.method == "POST":
        artist = request.form.get("artist")
        if artist:
            lyrics = getLyrics.get_song_lyrics(artist,access_token="0eQ5wCq5SI1y-TBbkEoX-kPPxHcHhqwRKRYRNdqJINNZzcG0kfjWmo7MMz8I3-ZS")
            if lyrics:
                return render_template("guessLyrics.html", artist=artist, lyrics=lyrics)
            else:
                return jsonify({"error": "Could not retrieve lyrics"}), 500
        else:
            return jsonify({"error": "Artist not provided"}), 400
    return render_template("enterArtist.html")


if __name__ == "__main__":
    app.run(debug=True)
