# Mevzuat Scraper with Hugging Face Integration

This project scrapes Turkish legislation documents from mevzuat.gov.tr and provides functionality to upload the collected data to Hugging Face Hub as datasets.

## Features

- Scrapes Turkish legislation documents (Kanunlar, etc.)
- Cleans and processes the text data
- Uploads tabular data to Hugging Face Hub
- Supports multiple dataset splits (train/test/validation)
- Automatic data cleaning and formatting

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Hugging Face credentials:**
   - Create an account at [huggingface.co](https://huggingface.co)
   - Generate an API token at [Settings > Access Tokens](https://huggingface.co/settings/tokens)
   - Set the token as an environment variable:
     ```bash
     export HF_TOKEN='your_token_here'
     ```

3. **Configure the scraper:**
   - Update the configuration in `config/config.py` as needed
   - In `main.py` and `example_usage.py`, replace `your-username` with your actual Hugging Face username

## Usage

### Basic Scraping and Upload

Run the main scraper with automatic Hugging Face upload:

```bash
python main.py
```

This will:
- Scrape legislation documents
- Save them locally as JSON files
- Automatically upload batches to Hugging Face Hub (if HF_TOKEN is set)

### Using the HuggingfacePusher Class

```python
from mevzuat_scraper.pusher import HuggingfacePusher

# Initialize the pusher
pusher = HuggingfacePusher()

# Upload data from JSON file
dataset_url = pusher.push_data(
    data="out.json",
    repo_id="username/turkish-legislation",
    split_name="train"
)

# Upload data from list of dictionaries
data = [
    {
        "text": "Law text content...",
        "title": "Law Title",
        "mevzuat_no": "7557",
        "mvzuat_turu": "Kanunlar"
    }
]

dataset_url = pusher.push_data(
    data=data,
    repo_id="username/my-dataset"
)

# Upload multiple splits
pusher.push_multiple_splits(
    data_dict={
        "train": train_data,
        "test": test_data,
        "validation": val_data
    },
    repo_id="username/dataset-with-splits"
)
```

### Example Usage

See `example_usage.py` for comprehensive examples:

```bash
python example_usage.py
```

## Data Format

The scraper collects Turkish legislation documents with the following structure:

```json
{
    "text": "Full text content of the legislation",
    "title": "Official title of the law",
    "url": "Source URL from mevzuat.gov.tr",
    "url_params": "URL parameters",
    "mevzuat_no": "Official law number",
    "resmi_g_tarih": "Official Gazette date",
    "resmi_g_sayisi": "Official Gazette number",
    "mvzuat_turu": "Type of legislation (e.g., 'Kanunlar')"
}
```

## HuggingfacePusher Class Methods

### `__init__(HF_TOKEN=None)`
Initialize the pusher with Hugging Face token.

### `push_data(data, repo_id, split_name="train", private=False, commit_message=None)`
Push tabular data to Hugging Face Hub.

**Parameters:**
- `data`: List of dicts, JSON file path, or pandas DataFrame
- `repo_id`: Repository ID (e.g., "username/dataset-name")
- `split_name`: Dataset split name (default: "train")
- `private`: Whether to create private repository
- `commit_message`: Custom commit message

### `push_multiple_splits(data_dict, repo_id, private=False, commit_message=None)`
Push multiple data splits to a single repository.

**Parameters:**
- `data_dict`: Dictionary mapping split names to data
- `repo_id`: Repository ID
- `private`: Whether to create private repository
- `commit_message`: Custom commit message

### `update_dataset(data, repo_id, split_name="train", commit_message=None)`
Update an existing dataset with new data.

### `get_dataset_info(repo_id)`
Get information about an existing dataset.

## Data Cleaning

The pusher automatically:
- Removes empty rows
- Normalizes text formatting (removes `\r\n`, excessive whitespace)
- Fills missing values appropriately
- Sorts data by legislation number
- Ensures proper data types

## File Structure

```
mevzuat-scraper/
├── config/
│   └── config.py
├── mevzuat_scraper/
│   ├── scraper.py
│   └── pusher.py          # HuggingfacePusher class
├── main.py                # Main scraper with HF integration
├── example_usage.py       # Usage examples
├── requirements.txt       # Dependencies
└── out.json              # Sample output data
```

## Dependencies

Key dependencies for Hugging Face functionality:
- `datasets` - Hugging Face datasets library
- `huggingface-hub` - Hugging Face Hub API
- `pandas` - Data manipulation
- `python-dotenv` - Environment variable management

## Error Handling

The pusher includes comprehensive error handling and logging:
- Validates input data formats
- Provides informative error messages
- Logs all operations for debugging
- Gracefully handles missing HF_TOKEN

## License

This project is open source. Please check the license file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
