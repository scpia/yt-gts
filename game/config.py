import sqlite3
from googleapiclient.discovery import build

APP_KEY = "PaulIstImmerNochEinHs"
YOUTUBE_API_KEY = "DEIN_YOUTUBE_API_KEY"

# YouTube API Client initialisieren
youtube_client_conn = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Funktion zur Verbindung mit der Datenbank
def get_db_connection():
    conn = sqlite3.connect('youtube_videos.db')
    conn.row_factory = sqlite3.Row
    return conn