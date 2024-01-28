from _helpers import ESRB, ESRB_DESCRIPTORS
import copy
import datetime
import itertools
import json
import random
import time
from urllib.parse import quote
import requests

def download() -> list[dict]:
  QUERY_URL = r"https://u3b6gr4ua3-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser%3B%20JS%20Helper%20(3.6.2)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(6.15.0)"
  DATA = {
    "requests": [
      {
        "indexName": "store_game_en_us",
        "params": ""
      }
    ]
  }
  PARAMS_RATINGS = "hitsPerPage=1000&analytics=false&distinct=true&enablePersonalization=false&page=0&facetFilters={facet_filters}&filters=({filters})"
  AVAILABLE_PARAMETERS = {
    "corePlatforms": ["Nintendo Switch"],
    "editions": ["Digital"],
    "topLevelFilters": ["", "Deals", "Demo Available", "Games with DLC"],
    "priceRange": ["", "$10 - $19.99", "$20 - $39.99", "$40+"],
    "esrbRating": ["E", "E10", "T", "M"],
    "playerCount": ["", "2+", "Single Player"],
  }
  FILTERS = [
    ("topLevelFilters", "DLC"),
    ("dlcType", "Bundle"),
    ("dlcType", "ROM Bundle"),
  ]
  HEADERS = {
    "x-algolia-api-key": "a29c6927638bfd8cee23993e51e721c9",
    "x-algolia-application-id": "U3B6GR4UA3",
    "Referer": "https://www.nintendo.com/",
    "Origin": "https://www.nintendo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }

  data_list = []
  keys = AVAILABLE_PARAMETERS.keys()
  for params in itertools.product(*AVAILABLE_PARAMETERS.values()):
    facet_filters = []
    filters = copy.deepcopy(FILTERS)
    for k, p in zip(keys, params):
      if p:
        facet_filters.append(f"{k}:{p}")
      else:
        for i in AVAILABLE_PARAMETERS[k]:
          if i:
            filters.append((k, i))

    facet_filters_str = json.dumps(facet_filters, ensure_ascii=False, separators=(",", ":"))
    filters_str = " AND ".join(f"NOT {k}:\"{v}\"" for k, v in filters)
    params = PARAMS_RATINGS.format(filters=quote(filters_str), facet_filters=quote(facet_filters_str))
    data = copy.deepcopy(DATA)
    data["requests"][0]["params"] = params
    data_list.append(data)

  hits_all: list[dict] = []
  session = requests.Session()
  for data in data_list:
    request = session.post(QUERY_URL, json=data, headers=HEADERS)
    hits = request.json()["results"][0]["hits"]
    hits_all += hits
    time.sleep(random.random() * 2)

  return hits_all

def parse(hits_all):
  results = {}
  for game in hits_all:
    if "DLC" in game["topLevelFilters"] or ["Physical"] == game["editions"] or game["dlcType"] or (not game["nsuid"]):
      continue
    esrb = game.get("esrbRating", "")
    year = 0
    try:
      release_date = datetime.datetime.strptime(game.get("releaseDate", ""), "%Y-%m-%dT%H:%M:%S.%fZ")
      year = release_date.year
    except:
      pass
    descriptors = []
    for i in game.get("esrbDescriptors", []) or []:
      if i not in ESRB_DESCRIPTORS:
        print(f"Warning: {i} not in ESRB_DESCRIPTORS")
      else:
        descriptors.append(ESRB_DESCRIPTORS[i])
    results[game["urlKey"].strip()] = {
      "id": game["urlKey"].strip(),
      "name": game["title"].replace("™", " ").replace("®", " ").replace("\n", " ").replace("  ", " ").replace(" :", ":").strip(),
      "desc": f'{year or ""} {game["platform"]} video game by {game["softwarePublisher"]}'.replace("  ", " ").strip(),
      # "url": f'https://www.nintendo.com{game["url"]}',
      "type": "Q7889",
      "P400": "Q19610114",
      "P437": "Q54820071",
      "P750": "Q3070866",
      "P852": ESRB.get(esrb, ""),
      "#ESRB_DESCRIPTORS": "|".join(descriptors),
    }

  results_list = sorted(results, key=lambda x:results[x]["name"])

  with open("results/Nintendo_eShop.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      f.write("\t".join(game.values()) + "\n")

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  results = download()
  parse(results)