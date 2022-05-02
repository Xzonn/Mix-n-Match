import time
from _mediawiki import parse, download, login

if __name__ == "__main__":
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  login("https://zh.moegirl.org.cn/api.php?format=json", os.environ["MOEGIRLPEDIA_BOT_NAME"], os.environ["MOEGIRLPEDIA_BOT_PASS"])
  results = {}
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:中国游戏作品", desc="Chinese video game", sleep=True))
  time.sleep(5)
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:日本游戏作品", desc="Japanese video game", sleep=True))
  time.sleep(5)
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:美国游戏作品", desc="American video game", sleep=True))
  time.sleep(5)
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:日本动画作品", "Q63952888", "Japanese anime series", True))
  time.sleep(5)
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:日本漫画作品", "Q21198342", "Japanese manga series", True))
  time.sleep(5)
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:日本小说作品", "Q104213567", "Japanese novel series", True))
  time.sleep(5)
  results.update(download("https://zh.moegirl.org.cn/api.php?format=json", "https://zh.moegirl.org.cn/", "Category:声优", "Q5", "seiyū/voice actor/voice actress", True))
  parse(results, "Moegirlpedia.txt")