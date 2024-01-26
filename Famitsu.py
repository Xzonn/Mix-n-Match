from _helpers import PLATFORMS
from bs4 import BeautifulSoup
import math
import re
import requests
import time

def download():
  URLS = ["https://www.famitsu.com/schedule/", "https://www.famitsu.com/schedule/recent/"]
  HEADERS = {
    "Referer": "https://www.famitsu.com/",
    "Origin": "https://www.famitsu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }
  session = requests.Session()
  results = {}
  now = time.time()

  for url_base in URLS:
    max_page = 60
    item_per_page = 30
    page = 1
    while page < max_page and (time.time() - now < 600):
      if page > 1:
        url = f"{url_base}all/{page}/"
      else:
        url = url_base
      response = session.get(url, headers=HEADERS)
      text = response.text
      total = int(re.findall(r"([\d,]+)本のソフトデータ", text)[0].replace(",", ""))
      max_page = min(max_page, math.ceil(total / item_per_page))
      parser = BeautifulSoup(text, "html.parser")
      body = parser.find(class_="contents-sort--schedule").parent
      headings = body.find_all(class_="heading--base")
      rows = body.find_all(class_="schedule-row")
      for heading, row in zip(headings, rows):
        year = re.findall(r"(\d+)年", heading.get_text())
        if not year:
          year = ""
        else:
          year = year[0]
        cards = row.find_all(class_="card-schedule")
        for card in cards:
          if card.find(class_="media-image--no-game"):
            continue
          platform = card.find(class_="icon-console").get_text()
          title = card.find(class_="card-schedule__title-inline").get_text().split("（")[0].strip()
          id = re.findall(r"/games/t/(\d+)/", card.find(class_="card-schedule__inner").get("href"))[0]
          if id not in results:
            results[id] = {
              "id": id,
              "name": title,
              "desc": f"{year} {platform} video game".strip(),
              "url": f"https://www.famitsu.com/games/t/{id}/",
              "type": "Q7889",
              "P400": PLATFORMS[platform] if platform in PLATFORMS else "",
            }
          else:
            if len(title) < len(results[id]["name"]):
              results[id]["name"] = title
      page += 1
  return results

def parse(results):
  results_list = sorted(results, key=lambda x:int(results[x]["id"]))

  with open("results/Famitsu.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for id in results_list:
      game = results[id]
      f.write("\t".join(game.values()) + "\n")

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  parse(download())