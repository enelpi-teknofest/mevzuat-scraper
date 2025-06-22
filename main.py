from mevzuat_scraper.scraper import Mevzuat
from config.config import Config

def main():
    mevzuat = Mevzuat()
    mev_tur = Config().mevzuat_turleri[0]  # Example: 'Kanun'
    start = 0          # Starting index for pagination
    length = 100       # Number of records to fetch

    response = mevzuat.request(mev_tur=mev_tur, start=start, length=length)
    
    if response:
        print("Response received successfully.")
        print(response)  # or process the response as needed
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()