"""
pip install selenium webdriver-manager requests bs4
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import requests
import json
import sys

# ─────────────────────────────────────────────────────────────
# 1. spin up a headless Chrome controlled by Selenium
# ─────────────────────────────────────────────────────────────
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")         # Chrome ≥ 109
options.add_argument("--window-size=1200,800") # (helps some CSPs)
driver = webdriver.Chrome(options)

mev_tur = ['Kanun', 'CumhurbaskaniKararnameleri', 
           'CumhurbaskanligiVeBakanlarKuruluYonetmelik', 
           'CumhurbaskaniKararlari', 'CumhurbaskanligiGenelgeleri',
           'KHK', 'Tuzuk', 'KurumVeKurulusYonetmeligi',
           'Teblig']

try:
    # ─────────────────────────────────────────────────────────
    # 2. visit the Kanunlar page (creates the session + sets cookies)
    # ─────────────────────────────────────────────────────────
    URL = "https://www.mevzuat.gov.tr/#kanunlar"
    driver.get(URL)

    # 3. wait for the hidden antiforgerytoken input to show up
    elm = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "antiforgerytoken"))
    )
    token = elm.get_attribute("value")
    print(f"fresh token  : {token[:20]}…")  # preview

    # 4. grab cookies from the browser and convert them to a dict
    cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
    print(f"cookies sent : {', '.join(list(cookies)[:3])}…")

finally:
    driver.quit()   # always close the browser

# ─────────────────────────────────────────────────────────────
# 5. build the JSON payload (as seen in DevTools) with the new token
# ─────────────────────────────────────────────────────────────
payload = {
    "draw": 1,
    "columns": [
        { "data": None, "name": "", "searchable": True,
          "orderable": False, "search": { "value": "", "regex": False } }
    ] * 3,
    "order": [],
    "start": 0,
    "length": 100,
    "search": { "value": "", "regex": False },
    "parameters": {
        "MevzuatTur": mev_tur[-1],
        "YonetmelikMevzuatTur": "OsmanliKanunu",
        "AranacakIfade": "sa",
        "AranacakYer": "3",
        "MevzuatNo": "",
        "BaslangicTarihi": "",
        "BitisTarihi": "",
        "antiforgerytoken": token          # ⭐️ freshly scraped token
    }
}

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.mevzuat.gov.tr",
    "Referer": "https://www.mevzuat.gov.tr/",
    "User-Agent": "Mozilla/5.0 (scraper via Selenium)",
}

# ─────────────────────────────────────────────────────────────
# 6. send the request via requests, re-using cookies
# ─────────────────────────────────────────────────────────────
POST_URL = "https://www.mevzuat.gov.tr/Anasayfa/MevzuatDatatable"

resp = requests.post(
    POST_URL,
    headers=headers,
    cookies=cookies,      # carries the .AspNetCore.* cookies from Selenium
    json=payload,
    timeout=20
)
resp.raise_for_status()

print("status       :", resp.status_code)
# print("first 500 B  :", resp.text[:500])   # or resp.json() for parsed data
print("JSON:\n", resp.json())   # or resp.json() for parsed data
