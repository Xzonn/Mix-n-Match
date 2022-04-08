from _mediawiki import parse, download

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  parse(download("https://www.pcgamingwiki.com/w/api.php?format=json", "https://www.pcgamingwiki.com/wiki/", "Category:Games"), "PCGamingWiki.txt")