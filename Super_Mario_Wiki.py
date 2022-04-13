from _mediawiki import parse, download

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  results = {}
  results.update(download("https://www.mariowiki.com/api.php?format=json", "https://www.mariowiki.com/", "Category:Games"))
  results.update(download("https://www.mariowiki.com/api.php?format=json", "https://www.mariowiki.com/", "Category:Game_series", "Q7058673", "video game series"))
  results.update(download("https://www.mariowiki.com/api.php?format=json", "https://www.mariowiki.com/", "Category:People", "Q5", "human"))
  results.update(download("https://www.mariowiki.com/api.php?format=json", "https://www.mariowiki.com/", "Category:Companies", "Q4830453", "company"))
  parse(results, "Super_Mario_Wiki.txt")