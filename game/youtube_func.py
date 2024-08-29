from config import get_db_connection, youtube_client_conn


def search_youtube_videos(query, prefer_official=True):
    # Versuche zuerst, das Video aus der Datenbank zu laden
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM videos WHERE artist_name = ?", (query,))
    video = c.fetchone()
    conn.close()

    if video:
        return {
            'title': video['title'],
            'videoId': video['video_id'],
            'thumbnail': video['thumbnail'],
            'channelTitle': video['channel_title']
        }

    # Wenn nicht in der Datenbank, YouTube-API abfragen
    search_response = youtube_client_conn.search().list(
        q=query,
        part='snippet',
        maxResults=5,
        type='video'
    ).execute()

    official_videos = []
    alternative_videos = []

    for search_result in search_response.get('items', []):
        video_data = {
            'title': search_result['snippet']['title'],
            'videoId': search_result['id']['videoId'],
            'thumbnail': search_result['snippet']['thumbnails']['high']['url'],
            'channelTitle': search_result['snippet']['channelTitle']
        }

        if "YouTube Music" in search_result['snippet']['channelTitle'] or "Official" in search_result['snippet']['title'].lower():
            official_videos.append(video_data)
        else:
            alternative_videos.append(video_data)

    # Wähle das bevorzugte Video
    selected_video = official_videos[0] if prefer_official and official_videos else alternative_videos[0] if alternative_videos else None

    if selected_video:
        # Speichere das Video in der Datenbank
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT OR IGNORE INTO videos (artist_name, title, video_id, thumbnail, channel_title) 
            VALUES (?, ?, ?, ?, ?)
        ''', (query, selected_video['title'], selected_video['videoId'], selected_video['thumbnail'], selected_video['channelTitle']))
        conn.commit()
        conn.close()

    return selected_video


def fetch_random_song_from_youtube(artist_name):
    query = f"{artist_name} official music video"
    video = search_youtube_videos(query)
    if not video:
        raise ValueError("No videos found.")
    return video
