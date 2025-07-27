#!/usr/bin/env python3
"""
Example usage of the HuggingfacePusher class for pushing Turkish legislation data to Hugging Face Hub.
"""

from mevzuat_scraper.pusher import HuggingfacePusher
import json
import os

def main():
    """
    Example demonstrating how to use HuggingfacePusher to upload the scraped mevzuat data.
    """
    
    # Initialize the pusher (make sure HF_TOKEN is set in your environment)
    try:
        pusher = HuggingfacePusher()
        print("✓ HuggingfacePusher initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing pusher: {e}")
        print("Make sure to set your HF_TOKEN environment variable")
        return
    
    # Example 1: Push data from the out.json file
    print("\n📤 Example 1: Pushing data from out.json file")
    try:
        dataset_url = pusher.push_data(
            data="out.json",  # Path to your JSON file
            repo_id="turkish-legislation",  # Replace with your HF username
            split_name="train",
            private=False,  # Set to True if you want a private dataset
            commit_message="Initial upload of Turkish legislation dataset"
        )
        print(f"✓ Dataset uploaded successfully: {dataset_url}")
    except Exception as e:
        print(f"❌ Error uploading dataset: {e}")
    
    # Example 2: Push data from a list of dictionaries
    print("\n📤 Example 2: Pushing sample data from list")
    sample_data = [
        {
            "text": "Sample Turkish law text...",
            "title": "Sample Law Title",
            "url": "https://example.com",
            "mevzuat_no": "7557",
            "mvzuat_turu": "Kanunlar"
        },
        # Add more sample data as needed
    ]
    
    try:
        dataset_url = pusher.push_data(
            data=sample_data,
            repo_id="sample-legislation",  # Replace with your HF username
            split_name="train",
            private=True,  # Private repo for testing
            commit_message="Upload sample legislation data"
        )
        print(f"✓ Sample dataset uploaded: {dataset_url}")
    except Exception as e:
        print(f"❌ Error uploading sample dataset: {e}")
    
    # Example 3: Push multiple splits (train/test/validation)
    print("\n📤 Example 3: Pushing multiple splits")
    try:
        # Load your data and split it appropriately
        with open("out.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
        
        # Simple split: 80% train, 20% test
        split_point = int(len(all_data) * 0.8)
        train_data = all_data[:split_point]
        test_data = all_data[split_point:]
        
        dataset_url = pusher.push_multiple_splits(
            data_dict={
                "train": train_data,
                "test": test_data
            },
            repo_id="turkish-legislation-split",  # Replace with your HF username
            private=False,
            commit_message="Upload train/test split of Turkish legislation"
        )
        print(f"✓ Multi-split dataset uploaded: {dataset_url}")
    except FileNotFoundError:
        print("❌ out.json file not found - run the scraper first")
    except Exception as e:
        print(f"❌ Error uploading multi-split dataset: {e}")
    
    # Example 4: Get dataset information
    print("\n📊 Example 4: Getting dataset information")
    try:
        info = pusher.get_dataset_info("your-username/turkish-legislation")
        print(f"✓ Dataset info retrieved:")
        print(f"  - Downloads: {info.get('downloads', 'N/A')}")
        print(f"  - Private: {info.get('private', 'N/A')}")
        print(f"  - Created: {info.get('created_at', 'N/A')}")
    except Exception as e:
        print(f"❌ Error getting dataset info: {e}")

def setup_instructions():
    """
    Print setup instructions for users.
    """
    print("🔧 Setup Instructions:")
    print("1. Create a Hugging Face account at https://huggingface.co")
    print("2. Generate an API token at https://huggingface.co/settings/tokens")
    print("3. Set the token as an environment variable:")
    print("   export HF_TOKEN='your_token_here'")
    print("4. Replace 'your-username' in the examples with your actual HF username")
    print("5. Install required dependencies: pip install -r requirements.txt")
    print()

if __name__ == "__main__":
    setup_instructions()
    
    # Check if HF_TOKEN is set
    if not os.environ.get('HF_TOKEN'):
        print("❌ HF_TOKEN environment variable not set!")
        print("Please set your Hugging Face token before running this example.")
        exit(1)
    
    main()
