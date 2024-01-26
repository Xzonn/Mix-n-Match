import json
import requests

def download():
  LIST_URL = r"https://reco-public.rec.mp.microsoft.com/channels/Reco/V8.0/Lists/Computed/{type}?Market=us&Language=en&ItemTypes=Game&deviceFamily=Windows.Xbox&count=200&skipitems={page}"
  TYPES = ["New", "TopPaid", "MostPlayed", "BestRated", "ComingSoon"]
  DETAIL_URL = r"https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={ids}&market=US&languages=en-us"
  HEADERS = {
    "Referer": "https://www.xbox.com/",
    "Origin": "https://www.xbox.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.114.514 Safari/537.36 XzonnMixnMatch/0.1"
  }

  ids = {}
  session = requests.Session()

  for type in TYPES:
    page = 0
    while True:
      url = LIST_URL.format(type=type, page=page * 200)
      response = session.get(url, headers=HEADERS)
      items = response.json()["Items"]
      for item in items:
        ids[item["Id"]] = 1
      page += 1
      if page >= response.json()["PagingInfo"]["TotalItems"] // 200:
        break
  
  products = []
  id_keys = list(ids.keys())
  for id_i in range(0, len(id_keys), 20):
    url = DETAIL_URL.format(ids=",".join(id_keys[id_i : id_i + 20]))
    response = session.get(url, headers=HEADERS)
    products += response.json()["Products"]

  #with open("results/Microsoft_Store.json", "w", -1, "utf-8") as f:
  #  json.dump(products, f, ensure_ascii=False, indent=2)
  
  return products

def parse(products):
  results = {}
  for game in products:
    # 检查是否为bundle
    if any([sku["Sku"]["Properties"]["IsBundle"] for sku in game["DisplaySkuAvailabilities"]]):
      continue
    product_id = game["ProductId"].strip().lower()
    release_date = game["MarketProperties"][0]["OriginalReleaseDate"][: 4]
    results[product_id] = {
      "id": product_id,
      "name": (game["LocalizedProperties"][0]["ShortTitle"] or game["LocalizedProperties"][0]["ProductTitle"]).replace("™", "").replace("®", "").replace("\n", " ").strip(),
      "desc": f'{release_date} video game by {game["LocalizedProperties"][0]["PublisherName"]}'.replace("  ", " "),
      # "url": f'https://www.microsoft.com/p/-/{product_id}',
      "type": "Q7889",
      "P437": "Q54820071",
      "P750": "Q135288"
    }

  results_list = sorted(results, key=lambda x:results[x]["name"])

  with open("results/Microsoft_Store.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(results[results_list[0]].keys()) + "\n")
    for game in results_list:
      game = results[game]
      f.write("\t".join(game.values()) + "\n")

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  parse(download())
