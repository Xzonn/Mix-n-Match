import copy
import datetime
import json
import random
import time

import requests

from _helpers import parse_title


def download():
  QUERY_URL = r"https://howlongtobeat.com/api/search"
  DATA = {
    "searchType": "games",
    "searchTerms": [""],
    "searchPage": 1,
    "size": 20,
    "searchOptions": {
      "games": {
        "userId": 0,
        "platform": "",
        "sortCategory": "popular",
        "rangeCategory": "main",
        "rangeTime": {"min": None, "max": None},
        "gameplay": {"perspective": "", "flow": "", "genre": "", "difficulty": ""},
        "rangeYear": {"min": "", "max": ""},
        "modifier": "hide_dlc",
      },
      "users": {"sortCategory": "postcount"},
      "lists": {"sortCategory": "follows"},
      "filter": "",
      "sort": 0,
      "randomizer": 0,
    },
    "useCache": True,
  }

  HEADERS = {
    "Referer": "https://howlongtobeat.com/",
    "Origin": "https://howlongtobeat.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.114.514 Safari/537.36 XzonnMixnMatch/0.1",
  }

  session = requests.Session()
  token = session.get(
    f"https://howlongtobeat.com/api/search/init?t={datetime.datetime.now().timestamp():.0f}", headers=HEADERS
  ).json()["token"]
  HEADERS["X-Auth-Token"] = token

  game_list = []
  current_year = datetime.datetime.now().year
  years = [""] + [str(y) for y in range(current_year - 5, current_year + 1)]
  for year in years:
    page = 1
    while page < 10:
      data = copy.deepcopy(DATA)
      data["searchPage"] = page
      data["searchOptions"]["games"]["rangeYear"]["min"] = str(year)  # type: ignore
      data["searchOptions"]["games"]["rangeYear"]["max"] = str(year)  # type: ignore
      page += 1
      try:
        response = session.post(QUERY_URL, json=data, headers=HEADERS)
        game_list += response.json()["data"]
        time.sleep(random.random() * 5)
      except Exception as e:
        print(f"Error: HowLongToBeat.py page {page} {e}")
        break

  return game_list


def parse(game_list: list[dict]):
  results = {}
  for game in game_list:
    if game["game_type"] != "game":
      continue
    results[game["game_id"]] = {
      "id": str(game["game_id"]),
      "name": parse_title(game["game_name"]),
      "desc": f"{game['release_world'] or ''} {game['profile_platform']} video game".replace("  ", " ").strip(),
      "url": f"https://howlongtobeat.com/game/{game['game_id']}",
      "type": "Q7889",
    }

  results_list = sorted(results, key=lambda x: (results[x]["name"].lower(), int(results[x]["id"])))

  with open("results/HowLongToBeat.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      f.write("\t".join(game.values()) + "\n")


if __name__ == "__main__":
  import os

  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  results = download()
  with open("results/HowLongToBeat.json", "w", -1, "utf-8") as writer:
    json.dump(results, writer, ensure_ascii=False, separators=(",", ":"))

  # with open("results/HowLongToBeat.json", "r", -1, "utf-8") as reader:
  #   results = json.load(reader)
  parse(results)
