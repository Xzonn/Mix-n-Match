from _mediawiki import parse, download

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  parse(download("https://www.mariowiki.com/api.php?format=json", "https://www.mariowiki.com/", "Category:Games"), "Super_Mario_Wiki.txt")