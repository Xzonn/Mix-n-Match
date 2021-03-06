import copy
import json
import requests

def download():
  QUERY_URL = r"https://u3b6gr4ua3-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser%3B%20JS%20Helper%20(3.6.2)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(6.15.0)"
  DATA = {
    "requests": [
      {
        "indexName": "store_game_en_us_release_des",
        "params": "hitsPerPage=1000&analytics=false&distinct=true&enablePersonalization=false&page=0&facetFilters=%5B%22corePlatforms%3ANintendo%20Switch%22%5D"
      }
    ]
  }
  PARAMS_RATINGS = "hitsPerPage=1000&analytics=false&distinct=true&enablePersonalization=false&page=0&facetFilters=%5B%22corePlatforms%3ANintendo%20Switch%22%2C%22esrbRating%3A{rating}%22%5D"
  RATINGS = ["E", "E10", "T", "M", "RP"]
  HEADERS = {
    "x-algolia-api-key": "a29c6927638bfd8cee23993e51e721c9",
    "x-algolia-application-id": "U3B6GR4UA3",
    "Referer": "https://www.nintendo.com/",
    "Origin": "https://www.nintendo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }

  data_list = []
  for rating in RATINGS:
    params = PARAMS_RATINGS.format(rating=rating)
    data = copy.deepcopy(DATA)
    data["requests"][0]["params"] = params
    data_list.append(data)
  
  data = copy.deepcopy(DATA)
  data["requests"][0]["indexName"] = "store_game_en_us"
  data_list.append(data.copy())

  hits_all = []
  session = requests.Session()
  for data in data_list:
    request = session.post(QUERY_URL, json=data, headers=HEADERS)
    hits = request.json()["results"][0]["hits"]
    hits_all += hits

  #with open("results/Nintendo_eShop.json", "w", -1, "utf-8") as f:
  #  json.dump(hits_all, f, ensure_ascii=False, indent=2)
  
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
  results = {}
  for game in hits_all:
    if "DLC" in game["topLevelFilters"] or "Games with DLC" in game["topLevelFilters"] or ["Physical"] == game["editions"]:
      continue
    results[game["urlKey"].strip()] = {
      "id": game["urlKey"].strip(),
      "name": game["title"].replace("???", "").replace("??", "").replace("\n", " ").strip(),
      "desc": f'{game["platform"]} video game by {game["softwarePublisher"]}'.replace("  ", " "),
      "url": f'https://www.nintendo.com{game["url"]}',
      "type": "Q7889",
      "P400": "Q19610114",
      "P437": "Q54820071",
      "P750": "Q3070866",
      "P852": ESRB[game["esrbRating"]] if game["esrbRating"] in ESRB else ""
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
  parse(download())