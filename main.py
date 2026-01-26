import os
import threading
import traceback


def run_python(file_name):
  try:
    os.system(f'python "{file_name}"')
  except Exception as e:
    print(f"Error: {file_name} {e}")
    print(traceback.format_exc())


FILE_NAMES = [
  "Nintendo_eShop.py",
  # "Microsoft_Store.py",
  # "Famitsu.py",
  "HowLongToBeat.py",
  # "Moegirlpedia.py",
  "PCGamingWiki.py",
  "StrategyWiki.py",
  "Super_Mario_Wiki.py",
  "VNDB.py",
  "MetaCritic.py",
  "OpenCritic.py",
]

threads = [threading.Thread(target=run_python, args=(file_name,)) for file_name in FILE_NAMES]
for thread in threads:
  thread.start()
for thread in threads:
  thread.join()
