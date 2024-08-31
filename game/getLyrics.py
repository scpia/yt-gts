import requests
import random

# Remove section headers (e.g. [Chorus]) from lyrics when searching
def get_artist_id(artist_name, access_token):
    base_url = "https://api.genius.com"
    search_url = f"{base_url}/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": artist_name}
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    
    artist_id = None
    for hit in data['response']['hits']:
        artist = hit['result']['primary_artist']
        if artist['name'].lower() == artist_name.lower():
            artist_id = artist['id']
            break
    
    return artist_id

def get_songs_by_artist(artist_id, access_token):
    base_url = "https://api.genius.com"
    artist_songs_url = f"{base_url}/artists/{artist_id}/songs"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(artist_songs_url, headers=headers)
    data = response.json()
    songs = []
    for song in data['response']['songs']:
        songs.append({
            'title': song['title'],
            'path': song['path']
        })
    
    return songs

def get_random_song(artist_name, access_token):
    artist_id = get_artist_id(artist_name, access_token)
    if not artist_id:
        return "Artist not found"
    
    songs = get_songs_by_artist(artist_id, access_token)
    print(songs)
    if not songs:
        return "No songs found for this artist"
    
    random_song = random.choice(songs)
    return random_song


def get_song_lyrics(artist_name, access_token):
    song_title = get_random_song(artist_name=artist_name,access_token=access_token)
    base_url = "https://api.genius.com"
    search_url = f"{base_url}/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"{song_title} {artist_name}"}
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    
    print(data)
    song_info = None
    for hit in data['response']['hits']:
        song = hit['result']
        if song['title'].lower() == song_title.lower() and song['primary_artist']['name'].lower() == artist_name.lower():
            song_info = song
            break
    print(song_info)
    if song_info:
        song_path = song_info['path']
        lyrics_url = f"{base_url}{song_path}"
        lyrics_response = requests.get(lyrics_url)
        if lyrics_response.status_code == 200:
            return lyrics_response.text
        else:
            return "Lyrics not found"
    else:
        return "Song not found"