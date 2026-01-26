import datetime
import json
import random
import time

import requests

from _helpers import parse_title


def parseIcs(raw: str):
  lines = raw.replace("\n ", "").split("\n")
  events = []
  event = {}
  for line in lines:
    if line.startswith("BEGIN:VEVENT"):
      event = {}
    elif line.startswith("END:VEVENT"):
      events.append(event)
    else:
      if ":" in line:
        key, value = line.split(":", 1)
        event[key] = value
  return events


def download():
  HEADERS = {
    "Referer": "https://opencritic.com/",
    "Origin": "https://opencritic.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.114.514 Safari/537.36 XzonnMixnMatch/0.1",
  }
  API_URL = "https://api.opencritic.com/api/game?skip={skip}&sort=firstReleaseDate"

  results: list[dict] = []
  session = requests.Session()

  if "Calendar":
    calendar_json = session.get("https://api.opencritic.com/api/calendar/v2", headers=HEADERS).json()
    results += calendar_json.get("games", [])

  if "ICS":
    ics_text = session.get("https://img.opencritic.com/calendar/OpenCritic.ics", headers=HEADERS).text.replace(
      "\r\n", "\n"
    )
    events = parseIcs(ics_text)
    for event in events:
      name = event.get("SUMMARY", "").strip().removesuffix(" Release").replace("\\,", ",")
      url: str = event.get("URL;VALUE=URI", "")
      id = url.split("/game/", 1)[1].split("/", 1)[0]
      date = event.get("DTSTART;VALUE=DATE", "")
      year, month, day = int(date[0:4]), int(date[4:6]), int(date[6:8])
      game = {
        "id": int(id),
        "name": name,
        "firstReleaseDate": f"{year:04d}-{month:02d}-{day:02d}T12:00:00.000Z",
        "Platforms": [],
        "url": url,
      }
      results.append(game)

  page = 0
  while page < 10:
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
      "desc": f"{year or ''} {platforms} video game".replace("  ", " ").strip(),
      "url": item.get("url", f"https://opencritic.com/game/{id}/-").strip(),
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
  with open("results/OpenCritic.json", "w", -1, "utf-8") as writer:
    json.dump(results, writer, ensure_ascii=False, separators=(",", ":"))
  parse(results)
