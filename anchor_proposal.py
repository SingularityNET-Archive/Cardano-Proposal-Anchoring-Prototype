#!/usr/bin/env python3
"""
Anchor a community proposal to the Cardano blockchain.

This script:
1. Accepts a proposal as JSON
2. Uploads it to IPFS
3. Computes its SHA256 hash
4. Anchors the hash as metadata in a Cardano transaction
5. Outputs transaction ID and metadata
"""

import argparse
import json
import hashlib
import sys
import time
from typing import Dict, Any
from pathlib import Path

from arweave_utils import ArweaveManager
from pycardano import (
    TransactionBuilder, TransactionOutput, Value, 
    MultiAsset, Asset, UTxO, TransactionInput,
    PlutusData, Datum, Redeemer, ScriptHash,
    Network, Address, PaymentKeyPair, StakeKeyPair,
    Transaction, TransactionBody, Metadata
)
from blockfrost import BlockFrostApi

from config import validate_config, BLOCKFROST_API_KEY, BLOCKFROST_NETWORK, METADATA_LABEL, ARWEAVE_KEY_FILE, ARWEAVE_NETWORK, get_blockfrost_url
from wallet_utils import WalletManager

class ProposalAnchorer:
    """Handles proposal anchoring to Cardano blockchain."""
    
    def __init__(self):
        validate_config()
        self.api = BlockFrostApi(project_id=BLOCKFROST_API_KEY, base_url=get_blockfrost_url(BLOCKFROST_NETWORK))
        self.wallet_manager = WalletManager()
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
    
    def upload_to_arweave(self, proposal: Dict[str, Any]) -> str:
        """
        Upload proposal to Arweave and return transaction ID.
        
        Args:
            proposal: Proposal dictionary
            
        Returns:
            Arweave transaction ID string
        """
        if not self.arweave_manager.wallet:
            self.connect_arweave()
        
        # Convert proposal to JSON string
        proposal_json = json.dumps(proposal, indent=2)
        
        try:
            # Upload to Arweave with tags
            tags = {
                "Content-Type": "application/json",
                "App-Name": "Cardano-Proposal-Anchoring",
                "App-Version": "1.0.0",
                "Proposal-Title": proposal.get("title", "Unknown"),
                "Proposal-Proposer": proposal.get("proposer", "Unknown")
            }
            
            tx_id = self.arweave_manager.upload_data(proposal_json, tags)
            return tx_id
                
        except Exception as e:
            raise Exception(f"Failed to upload to Arweave: {str(e)}")
    
    def create_metadata(self, proposal_hash: str, arweave_tx_id: str) -> Metadata:
        """
        Create Cardano transaction metadata.
        
        Args:
            proposal_hash: SHA256 hash of the proposal
            arweave_tx_id: Arweave transaction ID of the proposal
            
        Returns:
            Metadata object
        """
        metadata = {
            METADATA_LABEL: {
                "proposal_hash": proposal_hash,
                "arweave_tx_id": arweave_tx_id,
                "arweave_url": f"https://arweave.net/{arweave_tx_id}",
                "timestamp": int(time.time()),
                "type": "community_proposal",
                "storage": "arweave"
            }
        }
        
        return Metadata(metadata)
    
    def build_transaction(self, metadata: Metadata) -> str:
        """
        Build and submit Cardano transaction with metadata.
        
        Args:
            metadata: Transaction metadata
            
        Returns:
            Transaction ID
        """
        # Load wallet
        wallet_data = self.wallet_manager.load_wallet()
        if not wallet_data:
            raise Exception("No wallet found. Please generate a wallet first.")
        
        # Get wallet address and UTxOs
        address = Address.from_primitive(wallet_data['address'])
        
        # Get UTxOs from Blockfrost
        utxos = self.api.address_utxos(str(address))
        if not utxos:
            raise Exception("No UTxOs found. Please fund your wallet with testnet ADA.")
        
        # Convert UTxOs to PyCardano format
        utxo_list = []
        for utxo in utxos:
            tx_input = TransactionInput.from_primitive([utxo.tx_hash, utxo.output_index])
            tx_output = TransactionOutput.from_primitive([
                utxo.address,
                utxo.amount
            ])
            utxo_list.append(UTxO(tx_input, tx_output))
        
        # Create transaction builder
        builder = TransactionBuilder()
        
        # Add inputs
        for utxo in utxo_list:
            builder.add_input(utxo)
        
        # Add output (send ADA back to self with minimum amount)
        min_ada = 1000000  # 1 ADA in lovelace
        builder.add_output(
            TransactionOutput(
                address=address,
                amount=Value(min_ada)
            )
        )
        
        # Add metadata
        builder.metadata = metadata
        
        # Build transaction
        transaction = builder.build_and_sign(
            [PaymentKeyPair.from_json(wallet_data['payment_skey'])]
        )
        
        # Submit transaction
        try:
            tx_id = self.api.submit_transaction(transaction.to_cbor())
            return tx_id
        except Exception as e:
            raise Exception(f"Failed to submit transaction: {str(e)}")
    
    def anchor_proposal(self, proposal: Dict[str, Any]) -> Dict[str, str]:
        """
        Anchor a proposal to the Cardano blockchain.
        
        Args:
            proposal: Proposal dictionary
            
        Returns:
            Dictionary with transaction ID, hash, and IPFS CID
        """
        print("🔄 Computing proposal hash...")
        proposal_hash = self.compute_hash(proposal)
        print(f"✅ Hash computed: {proposal_hash}")
        
        print("🔄 Uploading to Arweave...")
        arweave_tx_id = self.upload_to_arweave(proposal)
        print(f"✅ Uploaded to Arweave: {arweave_tx_id}")
        print(f"🌐 Permanent URL: https://arweave.net/{arweave_tx_id}")
        
        print("🔄 Creating transaction metadata...")
        metadata = self.create_metadata(proposal_hash, arweave_tx_id)
        
        print("🔄 Building and submitting transaction...")
        tx_id = self.build_transaction(metadata)
        print(f"✅ Transaction submitted: {tx_id}")
        
        return {
            "transaction_id": tx_id,
            "proposal_hash": proposal_hash,
            "arweave_tx_id": arweave_tx_id,
            "arweave_url": f"https://arweave.net/{arweave_tx_id}",
            "metadata_label": METADATA_LABEL
        }

def load_proposal_from_file(file_path: str) -> Dict[str, Any]:
    """Load proposal from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON in file: {file_path}")

def create_example_proposal() -> Dict[str, Any]:
    """Create an example proposal for testing."""
    return {
        "title": "Community Garden Initiative",
        "description": "Proposal to establish a community garden in the local park to promote sustainability and community engagement.",
        "proposer": "Alice Johnson",
        "timestamp": int(time.time()),
        "category": "community_development",
        "budget": 5000,
        "duration_months": 12,
        "beneficiaries": ["local_residents", "environment", "community"]
    }

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Anchor a community proposal to the Cardano blockchain"
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to JSON file containing the proposal"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read proposal from stdin"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Use example proposal for testing"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for results (optional)"
    )
    
    args = parser.parse_args()
    
    # Load proposal
    if args.example:
        proposal = create_example_proposal()
        print("📝 Using example proposal:")
        print(json.dumps(proposal, indent=2))
    elif args.file:
        proposal = load_proposal_from_file(args.file)
    elif args.stdin:
        proposal = json.load(sys.stdin)
    else:
        print("❌ Please specify a proposal source: --file, --stdin, or --example")
        sys.exit(1)
    
    # Validate proposal structure
    required_fields = ["title", "description", "proposer"]
    missing_fields = [field for field in required_fields if field not in proposal]
    if missing_fields:
        print(f"❌ Missing required fields: {', '.join(missing_fields)}")
        sys.exit(1)
    
    try:
        # Anchor proposal
        anchorer = ProposalAnchorer()
        result = anchorer.anchor_proposal(proposal)
        
        # Output results
        print("\n🎉 Proposal anchored successfully!")
        print(f"📋 Transaction ID: {result['transaction_id']}")
        print(f"🔐 Proposal Hash: {result['proposal_hash']}")
        print(f"🌐 Arweave TX ID: {result['arweave_tx_id']}")
        print(f"🔗 Permanent URL: {result['arweave_url']}")
        print(f"🏷️  Metadata Label: {result['metadata_label']}")
        
        # Save results to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Results saved to: {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
