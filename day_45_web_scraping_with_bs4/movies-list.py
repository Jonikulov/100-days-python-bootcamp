import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline" \
    ".com/movies/features/best-movies-2/"
url = "https://empireonline.com/movies/features/best-movies-2/"

print("Scraping movies...")
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")
movies_data = [
    movie.get_text(strip=True) for movie in soup.select("span > h2 > strong")
]
# Sort in the ascending order
movies_data.reverse()
# movies_data.sort(key=lambda x: int(x.split(") ")[0]))

print("Writing result data...")
with open("movies.txt", "w") as file:
    file.write("\n".join(movies_data))
