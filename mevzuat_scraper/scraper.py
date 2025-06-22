# Get Cookies & Auth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Send Request
import requests

# Process Data
# import json
# import os

# Logging
from loguru import logger

class Mevzuat:
    def __init__(self, post_url="https://www.mevzuat.gov.tr/Anasayfa/MevzuatDatatable"):
        self._get_driver()
        self._get_auth()
        self._init_metadata()
        self.post_url = post_url
    
    def request(self, mev_tur="Kanun", start=0, length=100):
        payload = self._get_payload(mev_tur, start, length)
        # logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(
                self.post_url,
                headers=self.headers,
                cookies=self.cookies,
                json=payload
            )
            response.raise_for_status()  # Raise an error for bad responses
            logger.info("✅ Request successful")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"🛑 Request failed: {e}")
            return None

    def _get_auth(self):
        try:
            URL = "https://www.mevzuat.gov.tr/#kanunlar"
            self.driver.get(URL)

            # 1. wait for the hidden antiforgerytoken input to show up
            elm = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "antiforgerytoken"))
            )
            self.token = elm.get_attribute("value")
            logger.info(f"✅ Got the token: {self.token[:5]}…")  # preview

            # 2. grab cookies from the browser and convert them to a dict
            self.cookies = {c["name"]: c["value"] for c in self.driver.get_cookies()}
            logger.debug(f"cookies sent : {', '.join(list(self.cookies)[:3])}…")
        except:
            logger.warning("🛑 Couldn't get Cookies || Auth")

        finally:
            self.driver.quit()   # always close the browser
    
    def _get_driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")         # Chrome ≥ 109
            options.add_argument("--window-size=1200,800") # (helps some CSPs)
            self.driver = webdriver.Chrome(options)
            logger.info("✅ Chrome Driver is ready")
        except Exception as e:
            logger.error(f"🛑 Error while initializing Chrome Driver: {e}")
            raise
    
    def _get_payload(self, mev_tur="Kanun", start=0, length=100):
        return {
            "draw": 1,
            "columns": [
                { "data": None, "name": "", "searchable": True,
                "orderable": False, "search": { "value": "", "regex": False } }
            ] * 3,
            "order": [],
            "start": start,
            "length": length,
            "search": { "value": "", "regex": False },
            "parameters": {
                "MevzuatTur": mev_tur,
                "YonetmelikMevzuatTur": "OsmanliKanunu",
                "AranacakIfade": "sa",
                "AranacakYer": "3",
                "MevzuatNo": "",
                "BaslangicTarihi": "",
                "BitisTarihi": "",
                "antiforgerytoken": self.token
            }
        }

    def _init_metadata(self):
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.mevzuat.gov.tr",
            "Referer": "https://www.mevzuat.gov.tr/",
            "User-Agent": "Mozilla/5.0 (scraper via Selenium)",
        }