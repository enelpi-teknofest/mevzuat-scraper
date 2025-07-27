from dotenv import load_dotenv
import os
import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi
import json
from typing import List, Dict, Union, Optional
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingfacePusher:
    """
    A class to push tabular data to Hugging Face Hub as datasets.
    Specifically designed for Turkish legislation/law documents.
    """

    def __init__(self, HF_TOKEN: Optional[str] = None):
        """
        Initialize the HuggingfacePusher with authentication token.
        
        Args:
            HF_TOKEN: Hugging Face API token. If None, tries to get from environment.
        """
        self.token = HF_TOKEN or os.environ.get('HF_TOKEN')
        if not self.token:
            raise Exception("Please provide a Hugging Face token via HF_TOKEN parameter or environment variable")
        
        self.api = HfApi(token=self.token)
        logger.info("HuggingfacePusher initialized successfully")

    def prepare_dataset(self, data: Union[List[Dict], str, pd.DataFrame]) -> Dataset:
        """
        Prepare the data as a Hugging Face Dataset.
        
        Args:
            data: Input data - can be a list of dictionaries, JSON file path, or pandas DataFrame
            
        Returns:
            Dataset: Hugging Face Dataset object
        """
        # Handle different input types
        if isinstance(data, str):
            # Assume it's a file path
            logger.info(f"Loading data from file: {data}")
            with open(data, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        if isinstance(data, list):
            # Convert list of dictionaries to pandas DataFrame
            logger.info(f"Converting {len(data)} records to DataFrame")
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError("Data must be a list of dictionaries, file path, or pandas DataFrame")
        
        # Clean and prepare the data
        df = self._clean_dataframe(df)
        
        # Convert to Hugging Face Dataset
        dataset = Dataset.from_pandas(df)
        logger.info(f"Created dataset with {len(dataset)} rows and {len(dataset.column_names)} columns")
        
        return dataset

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare the DataFrame for Hugging Face upload.
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        # Fill NaN values with empty strings for text columns
        text_columns = ['text', 'title', 'url', 'url_params', 'mvzuat_turu']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('')
        
        # Clean text data - remove excessive whitespace and normalize
        if 'text' in df.columns:
            df['text'] = df['text'].str.replace(r'\r\n', '\n', regex=True)
            df['text'] = df['text'].str.replace(r'\r', '\n', regex=True)
            df['text'] = df['text'].str.strip()
        
        if 'title' in df.columns:
            df['title'] = df['title'].str.strip()
        
        # Ensure mevzuat_no is string type
        if 'mevzuat_no' in df.columns:
            df['mevzuat_no'] = df['mevzuat_no'].astype(str)
        
        # Sort by mevzuat_no if available
        if 'mevzuat_no' in df.columns:
            df = df.sort_values('mevzuat_no')
        
        logger.info("DataFrame cleaned and prepared")
        return df

    def push_data(self, 
                  data: Union[List[Dict], str, pd.DataFrame], 
                  repo_id: str,
                  split_name: str = "train",
                  private: bool = False,
                  commit_message: Optional[str] = None) -> str:
        """
        Push tabular data to Hugging Face Hub as a dataset.
        
        Args:
            data: Input data to push
            repo_id: Repository ID on Hugging Face Hub (e.g., "username/dataset-name")
            split_name: Name of the dataset split (default: "train")
            private: Whether to create a private repository
            commit_message: Custom commit message
            
        Returns:
            str: URL to the uploaded dataset
        """
        try:
            # Prepare the dataset
            dataset = self.prepare_dataset(data)
            
            # Create DatasetDict if needed
            if split_name:
                dataset_dict = DatasetDict({split_name: dataset})
            else:
                dataset_dict = DatasetDict({"train": dataset})
            
            # Set default commit message
            if not commit_message:
                commit_message = f"Upload Turkish legislation dataset with {len(dataset)} documents"
            
            logger.info(f"Pushing dataset to {repo_id}")
            
            # Push to hub
            dataset_dict.push_to_hub(
                repo_id=repo_id,
                private=private,
                token=self.token,
                commit_message=commit_message
            )
            
            dataset_url = f"https://huggingface.co/datasets/{repo_id}"
            logger.info(f"Dataset successfully pushed to: {dataset_url}")
            
            return dataset_url
            
        except Exception as e:
            logger.error(f"Error pushing data to Hugging Face: {str(e)}")
            raise
    
    def update_dataset(self, 
                      data: Union[List[Dict], str, pd.DataFrame],
                      repo_id: str,
                      split_name: str = "train",
                      commit_message: Optional[str] = None) -> str:
        """
        Update an existing dataset with new data.
        
        Args:
            data: New data to add/update
            repo_id: Existing repository ID
            split_name: Split to update
            commit_message: Custom commit message
            
        Returns:
            str: URL to the updated dataset
        """
        return self.push_data(
            data=data,
            repo_id=repo_id,
            split_name=split_name,
            private=False,  # Existing repo privacy will be maintained
            commit_message=commit_message or f"Update dataset with new data"
        )
    
    def push_multiple_splits(self,
                           data_dict: Dict[str, Union[List[Dict], str, pd.DataFrame]],
                           repo_id: str,
                           private: bool = False,
                           commit_message: Optional[str] = None) -> str:
        """
        Push multiple data splits to a single dataset repository.
        
        Args:
            data_dict: Dictionary mapping split names to data
            repo_id: Repository ID on Hugging Face Hub
            private: Whether to create a private repository
            commit_message: Custom commit message
            
        Returns:
            str: URL to the uploaded dataset
        """
        try:
            dataset_dict = DatasetDict()
            
            for split_name, split_data in data_dict.items():
                logger.info(f"Preparing split: {split_name}")
                dataset = self.prepare_dataset(split_data)
                dataset_dict[split_name] = dataset
            
            if not commit_message:
                total_rows = sum(len(ds) for ds in dataset_dict.values())
                commit_message = f"Upload multi-split dataset with {total_rows} total documents"
            
            logger.info(f"Pushing multi-split dataset to {repo_id}")
            
            dataset_dict.push_to_hub(
                repo_id=repo_id,
                private=private,
                token=self.token,
                commit_message=commit_message
            )
            
            dataset_url = f"https://huggingface.co/datasets/{repo_id}"
            logger.info(f"Multi-split dataset successfully pushed to: {dataset_url}")
            
            return dataset_url
            
        except Exception as e:
            logger.error(f"Error pushing multi-split data: {str(e)}")
            raise
    
    def get_dataset_info(self, repo_id: str) -> Dict:
        """
        Get information about an existing dataset.
        
        Args:
            repo_id: Repository ID
            
        Returns:
            Dict: Dataset information
        """
        try:
            repo_info = self.api.repo_info(repo_id, repo_type="dataset", token=self.token)
            return {
                "id": repo_info.id,
                "private": repo_info.private,
                "downloads": repo_info.downloads,
                "tags": repo_info.tags,
                "created_at": repo_info.created_at,
                "last_modified": repo_info.last_modified
            }
        except Exception as e:
            logger.error(f"Error getting dataset info: {str(e)}")
            raise