# Send Request
import requests

# Parsing
from bs4 import BeautifulSoup

# Logging
from loguru import logger

class Mevzuat:
    def __init__(self, post_url="https://www.mevzuat.gov.tr/Anasayfa/MevzuatDatatable"):
        self._init_metadata()
        self.post_url = post_url
        self.token = "sa"
    
    def request(self, mev_tur="Kanun", start=0, length=100):
        payload = self._get_payload(mev_tur, start, length)

        try:
            logger.info(f"⌛️ Requesting start: {start}, length: {length}, keyword: {mev_tur} ...")
            response = requests.post(
                self.post_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()  # Raise an error for bad responses
            logger.info("✅ Request successful")
            return self._clean_response(response.json())
        except requests.RequestException as e:
            logger.error(f"🛑 Request failed: {e}")
            return None

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
                "AranacakIfade": "a",
                "AranacakYer": "3",
                "MevzuatNo": "",
                "BaslangicTarihi": "",
                "BitisTarihi": "",
                "antiforgerytoken": self.token
            }
        }

    def _init_metadata(self):
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://www.mevzuat.gov.tr",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0.0.0 Safari/537.36"),
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
        }
    
    def _clean_response(self, j):
        data = j['data']
        return [
            dict(
                title=d['mevAdi'],
                url_params=d['url'].split('?')[-1],
                mevzuat_no=d['mevzuatNo'],
                resmi_g_tarih=d['resmiGazeteTarihi'],
                resmi_g_sayisi=d['resmiGazeteSayisi'],
                mvzuat_turu=d['mevzuatTurEnumString']
            ) for d in data
        ]
    
    def _request_text(
            self,
            post_url="https://www.mevzuat.gov.tr/anasayfa/MevzuatFihristDetayIframe?", 
            params="MevzuatNo=6713&MevzuatTur=1&MevzuatTertip=5"
        ):
        url = post_url + params
        # logger.debug(f"Retrieving Text From: {url}")
        response = requests.post(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body')
        text = body.get_text(strip=False) if body else None
        if not text:
            raise Exception("No text retrieved.")
        return url, text

    
    def request_text(self, metadata):
        data = []
        logger.info("⌛️ Requesting Text ...")
        for i, m in enumerate(metadata): ### DEBUGGING
            try:
                url, text = self._request_text(params=m['url_params'])
                data.append(
                    dict(
                        text=text,
                        url=url,
                        **m
                    )
                )
                logger.info(f"- ✅ Retrieved Text @ {i+1}, Text[:5] = {text[:5].strip()} ... ")
            except Exception as e:
                logger.error(f"An error occured while requesting text:\n {e}")
        return data