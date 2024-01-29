import datetime
import json
import random
import time

from bs4 import BeautifulSoup
from _helpers import parse_title
import requests

def download():
  HEADERS = {
    "Referer": "https://opencritic.com/",
    "Origin": "https://opencritic.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }
  API_URL = "https://api.opencritic.com/api/game?skip={skip}&sort=firstReleaseDate"

  results: list[dict] = []
  session = requests.Session()

  if "Calendar":
    calendar_text = session.get("https://opencritic.com/calendar", headers=HEADERS).text
    parser = BeautifulSoup(calendar_text, "html.parser")
    calendar_json = json.loads(parser.find(id="serverApp-state").get_text().replace("&q;", '"')).get("calendar", {})
    results += calendar_json.get("games", [])

  page = 0
  while page < 20:
    url = API_URL.format(skip=page * 20)
    response = session.get(url, headers=HEADERS)
    items: list[dict] = response.json()
    results += items
    page += 1
    time.sleep(random.random() * 5)
  
  return results

def parse(downloaded_data):
  results = {}
  for item in downloaded_data:
    id = item["id"]
    year = 0
    try:
      release_date = datetime.datetime.strptime(item.get("firstReleaseDate", ""), "%Y-%m-%dT%H:%M:%S.%fZ")
      year = release_date.year
    except:
      pass
    platforms = ", ".join(map(lambda x: x.get("shortName", ""), item.get("Platforms", [])))
    results[str(id)] = {
      "id": str(id),
      "name": parse_title(item["name"]),
      "desc": f'{year or ""} {platforms} video game'.replace("  ", " ").strip(),
      "url": f"https://opencritic.com/game/{id}/-",
      "type": "Q7889",
    }

  results_list = sorted(results, key=lambda x: (results[x]["name"].lower(), int(results[x]["id"])))
  with open("results/OpenCritic.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      f.write("\t".join(game.values()) + "\n")

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  results = download()
  parse(results)