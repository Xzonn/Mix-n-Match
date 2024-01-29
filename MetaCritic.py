import random
import time

from _helpers import ESRB, parse_title
import requests

def download():
  HEADERS = {
    "Referer": "https://www.metacritic.com/",
    "Origin": "https://www.metacritic.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }
  API_URL = "https://internal-prod.apigee.fandom.net/v1/xapi/finder/metacritic/web?sortBy=-releaseDate&productType=games&page=1&offset={offset}&limit=50"

  results: list[dict] = []
  session = requests.Session()

  page = 0
  while page < 30:
    url = API_URL.format(offset=page * 50)
    response = session.get(url, headers=HEADERS)
    items: list[dict] = response.json()["data"]["items"]
    results += items
    page += 1
    time.sleep(random.random() * 6)
  
  return results

def parse(downloaded_data):
  results = {}
  for item in downloaded_data:
    review_count = item["criticScoreSummary"]["reviewCount"]
    if review_count < 2:
      continue

    id = item["id"]
    slug = item["slug"]
    year = item.get("premiereYear", 0)
    esrb = item.get("rating", "")
    results[slug] = {
      "id": slug,
      "name": parse_title(item["title"]),
      "desc": f'{year or ""} video game'.replace("  ", " ").strip(),
      "url": f"https://www.metacritic.com/game/{slug}/",
      "type": "Q7889",
      "P12078": str(id),
      "P852": ESRB.get(esrb, ""),
    }

  results_list = sorted(results, key=lambda x: (results[x]["name"].lower(), int(results[x]["P12054"])))
  with open("results/MetaCritic.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      f.write("\t".join(game.values()) + "\n")

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  results = download()
  parse(results)