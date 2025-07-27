from mevzuat_scraper.scraper import Mevzuat
from mevzuat_scraper.pusher import HuggingfacePusher
from config.config import Config
import datetime
import json
import os

def main():
    mevzuat = Mevzuat()
    mev_tur = Config().mevzuat_turleri[0]  # Example: 'Kanun'

    start = 0          # Starting index for pagination
    length = 10       # Number of records to fetch
    push_after = 100   # Push to HF after collecting this many records

    result = []
    metadata = mevzuat.request(mev_tur=mev_tur, start=start, length=length)
    
    # Initialize HuggingFace pusher if token is available
    hf_pusher = None
    if os.environ.get('HF_TOKEN'):
        try:
            hf_pusher = HuggingfacePusher()
            print("✓ HuggingFace pusher initialized")
        except Exception as e:
            print(f"⚠️  HuggingFace pusher failed to initialize: {e}")
    else:
        print("⚠️  HF_TOKEN not set - skipping HuggingFace upload")
    
    batch_count = 0
    
    while metadata is not None:
        result.extend(metadata)
        start += length
        
        # Get full text content for the collected metadata
        if len(result) >= push_after:
            print(f"📄 Fetching full text for {len(result)} documents...")
            full_data = mevzuat.request_text(result)
            
            # Save to local file
            filename = f"{mev_tur}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = f"out/{filename}" if os.path.exists("out") else filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(full_data, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved {len(full_data)} documents to {filepath}")
            
            # Push to HuggingFace if available
            if hf_pusher:
                try:
                    batch_count += 1
                    repo_id = f"fikriokan/turkish-{mev_tur.lower()}-batch-{batch_count}"
                    dataset_url = hf_pusher.push_data(
                        data=full_data,
                        repo_id=repo_id,
                        commit_message=f"Batch {batch_count}: {len(full_data)} {mev_tur} documents"
                    )
                    print(f"🚀 Uploaded to HuggingFace: {dataset_url}")
                except Exception as e:
                    print(f"❌ Failed to upload to HuggingFace: {e}")
            
            # Reset for next batch
            result = []
        
        # Get next batch of metadata
        metadata = mevzuat.request(mev_tur=mev_tur, start=start, length=length)
    
    # Handle any remaining data
    if result:
        print(f"📄 Processing final batch of {len(result)} documents...")
        full_data = mevzuat.request_text(result)
        
        filename = f"{mev_tur}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_final.json"
        filepath = f"out/{filename}" if os.path.exists("out") else filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved final {len(full_data)} documents to {filepath}")
        
        if hf_pusher:
            try:
                batch_count += 1
                repo_id = f"your-username/turkish-{mev_tur.lower()}-final"
                dataset_url = hf_pusher.push_data(
                    data=full_data,
                    repo_id=repo_id,
                    commit_message=f"Final batch: {len(full_data)} {mev_tur} documents"
                )
                print(f"🚀 Uploaded final batch to HuggingFace: {dataset_url}")
            except Exception as e:
                print(f"❌ Failed to upload final batch to HuggingFace: {e}")

if __name__ == "__main__":
    main()