import copy
import datetime
import itertools
import json
import random
import time
from urllib.parse import quote

import requests

from _helpers import ESRB, ESRB_DESCRIPTORS, PLATFORMS, parse_title


def download() -> list[dict]:
  QUERY_URL = r"https://u3b6gr4ua3-3.algolianet.com/1/indexes/store_game_en_us/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.23.2)%3B%20Browser"
  DATA = {
    "query": "",
    "filters": "",
    "hitsPerPage": 1000,
    "analytics": False,
    "facetingAfterDistinct": True,
    "clickAnalytics": False,
    # "highlightPreTag": "^*^^",
    # "highlightPostTag": "^*",
    # "attributesToHighlight": ["description"],
    "facets": ["*"],
    "maxValuesPerFacet": 1000,
    "page": 0,
  }
  DEFAULT_FILTERS = [
    '(editions:"Digital")',
  ]
  AVAILABLE_PARAMETERS = {
    "corePlatforms": ["Nintendo Switch", "Nintendo Switch 2"],
    "topLevelFilters": ["", "Demo available", "Games with DLC"],
    "priceRange": ["", "$10 - $19.99", "$20 - $39.99", "$40+"],
    # "contentRatingCode": ["", "E", "E10", "T", "M"],
    # "playerCount": ["", "2+", "Single Player"],
    "nsoFeatures": ["", "Online Play", "Save Data Cloud"],
  }
  AVAILABLE_PUBLISHERS = {
    "corePlatforms": ["Nintendo Switch", "Nintendo Switch 2"],
    "softwarePublisher": [
      "BANDAI NAMCO Entertainment",
      "KOEI TECMO AMERICA",
      "NIS America",
      "Nintendo",
      "CAPCOM",
      "KEMCO",
      "Marvelous (XSEED)",
      "SEGA",
      "SQUARE ENIX",
      "WB Games",
      "THQ Nordic",
      "Ubisoft",
      "Team17",
      "TAITO",
      "D3PUBLISHER",
      "Bushiroad",
      "Electronic Arts",
      "2K",
      "ARC SYSTEM WORKS",
      "GungHo America",
      "Devolver Digital",
      "Atari",
      "Idea Factory",
      "Kairosoft",
    ],
  }
  HEADERS = {
    "x-algolia-api-key": "a29c6927638bfd8cee23993e51e721c9",
    "x-algolia-application-id": "U3B6GR4UA3",
    "Referer": "https://www.nintendo.com/",
    "Origin": "https://www.nintendo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.114.514 Safari/537.36 XzonnMixnMatch/0.1",
  }

  data_list = [copy.deepcopy(DATA)]
  for params in [AVAILABLE_PARAMETERS, AVAILABLE_PUBLISHERS]:
    keys = params.keys()
    for params in itertools.product(*params.values()):
      filters = copy.deepcopy(DEFAULT_FILTERS)
      for k, p in zip(keys, params):
        if p:
          filters.append(f'({k}:"{p}")')

      filters_str = " AND ".join(filters)
      data = copy.deepcopy(DATA)
      data["filters"] = filters_str
      data_list.append(data)

  hits_all: list[dict] = []
  session = requests.Session()
  for data in data_list:
    try:
      request = session.post(QUERY_URL, json=data, headers=HEADERS)
    except Exception as e:
      print(f"Error: {e}")
      time.sleep(5)
      continue

    hits = request.json()["hits"]
    hits_all += hits
    time.sleep(random.random() * 2)

  return hits_all


def parse(hits_all):
  results = {}
  for game in hits_all:
    if (
      "DLC" in game.get("topLevelFilters", [])
      or ["Physical"] == game.get("editions", [])
      or game.get("dlcType", None)
      or (not game.get("nsuid", None))
    ):
      continue
    productType = (game.get("eshopDetails") or {}).get("productType", "")
    if productType not in ["TITLE"]:
      continue

    esrb = game.get("contentRatingCode", "")
    year = 0
    try:
      release_date = datetime.datetime.strptime(game.get("releaseDate", ""), "%Y-%m-%dT%H:%M:%S.%fZ")
      year = release_date.year
    except:
      pass
    descriptors = []
    interactive_elements = []
    for i in game.get("contentDescriptors", []) or []:
      label = i.get("label", "")
      if label not in ESRB_DESCRIPTORS:
        if "www.esrb.org" in label:
          continue
        print(f"Warning: {label} not in ESRB_DESCRIPTORS")
      else:
        if i["type"] == "CONTENT_DESCRIPTOR":
          descriptors.append(ESRB_DESCRIPTORS[label])
        elif i["type"] == "INTERACTIVE_ELEMENT":
          interactive_elements.append(ESRB_DESCRIPTORS[label])

    platform = game.get("platform", "")
    platformQid = PLATFORMS.get(platform, "")

    results[game["urlKey"].strip()] = {
      "id": game["urlKey"].strip(),
      "name": parse_title(game["title"]),
      "desc": f"{year or ''} {platform} video game by {parse_title(game['softwarePublisher'])}".replace(
        "  ", " "
      ).strip(),
      "url": f"https://www.nintendo.com{game['url']}",
      "type": "Q7889",
      "P400": platformQid,
      "P437": "Q54820071",
      "P750": "Q3070866",
      "P852": ESRB.get(esrb, ""),
      "#ESRB_DESCRIPTORS": "|".join(descriptors),
      "#ESRB_INTERACTIVE_ELEMENTS": "|".join(interactive_elements),
    }

  results_list = sorted(results, key=lambda x: (results[x]["name"].lower(), results[x]["id"]))

  with open("results/Nintendo_eShop.txt", "w", -1, "utf-8") as writer:
    writer.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      writer.write("\t".join(game.values()) + "\n")


if __name__ == "__main__":
  import os

  os.chdir(os.path.dirname(os.path.abspath(__file__)))

  results = download()
  with open("results/Nintendo_eShop.json", "w", -1, "utf-8") as writer:
    json.dump(results, writer, ensure_ascii=False, separators=(",", ":"))
  parse(results)
