import re


PLATFORMS = {
  "PC": "Q1406",
  "Switch": "Q19610114",
  "Wii U": "Q56942",
  "WiiU": "Q56942",
  "3DS": "Q203597",
  "PS4": "Q5014725",
  "PS5": "Q63184502",
  "Xbox Series X": "Q98973368",
  "XSX": "Q98973368",
  "Xbox One": "Q13361286",
  "XOne": "Q13361286",
}

ESRB = {
  "EC": "Q14864327",
  "E": "Q14864328",
  "E10": "Q14864329",
  "T": "Q14864330",
  "M": "Q14864331",
  "AO": "Q14864332",
  "RP": "Q14864333",
}

ESRB_DESCRIPTORS = {
  "Alcohol and Tobacco Reference": "Q99904297",
  "Alcohol Reference": "Q60316458",
  "Animated Blood": "Q60316460",
  "Animated Blood and Gore": "Q69577075",
  "Animated Violence": "Q69577345",
  "Blood": "Q60316463",
  "Blood and Gore": "Q60316461",
  "Cartoon Violence": "Q60316462",
  "Comic Mischief": "Q60316464",
  "Crude Humor": "Q60300344",
  "Digital Purchases": "Q102110695",
  "Diverse Content Discretion Advised": "Q123653389",
  "Drug and Alcohol Reference": "Q110343784",
  "Drug Reference": "Q60317579",
  "Edutainment": "Q60300293",
  "Fantasy Violence": "Q60317581",
  "Fine Motor Skills": "Q98556733",
  "Gambling": "Q97543276",
  "Game Experience May Change During Online Play": "Q97302889",
  "Gaming": "Q103531650",
  "Higher-Level Thinking Skills": "Q98556734",
  "In-App Purchases": "Q106097196",
  "Includes Demo of a Game Not Yet Rated by ESRB": "Q98088300",
  "Includes Demos rated Rating Pending to Teen by the ESRB": "Q98088301",
  "Informational": "Q60724353",
  "In-Game Purchases": "Q69991173",
  "In-Game Purchases (Includes Random Items)": "Q90412335",
  "Intense Violence": "Q60317584",
  "Language": "Q60317586",
  "Lyrics": "Q60317587",
  "Mature Humor": "Q60317589",
  "Mature Sexual Themes": "Q69821734",
  "Mild Alcohol Reference": "Q97578625",
  "Mild Animated Violence": "Q97656786",
  "Mild Blood": "Q77315029",
  "Mild Cartoon Violence": "Q69993985",
  "Mild Fantasy Violence": "Q70002023",
  "Mild Language": "Q68205918",
  "Mild Lyrics": "Q96310546",
  "Mild Realistic Violence": "Q97656787",
  "Mild Sexual Themes": "Q97585290",
  "Mild Strong Language": "Q98269045",
  "Mild Suggestive Themes": "Q72415417",
  "Mild Use of Alcohol": "Q97578141",
  "Mild Use of Drugs": "Q97579457",
  "Mild Violence": "Q60324381",
  "Mild violent references": "Q102110675",
  "Music downloads not rated by the ESRB.": "Q96220171",
  "Nudity": "Q60324383",
  "Online interactions not rated by the ESRB.": "Q68183722",
  "Online Music Not Rated by the ESRB": "Q96220186",
  "Partial Nudity": "Q60300245",
  "Reading Skills": "Q98556732",
  "Real Gambling": "Q60324384",
  "Realistic Blood": "Q98556739",
  "Realistic Blood and Gore": "Q69582662",
  "Realistic Violence": "Q69583053",
  "Sexual Content": "Q69578048",
  "Sexual Themes": "Q60324385",
  "Sexual Violence": "Q60324386",
  "Shares Info": "Q97363751",
  "Shares Location": "Q69430054",
  "Simulated Gambling": "Q60324387",
  "Some Adult Assistance May Be Needed": "Q60324422",
  "Strong Language": "Q60300342",
  "Strong Lyrics": "Q60324421",
  "Strong Sexual Content": "Q60324423",
  "Strong Sexual Themes": "Q97061867",
  "Strong Violence": "Q102110867",
  "Suggestive Themes": "Q60324424",
  "Tobacco Reference": "Q60324425",
  "Unrestricted Internet": "Q69430020",
  "Use of Alcohol": "Q60324427",
  "Use of Alcohol and Tobacco": "Q96337561",
  "Use of Drugs": "Q60324426",
  "Use of Drugs and Alcohol": "Q86235040",
  "Use of Drugs and Tobacco": "Q124356179",
  "Use of Tobacco": "Q60324428",
  "Users Interact": "Q69430207",
  "Violence": "Q60324429",
  "Violent References": "Q69573910",
}

def parse_title(original_title: str) -> str:
  if not original_title:
    return ""
  title = re.sub(r"[ \t\n\u200B]+", " ", original_title.replace("™", " ").replace("®", " ")).replace(" :", ":").strip()
  return title