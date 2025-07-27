from mevzuat_scraper.scraper import Mevzuat
from config.config import Config

def main():
    mevzuat = Mevzuat()
    mev_tur = Config().mevzuat_turleri[0]  # Example: 'Kanun'
    start = 0          # Starting index for pagination
    length = 100       # Number of records to fetch

    metadata = mevzuat.request(mev_tur=mev_tur, start=start, length=length)
    metadata = mevzuat.request_text(metadata)

if __name__ == "__main__":
    main()