def parse():
  with open("temp/vndb/db/vn.header", "r", -1, "utf8") as reader:
    vn_header = reader.read().splitlines()[0].split("\t")
  with open("temp/vndb/db/vn", "r", -1, "utf8") as reader:
    vn = reader.read().splitlines()

  results = {}
  for game in vn:
    game_data = dict(zip(vn_header, game.split("\t")))
    if len(game_data) != len(vn_header):
      continue
    game_id = game_data["id"]
    results[game_id] = {
      "id": game_id,
      "q": ("Q" + game_data["l_wikidata"]) if game_data["l_wikidata"] != "\\N" else "",
      "name": "",
      "desc": "video game",
      "url": f"https://vndb.org/{game_id}",
      "type": "Q7889",
      "P21": "",
      "#olang": game_data["olang"],
    }

  with open("temp/vndb/db/vn_titles.header", "r", -1, "utf8") as reader:
    vn_titles_header = reader.read().splitlines()[0].split("\t")
  with open("temp/vndb/db/vn_titles", "r", -1, "utf8") as reader:
    vn_titles = reader.read().splitlines()
  
  for game in vn_titles:
    game_data = dict(zip(vn_titles_header, game.split("\t")))
    game_id = game_data["id"]
    if game_id not in results or len(game_data) != len(vn_titles_header):
      continue
    if game_data["lang"] == "en" or (game_data["lang"] == results[game_id]["#olang"] and not results[game_id]["name"]):
      results[game_id]["name"] = game_data["title"].replace("™", "").replace("®", "").replace("\n", " ").strip()

  for game in results.values():
    if "#olang" in game:
      del game["#olang"]

  with open("temp/vndb/db/producers.header", "r", -1, "utf8") as reader:
    producers_header = reader.read().splitlines()[0].split("\t")
  with open("temp/vndb/db/producers", "r", -1, "utf8") as reader:
    producers = reader.read().splitlines()
  for producer in producers:
    producer_data = dict(zip(producers_header, producer.split("\t")))
    if len(producer_data) != len(producers_header) or producer_data["type"] != "co":
      continue
    producer_id = producer_data["id"]
    results[producer_id] = {
      "id": producer_id,
      "q": ("Q" + producer_data["l_wikidata"]) if producer_data["l_wikidata"] != "\\N" else "",
      "name": producer_data["name"],
      "desc": "video game developer/producer",
      "url": f"https://vndb.org/{producer_id}",
      "type": "Q210167",
      "P21": "",
    }

  with open("temp/vndb/db/staff_alias.header", "r", -1, "utf8") as reader:
    staff_alias_header = reader.read().splitlines()[0].split("\t")
  with open("temp/vndb/db/staff_alias", "r", -1, "utf8") as reader:
    staff_alias = reader.read().splitlines()
  staff_names = {}
  for person in staff_alias:
    person_data = dict(zip(staff_alias_header, person.split("\t")))
    if len(person_data) != len(staff_alias_header):
      continue
    staff_names[person_data["aid"]] = person_data["name"]

  with open("temp/vndb/db/staff.header", "r", -1, "utf8") as reader:
    staff_header = reader.read().splitlines()[0].split("\t")
  with open("temp/vndb/db/staff", "r", -1, "utf8") as reader:
    staff = reader.read().splitlines()
  for person in staff:
    person_data = dict(zip(staff_header, person.split("\t")))
    if len(person_data) != len(staff_header):
      continue
    person_id = person_data["id"]
    results[person_id] = {
      "id": person_id,
      "q": ("Q" + person_data["l_wikidata"]) if person_data["l_wikidata"] != "\\N" else "",
      "name": staff_names.get(person_data["main"], ""),
      "desc": "male" if person_data["gender"] == "m" else ("female" if person_data["gender"] == "f" else ""),
      "url": f"https://vndb.org/{person_id}",
      "type": "Q5",
      "P21": "Q6581097" if person_data["gender"] == "m" else ("Q6581072" if person_data["gender"] == "f" else ""),
    }

  results_list = sorted(results, key=lambda x: (results[x]["type"], results[x]["name"]))

  with open("results/VNDB.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      f.write("\t".join(game.values()) + "\n")

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  parse()