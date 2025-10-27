#!/usr/bin/env python3
"""
Verify a community proposal anchored to the Cardano blockchain.

This script:
1. Fetches transaction metadata from Blockfrost
2. Retrieves proposal from IPFS using stored CID
3. Recomputes SHA256 hash
4. Compares with on-chain hash
5. Reports verification result
"""

import argparse
import json
import hashlib
import sys
from typing import Dict, Any, Optional

from src.core.arweave_utils import ArweaveManager
import requests
from blockfrost import BlockFrostApi

from src.config import validate_config, BLOCKFROST_API_KEY, BLOCKFROST_NETWORK, METADATA_LABEL, ARWEAVE_KEY_FILE, ARWEAVE_NETWORK, get_blockfrost_url

class ProposalVerifier:
    """Handles proposal verification from Cardano blockchain."""
    
    def __init__(self):
        validate_config()
        # Explicitly set base_url to match the network (auto-detection doesn't always work)
        self.api = BlockFrostApi(
            project_id=BLOCKFROST_API_KEY,
            base_url=get_blockfrost_url(BLOCKFROST_NETWORK)
        )
        self.arweave_manager = ArweaveManager(key_file=ARWEAVE_KEY_FILE, network=ARWEAVE_NETWORK)
        
    def connect_arweave(self):
        """Connect to Arweave and load wallet."""
        try:
            self.arweave_manager.load_wallet()
        except FileNotFoundError:
            raise Exception("Arweave key file not found. Please create arweave_key.json with your Arweave wallet.")
        except ValueError as e:
            raise Exception(f"Invalid Arweave key file: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to connect to Arweave: {str(e)}")
    
    def fetch_transaction_metadata(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch transaction metadata from Blockfrost.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Metadata dictionary or None if not found
        """
        try:
            # Get transaction details
            tx = self.api.transaction(tx_id)
            
            # Get transaction metadata
            metadata = self.api.transaction_metadata(tx_id)
            
            # Look for our metadata label
            for meta in metadata:
                if str(meta.label) == str(METADATA_LABEL):
                    return meta.json_metadata
            
            return None
            
        except Exception as e:
            raise Exception(f"Failed to fetch transaction metadata: {str(e)}")
    
    def retrieve_proposal_from_arweave(self, arweave_tx_id: str) -> Dict[str, Any]:
        """
        Retrieve proposal from Arweave.
        
        Args:
            arweave_tx_id: Arweave transaction ID of the proposal
            
        Returns:
            Proposal dictionary
        """
        try:
            if not self.arweave_manager.wallet:
                self.connect_arweave()
            
            # Get data from Arweave
            proposal_json = self.arweave_manager.get_data(arweave_tx_id)
            return json.loads(proposal_json)
                
        except Exception as e:
            raise Exception(f"Failed to retrieve proposal from Arweave: {str(e)}")
    
    def compute_hash(self, proposal: Dict[str, Any]) -> str:
        """
        Compute SHA256 hash of the proposal JSON.
        
        Args:
            proposal: Proposal dictionary
            
        Returns:
            SHA256 hash as hex string
        """
        # Normalize JSON by sorting keys and removing whitespace
        normalized_json = json.dumps(proposal, sort_keys=True, separators=(',', ':'))
        
        # Compute SHA256 hash
        hash_obj = hashlib.sha256()
        hash_obj.update(normalized_json.encode('utf-8'))
        
        return hash_obj.hexdigest()
    
    def verify_proposal(self, tx_id: str) -> Dict[str, Any]:
        """
        Verify a proposal anchored to the blockchain.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Verification result dictionary
        """
        print(f"🔄 Fetching transaction metadata for: {tx_id}")
        
        # Fetch metadata from blockchain
        metadata = self.fetch_transaction_metadata(tx_id)
        if not metadata:
            raise Exception(f"No proposal metadata found in transaction {tx_id}")
        
        print("✅ Metadata retrieved from blockchain")
        print(f"📋 Metadata: {json.dumps(metadata, indent=2)}")
        
        # Extract proposal hash and Arweave transaction ID
        proposal_hash = metadata.get('proposal_hash')
        arweave_tx_id = metadata.get('arweave_tx_id')
        arweave_url = metadata.get('arweave_url')
        timestamp = metadata.get('timestamp')
        
        if not proposal_hash or not arweave_tx_id:
            raise Exception("Invalid metadata: missing proposal_hash or arweave_tx_id")
        
        print(f"🔐 On-chain hash: {proposal_hash}")
        print(f"🌐 Arweave TX ID: {arweave_tx_id}")
        if arweave_url:
            print(f"🔗 Arweave URL: {arweave_url}")
        
        # Retrieve proposal from Arweave
        print("🔄 Retrieving proposal from Arweave...")
        proposal = self.retrieve_proposal_from_arweave(arweave_tx_id)
        print("✅ Proposal retrieved from Arweave")
        
        # Compute hash of retrieved proposal
        print("🔄 Computing hash of retrieved proposal...")
        computed_hash = self.compute_hash(proposal)
        print(f"🔐 Computed hash: {computed_hash}")
        
        # Compare hashes
        hash_match = proposal_hash == computed_hash
        
        result = {
            "transaction_id": tx_id,
            "verification_successful": hash_match,
            "on_chain_hash": proposal_hash,
            "computed_hash": computed_hash,
            "arweave_tx_id": arweave_tx_id,
            "arweave_url": arweave_url,
            "timestamp": timestamp,
            "proposal": proposal,
            "metadata": metadata
        }
        
        if hash_match:
            print("✅ VERIFICATION SUCCESSFUL: Hashes match!")
        else:
            print("❌ VERIFICATION FAILED: Hashes do not match!")
            print(f"   On-chain hash: {proposal_hash}")
            print(f"   Computed hash: {computed_hash}")
        
        return result

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Verify a community proposal anchored to the Cardano blockchain"
    )
    parser.add_argument(
        "transaction_id",
        help="Transaction ID to verify"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for verification results (optional)"
    )
    parser.add_argument(
        "--show-proposal",
        action="store_true",
        help="Display the full proposal content"
    )
    
    args = parser.parse_args()
    
    try:
        # Verify proposal
        verifier = ProposalVerifier()
        result = verifier.verify_proposal(args.transaction_id)
        
        # Display results
        print(f"\n📊 Verification Results:")
        print(f"   Transaction ID: {result['transaction_id']}")
        print(f"   Verification: {'✅ SUCCESS' if result['verification_successful'] else '❌ FAILED'}")
        print(f"   Arweave TX ID: {result['arweave_tx_id']}")
        if result['arweave_url']:
            print(f"   Arweave URL: {result['arweave_url']}")
        print(f"   Timestamp: {result['timestamp']}")
        
        if args.show_proposal:
            print(f"\n📝 Proposal Content:")
            print(json.dumps(result['proposal'], indent=2))
        
        # Save results to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {args.output}")
        
        # Exit with appropriate code
        sys.exit(0 if result['verification_successful'] else 1)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
