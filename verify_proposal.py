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

import ipfshttpclient
import requests
from blockfrost import BlockFrostApi

from config import validate_config, BLOCKFROST_API_KEY, BLOCKFROST_NETWORK, METADATA_LABEL

class ProposalVerifier:
    """Handles proposal verification from Cardano blockchain."""
    
    def __init__(self):
        validate_config()
        self.api = BlockFrostApi(project_id=BLOCKFROST_API_KEY, network=BLOCKFROST_NETWORK)
        self.ipfs_client = None
        
    def connect_ipfs(self):
        """Connect to IPFS."""
        try:
            self.ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        except:
            # Use public IPFS gateway as fallback
            self.ipfs_gateway = "https://ipfs.io/ipfs/"
    
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
    
    def retrieve_proposal_from_ipfs(self, ipfs_cid: str) -> Dict[str, Any]:
        """
        Retrieve proposal from IPFS.
        
        Args:
            ipfs_cid: IPFS CID of the proposal
            
        Returns:
            Proposal dictionary
        """
        try:
            if hasattr(self, 'ipfs_gateway'):
                # Use public IPFS gateway
                url = f"{self.ipfs_gateway}{ipfs_cid}"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.json()
            else:
                # Use local IPFS client
                if not self.ipfs_client:
                    self.connect_ipfs()
                
                proposal_json = self.ipfs_client.cat(ipfs_cid)
                return json.loads(proposal_json.decode('utf-8'))
                
        except Exception as e:
            raise Exception(f"Failed to retrieve proposal from IPFS: {str(e)}")
    
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
        
        # Extract proposal hash and IPFS CID
        proposal_hash = metadata.get('proposal_hash')
        ipfs_cid = metadata.get('ipfs_cid')
        timestamp = metadata.get('timestamp')
        
        if not proposal_hash or not ipfs_cid:
            raise Exception("Invalid metadata: missing proposal_hash or ipfs_cid")
        
        print(f"🔐 On-chain hash: {proposal_hash}")
        print(f"🌐 IPFS CID: {ipfs_cid}")
        
        # Retrieve proposal from IPFS
        print("🔄 Retrieving proposal from IPFS...")
        proposal = self.retrieve_proposal_from_ipfs(ipfs_cid)
        print("✅ Proposal retrieved from IPFS")
        
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
            "ipfs_cid": ipfs_cid,
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
        print(f"   IPFS CID: {result['ipfs_cid']}")
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
