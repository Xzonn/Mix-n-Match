from _helpers import parse_title
import requests

def download():
  QUERY_URL = r"https://howlongtobeat.com/api/search"
  DATA = {
    "searchType": "games",
    "searchTerms": [""],
    "searchPage": 1,
    "size": 500000,
    "searchOptions": {
      "games": {
        "userId": 114514,
        "platform": "",
        "sortCategory": "popular",
        "rangeCategory": "main",
        "rangeTime": { "min": None, "max": None },
        "gameplay": { "perspective": "", "flow": "", "genre": "" },
        "rangeYear": { "min": "", "max": "" },
        "modifier": ""
      },
      "users": { "sortCategory": "postcount" },
      "lists": { "sortCategory": "follows" },
      "filter": "",
      "sort": 0,
      "randomizer": 0
    }
  }

  HEADERS = {
    "Referer": "https://howlongtobeat.com/",
    "Origin": "https://howlongtobeat.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }

  session = requests.Session()
  response = session.post(QUERY_URL, json=DATA, headers=HEADERS)
  game_list = response.json()["data"]
  
  # with open("results/HowLongToBeat.json", "w", -1, "utf-8") as f:
  #   json.dump(game_list, f, ensure_ascii=False, indent=2)

  return game_list

def parse(game_list: list[dict]):
  results = {}
  for game in game_list:
    if game["game_type"] != "game":
      continue
    results[game["game_id"]] = {
      "id": str(game["game_id"]),
      "name": parse_title(game["game_name"]),
      "desc": f'{game["release_world"] or ""} {game["profile_platform"]} video game {"by " + parse_title(game["profile_dev"]) if game["profile_dev"] else ""}'.replace("  ", " ").strip(),
      "url": f'https://howlongtobeat.com/game/{game["game_id"]}',
      "type": "Q7889",
      "P1733": str(game["profile_steam"]) if game["profile_steam"] > 0 else "",
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
  game_list = download()
  parse(game_list)