from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import requests

app = Flask(__name__)

# YouTube API und Genius API Konfiguration
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
GENIUS_API_TOKEN = 'YOUR_GENIUS_API_TOKEN'

# YouTube Data API Client initialisieren
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_video_info(query):
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        return video_id, video_title
    return None, None

def get_genius_lyrics(song_title, artist_name):
    base_url = "https://api.genius.com"
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + "/search"
    data = {'q': f'{song_title} {artist_name}'}
    response = requests.get(search_url, data=data, headers=headers)
    
    if response.status_code == 200:
        json_data = response.json()
        if json_data['response']['hits']:
            song_api_path = json_data['response']['hits'][0]['result']['api_path']
            song_url = base_url + song_api_path
            song_response = requests.get(song_url, headers=headers)
            song_info = song_response.json()
            lyrics_url = song_info['response']['song']['url']  # URL zum Songtext
            return lyrics_url
    return None

def get_lyrics():
    song_title = request.args.get('title')
    artist_name = request.args.get('artist')
    
    if not song_title or not artist_name:
        return jsonify({'error': 'Please provide both song title and artist name'}), 400
    
    # YouTube-Video-Informationen abrufen
    video_id, video_title = get_youtube_video_info(f'{song_title} {artist_name}')
    
    if not video_id:
        return jsonify({'error': 'No video found for the given song title and artist'}), 404
    
    # Songtexte von Genius abrufen
    lyrics_url = get_genius_lyrics(song_title, artist_name)
    
    if not lyrics_url:
        return jsonify({'error': 'No lyrics found for the given song title and artist'}), 404
    
    return jsonify({
        'video_id': video_id,
        'video_title': video_title,
        'lyrics_url': lyrics_url
    })
