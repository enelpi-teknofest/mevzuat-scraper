import requests

url = "https://www.mevzuat.gov.tr/Anasayfa/MevzuatDatatable"

payload = {
    "draw": 1,
    "columns": [
        {"data": None, "name": "", "searchable": True, "orderable": False,
         "search": {"value": "", "regex": False}},
        {"data": None, "name": "", "searchable": True, "orderable": False,
         "search": {"value": "", "regex": False}},
        {"data": None, "name": "", "searchable": True, "orderable": False,
         "search": {"value": "", "regex": False}}
    ],
    "order": [],
    "start": 0,
    "length": 10,
    "search": {"value": "", "regex": False},
    "parameters": {
        "MevzuatTur": "Kanun",
        "YonetmelikMevzuatTur": "OsmanliKanunu",
        "AranacakIfade": "sa",
        "AranacakYer": "3",
        "MevzuatNo": "",
        "BaslangicTarihi": "",
        "BitisTarihi": "",
        # *** hard-coded anti-forgery token (works only for a short time!) ***
        "antiforgerytoken":
            "CfDJ8GZT_MP_neZPpJvMcEuCmFB6vx9QAVisckzNS5amaDR-"
            "Yx3N5ZkkCxHN5pgOZb9xbc9Tet0Qw86fiipwml-GhzCTXn261YmwfX78zdGABw"
            "nzyQCZyx7DS3Fsy5SvQZ91J-5Ky0c4fzQ4DAhwM8eWWFk"
    }
}

headers = {
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

resp = requests.post(url, headers=headers, json=payload, timeout=20)
resp.raise_for_status()          # raise if HTTP error
print(resp.json())               # the server’s JSON response

