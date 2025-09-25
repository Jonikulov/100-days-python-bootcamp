"""Day 46. Create a Spotify Playlist using the Musical Time Machine"""

import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

# Getting top 100 songs from Billboard
travel_time = input("Which year do you want to travel to? (YYYY-mm-dd): ")
print(f"Scraping travel time: {travel_time} ...")

url = "https://billboard.com/charts/hot-100"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 " \
        "Safari/537.36"
}
resp = requests.get(url + f"/{travel_time}", headers=header)
soup = BeautifulSoup(resp.text, "html.parser")
song_titles = soup.select(
    "li > ul > li.o-chart-results-list__item > h3#title-of-a-story"
)
song_artists_rows = soup.select(
    "li > ul > li.o-chart-results-list__item > span"
)

song_artists = []
for artists in song_artists_rows:
    artist_names = [a.get_text(strip=True) for a in artists.select("a")]
    if artist_names:
        artist = ", ".join(artist_names)
    else:
        artist = artists.get_text(strip=True)
    song_artists.append(artist)


# spotify = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="playlist-modify-private",
#         redirect_uri="https://example.com/",
#         client_id=os.getenv("SPOTIFY_CLIENT_ID"),
#         client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
#     )
# )
spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    )
)

# Create a new playlist in spotify with the date name
new_playlist = spotify.user_playlist_create(
    user=os.getenv("SPOTIFY_USER_ID"),
    name=f"{travel_time} Billboard ~100",
    public=False,
)

# Search songs from spotify and add found results to the new playlist
for i in range(len(song_titles)):
    song_title = song_titles[i].get_text(strip=True)
    print("\nSearching the track:")
    print(f"{i + 1}. Song: {song_title}")
    print(f"\tArtist(s): {song_artists[i]}")

    search_results = spotify.search(
        f"track: {song_title} year: {travel_time.split("-")[0]}",
        offset=0,
        type="track",
    )

    for track in search_results["tracks"]["items"]:
        artist = track["artists"][0]["name"]
        if song_title.lower() in track["name"].lower() or \
            artist.lower() in song_artists[i].lower():
            print(f'Spotify search result: {track["name"]},\t{artist}')
            spotify.user_playlist_add_tracks(
                user=os.getenv(""),
                playlist_id=new_playlist["id"],
                tracks=[track["id"]],
            )
            break

