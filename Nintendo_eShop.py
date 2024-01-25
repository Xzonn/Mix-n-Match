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
  PARAMS_RATINGS = "hitsPerPage=1000&analytics=false&distinct=true&enablePersonalization=false&page=0&facetFilters={filters}&filters=(NOT%20topLevelFilters:DLC%20AND%20NOT%20dlcType:Bundle%20AND%20NOT%20dlcType:\"ROM%20Bundle\")"
  AVAILABLE_PARAMETERS = {
    "corePlatforms": ["Nintendo Switch"],
    "editions": ["Digital"],
    "topLevelFilters": ["", "Deals", "Demo Available", "Games with DLC"],
    "priceRange": ["", "$10 - $19.99", "$20 - $39.99", "$40+"],
    "esrbRating": ["E", "E10", "T", "M"],
    "playerCount": ["", "2+", "Single Player"],
  }
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
    facet_filters = json.dumps([f"{i[0]}:{i[1]}" for i in zip(keys, params)if i[1]], ensure_ascii=False, separators=(",", ":"))
    params = PARAMS_RATINGS.format(filters=quote(facet_filters))
    data = copy.deepcopy(DATA)
    data["requests"][0]["params"] = params
    data_list.append(data)

  hits_all: list[dict] = []
  session = requests.Session()
  for data in data_list:
    request = session.post(QUERY_URL, json=data, headers=HEADERS)
    hits = request.json()["results"][0]["hits"]
    hits_all += hits
    time.sleep(random.random())

  return hits_all

def parse(hits_all):
  ESRB = {
    "EC": "Q14864327",
    "E": "Q14864328",
    "E10": "Q14864329",
    "T": "Q14864330",
    "M": "Q14864331",
    "AO": "Q14864332",
    "RP": "Q14864333",
  }
  ESRB_DESCRIPTORS = {
    "Alcohol and Tobacco Reference": "Q99904297",
    "Alcohol Reference": "Q60316458",
    "Animated Blood": "Q60316460",
    "Animated Blood and Gore": "Q69577075",
    "Animated Violence": "Q69577345",
    "Blood": "Q60316463",
    "Blood and Gore": "Q60316461",
    "Cartoon Violence": "Q60316462",
    "Comic Mischief": "Q60316464",
    "Crude Humor": "Q60300344",
    "Digital Purchases": "Q102110695",
    "Diverse Content Discretion Advised": "Q123653389",
    "Drug and Alcohol Reference": "Q110343784",
    "Drug Reference": "Q60317579",
    "Edutainment": "Q60300293",
    "Fantasy Violence": "Q60317581",
    "Fine Motor Skills": "Q98556733",
    "Gambling": "Q97543276",
    "Game Experience May Change During Online Play": "Q97302889",
    "Gaming": "Q103531650",
    "Higher-Level Thinking Skills": "Q98556734",
    "In-App Purchases": "Q106097196",
    "Includes Demo of a Game Not Yet Rated by ESRB": "Q98088300",
    "Includes Demos rated Rating Pending to Teen by the ESRB": "Q98088301",
    "Informational": "Q60724353",
    "In-Game Purchases": "Q69991173",
    "In-Game Purchases (Includes Random Items)": "Q90412335",
    "Intense Violence": "Q60317584",
    "Language": "Q60317586",
    "Lyrics": "Q60317587",
    "Mature Humor": "Q60317589",
    "Mature Sexual Themes": "Q69821734",
    "Mild Alcohol Reference": "Q97578625",
    "Mild Animated Violence": "Q97656786",
    "Mild Blood": "Q77315029",
    "Mild Cartoon Violence": "Q69993985",
    "Mild Fantasy Violence": "Q70002023",
    "Mild Language": "Q68205918",
    "Mild Lyrics": "Q96310546",
    "Mild Realistic Violence": "Q97656787",
    "Mild Sexual Themes": "Q97585290",
    "Mild Strong Language": "Q98269045",
    "Mild Suggestive Themes": "Q72415417",
    "Mild Use of Alcohol": "Q97578141",
    "Mild Use of Drugs": "Q97579457",
    "Mild Violence": "Q60324381",
    "Mild violent references": "Q102110675",
    "Music downloads not rated by the ESRB.": "Q96220171",
    "Nudity": "Q60324383",
    "Online interactions not rated by the ESRB.": "Q68183722",
    "Online Music Not Rated by the ESRB": "Q96220186",
    "Partial Nudity": "Q60300245",
    "Reading Skills": "Q98556732",
    "Real Gambling": "Q60324384",
    "Realistic Blood": "Q98556739",
    "Realistic Blood and Gore": "Q69582662",
    "Realistic Violence": "Q69583053",
    "Sexual Content": "Q69578048",
    "Sexual Themes": "Q60324385",
    "Sexual Violence": "Q60324386",
    "Shares Info": "Q97363751",
    "Shares Location": "Q69430054",
    "Simulated Gambling": "Q60324387",
    "Some Adult Assistance May Be Needed": "Q60324422",
    "Strong Language": "Q60300342",
    "Strong Lyrics": "Q60324421",
    "Strong Sexual Content": "Q60324423",
    "Strong Sexual Themes": "Q97061867",
    "Strong Violence": "Q102110867",
    "Suggestive Themes": "Q60324424",
    "Tobacco Reference": "Q60324425",
    "Unrestricted Internet": "Q69430020",
    "Use of Alcohol": "Q60324427",
    "Use of Alcohol and Tobacco": "Q96337561",
    "Use of Drugs": "Q60324426",
    "Use of Drugs and Alcohol": "Q86235040",
    "Use of Drugs and Tobacco": "Q124356179",
    "Use of Tobacco": "Q60324428",
    "Users Interact": "Q69430207",
    "Violence": "Q60324429",
    "Violent References": "Q69573910",
  }
  results = {}
  for game in hits_all:
    if "DLC" in game["topLevelFilters"] or ["Physical"] == game["editions"] or game["dlcType"]:
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
      "name": game["title"].replace("™", "").replace("®", "").replace("\n", " ").strip(),
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