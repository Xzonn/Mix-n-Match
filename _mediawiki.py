import requests
import time
from urllib.parse import quote

HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
}

_session = requests.Session()

def login(api_address, bot_name, bot_pass):
  kw = {
    "action": "query",
    "meta": "tokens",
    "type": "login"
  }
  response = _session.post(api_address, data=kw, headers=HEADERS)
  time.sleep(2.5)
  kw = {
    "action": "login",
    "lgtoken": response.json()["query"]["tokens"]["logintoken"],
    "lgname": bot_name,
    "lgpassword": bot_pass
  }
  response = _session.post(api_address, data=kw, headers=HEADERS)
  time.sleep(2.5)

def download(api_address, base_url, category, type="Q7889", desc="video game", sleep=False):
  results = {}
  now = time.time()

  kw = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": category,
    "cmnamespace": "0",
    "cmlimit": "max",
    "cmsort": "timestamp",
    "cmdir": "descending"
  }
  while (time.time() - now < 600):
    response = _session.post(api_address, data=kw, headers=HEADERS)
    json = response.json()
    for page in json["query"]["categorymembers"]:
      results[page["title"]] = {
        "id": page["title"].replace(" ", "_"),
        "name": page["title"],
        "desc": desc,
        # "url": base_url + quote(page["title"].replace(" ", "_")),
        "type": type
      }
    if "continue" in json and "cmcontinue" in json["continue"]:
      kw.update({
        "cmcontinue": json["continue"]["cmcontinue"]
      })
    else:
      break
    if sleep:
      time.sleep(2.5)
  return results

def parse(results, file_name):
  results_list = sorted(results, key=lambda x:results[x]["name"])

  with open(f"results/{file_name}", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for id in results_list:
      game = results[id]
      f.write("\t".join(game.values()) + "\n")