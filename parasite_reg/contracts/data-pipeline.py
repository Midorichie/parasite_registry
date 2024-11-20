import hashlib
import json
from typing import Dict, Any
from datetime import datetime
import requests

class ParasiteDataPipeline:
    def __init__(self, stacks_api_url: str):
        self.stacks_api_url = stacks_api_url
        self.contract_address = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
        self.contract_name = "parasite-registry"

    def prepare_parasite_data(self, 
                            parasite_name: str,
                            classification: str,
                            location: str,
                            additional_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare parasite data for blockchain storage
        """
        # Create complete metadata
        metadata = {
            "parasite_name": parasite_name,
            "classification": classification,
            "location": location,
            "timestamp": datetime.utcnow().isoformat(),
            "additional_data": additional_metadata
        }
        
        # Generate metadata hash
        metadata_hash = hashlib.sha256(
            json.dumps(metadata, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            "metadata": metadata,
            "metadata_hash": metadata_hash
        }

    def submit_to_blockchain(self, prepared_data: Dict[str, Any]) -> str:
        """
        Submit prepared data to the Stacks blockchain
        """
        contract_call = {
            "contract_address": self.contract_address,
            "contract_name": self.contract_name,
            "function_name": "add-parasite-record",
            "function_args": [
                prepared_data["metadata"]["parasite_name"],
                prepared_data["metadata"]["classification"],
                prepared_data["metadata"]["location"],
                prepared_data["metadata_hash"]
            ]
        }
        
        # Note: In a real implementation, this would use the Stacks API
        # to submit the contract call transaction
        return f"Transaction submitted with metadata hash: {prepared_data['metadata_hash']}"

    def verify_record(self, record_id: int) -> Dict[str, Any]:
        """
        Verify a parasite record on the blockchain
        """
        # In real implementation, this would query the Stacks blockchain
        # to retrieve and verify the record
        response = {
            "verified": True,
            "record_id": record_id,
            "blockchain_timestamp": datetime.utcnow().isoformat()
        }
        return response

# Example usage
if __name__ == "__main__":
    pipeline = ParasiteDataPipeline("https://stacks-node-api.mainnet.stacks.co")
    
    # Example data
    sample_data = pipeline.prepare_parasite_data(
        parasite_name="Plasmodium falciparum",
        classification="Apicomplexan",
        location="Sub-Saharan Africa",
        additional_metadata={
            "resistance_profile": "chloroquine-resistant",
            "prevalence": "high",
            "year_identified": 2024
        }
    )
    
    # Submit to blockchain
    result = pipeline.submit_to_blockchain(sample_data)
    print(result)