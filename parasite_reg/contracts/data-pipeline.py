import hashlib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor
from retry import retry

# Enhanced data structures
class ParasiteStatus(Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    UPDATED = "Updated"

@dataclass
class ParasiteRecord:
    parasite_name: str
    classification: str
    location: str
    metadata: Dict[str, Any]
    researcher: str
    institution: str
    status: ParasiteStatus = ParasiteStatus.ACTIVE
    version: int = 1
    previous_version: Optional[int] = None

class ParasiteDataPipeline:
    def __init__(self, stacks_api_url: str, ipfs_gateway: str):
        self.stacks_api_url = stacks_api_url
        self.ipfs_gateway = ipfs_gateway
        self.contract_address = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
        self.contract_name = "parasite-registry-v2"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize cache
        self.cache = {}

    @retry(tries=3, delay=1)
    async def prepare_parasite_data(self, 
                                  record: ParasiteRecord,
                                  additional_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Enhanced data preparation with IPFS support and validation
        """
        try:
            # Validate input data
            self._validate_record(record)
            
            # Process additional files if provided
            ipfs_hashes = []
            if additional_files:
                ipfs_hashes = await self._process_additional_files(additional_files)
            
            # Create complete metadata
            metadata = {
                "parasite_name": record.parasite_name,
                "classification": record.classification,
                "location": record.location,
                "timestamp": datetime.utcnow().isoformat(),
                "researcher": record.researcher,
                "institution": record.institution,
                "version": record.version,
                "additional_data": record.metadata,
                "ipfs_files": ipfs_hashes
            }
            
            # Generate metadata hash
            metadata_hash = hashlib.sha256(
                json.dumps(metadata, sort_keys=True).encode()
            ).hexdigest()
            
            return {
                "metadata": metadata,
                "metadata_hash": metadata_hash
            }
            
        except Exception as e:
            self.logger.error(f"Error preparing parasite data: {str(e)}")
            raise

    async def submit_to_blockchain(self, 
                                 prepared_data: Dict[str, Any],
                                 update_existing: Optional[int] = None) -> str:
        """
        Enhanced blockchain submission with version control
        """
        try:
            function_name = "update-parasite-record" if update_existing else "add-parasite-record"
            
            contract_call = {
                "contract_address": self.contract_address,
                "contract_name": self.contract_name,
                "function_name": function_name,
                "function_args": [
                    prepared_data["metadata"]["parasite_name"],
                    prepared_data["metadata"]["classification"],
                    prepared_data["metadata"]["location"],
                    prepared_data["metadata_hash"]
                ]
            }
            
            if update_existing:
                contract_call["function_args"].insert(0, update_existing)
            
            # Submit to blockchain (implementation would use actual Stacks API)
            return f"Transaction submitted with metadata hash: {prepared_data['metadata_hash']}"
            
        except Exception as e:
            self.logger.error(f"Error submitting to blockchain: {str(e)}")
            raise

    async def analyze_geographic_distribution(self) -> pd.DataFrame:
        """
        New: Analyze geographic distribution of parasites
        """
        try:
            # Fetch all records (implementation would use actual blockchain data)
            records = await self._fetch_all_records()
            
            # Create DataFrame for analysis
            df = pd.DataFrame(records)
            
            # Analyze geographic distribution
            distribution = df.groupby('location').agg({
                'record_id': 'count',
                'classification': lambda x: list(set(x)),
                'date_recorded': 'max'
            }).reset_index()
            
            return distribution
            
        except Exception as e:
            self.logger.error(f"Error analyzing geographic distribution: {str(e)}")
            raise

    async def get_record_history(self, record_id: int) -> List[Dict[str, Any]]:
        """
        New: Fetch complete history of a record
        """
        try:
            history = []
            current_id = record_id
            
            while current_id:
                record = await self._fetch_record(current_id)
                history.append(record)
                current_id = record.get('previous_version')
            
            return history
            
        except Exception as e:
            self.logger.error(f"Error fetching record history: {str(e)}")
            raise

    def _validate_record(self, record: ParasiteRecord) -> None:
        """
        Validate parasite record data
        """
        if not record.parasite_name or not record.classification or not record.location:
            raise ValueError("Missing required fields in parasite record")
        
        if not isinstance(record.metadata, dict):
            raise ValueError("Metadata must be a dictionary")

    async def _process_additional_files(self, files: List[str]) -> List[str]:
        """
        Process and upload additional files to IPFS
        """
        with ThreadPoolExecutor() as executor:
            ipfs_hashes = list(executor.map(self._upload_to_ipfs, files))
        return ipfs_hashes

    def _upload_to_ipfs(self, file_path: str) -> str:
        """
        Upload file to IPFS (mock implementation)
        """
        return f"ipfs_hash_{hashlib.md5(file_path.encode()).hexdigest()}"

# Example usage
async def main():
    pipeline = ParasiteDataPipeline(
        "https://stacks-node-api.mainnet.stacks.co",
        "https://ipfs.io"
    )
    
    # Create sample record
    record = ParasiteRecord(
        parasite_name="Plasmodium falciparum",
        classification="Apicomplexan",
        location="Sub-Saharan Africa",
        metadata={
            "resistance_profile": "chloroquine-resistant",
            "prevalence": "high",
            "year_identified": 2024,
            "genome_sequence": "ATCG...",
            "treatment_protocols": ["artemisinin-based", "combination therapy"]
        },
        researcher="DR_SMITH",
        institution="WHO_AFRICA"
    )
    
    # Prepare and submit data
    prepared_data = await pipeline.prepare_parasite_data(record, ["genome_data.fastq"])
    result = await pipeline.submit_to_blockchain(prepared_data)
    
    # Analyze geographic distribution
    distribution = await pipeline.analyze_geographic_distribution()
    print(f"Geographic Distribution:\n{distribution}")
    
    # Get record history
    history = await pipeline.get_record_history(1)
    print(f"Record History:\n{json.dumps(history, indent=2)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())