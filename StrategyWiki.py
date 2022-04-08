from _mediawiki import parse, download

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  parse(download("https://strategywiki.org/w/api.php?format=json", "https://strategywiki.org/wiki/", "Category:Games"), "StrategyWiki.txt")