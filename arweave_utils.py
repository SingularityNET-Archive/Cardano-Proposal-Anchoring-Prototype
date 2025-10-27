"""
Arweave utilities for the Cardano proposal anchoring prototype.
"""
import json
import os
from typing import Dict, Any, Optional
import arweave
from arweave import Wallet

class ArweaveManager:
    """Manages Arweave operations for the prototype."""
    
    def __init__(self, key_file: str = "arweave_key.json", network: str = "mainnet"):
        self.key_file = key_file
        self.network = network
        self.wallet = None
        self.arweave_client = None
        
    def load_wallet(self) -> Wallet:
        """
        Load Arweave wallet from key file.
        
        Returns:
            Arweave wallet object
            
        Raises:
            FileNotFoundError: If key file doesn't exist
            ValueError: If key file is invalid
        """
        if not os.path.exists(self.key_file):
            raise FileNotFoundError(f"Arweave key file not found: {self.key_file}")
        
        try:
            with open(self.key_file, 'r') as f:
                key_data = json.load(f)
            
            # Validate key file format
            if not isinstance(key_data, dict):
                raise ValueError("Invalid key file format: must be JSON object")
            
            # Create wallet from key data
            self.wallet = Wallet(key_data)
            
            # Initialize Arweave client
            if self.network == "testnet":
                self.arweave_client = arweave.Arweave(host="arweave.net", port=443, protocol="https")
            else:
                self.arweave_client = arweave.Arweave(host="arweave.net", port=443, protocol="https")
            
            return self.wallet
            
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in key file: {self.key_file}")
        except Exception as e:
            raise ValueError(f"Failed to load Arweave wallet: {str(e)}")
    
    def get_wallet_balance(self) -> float:
        """
        Get AR balance of the wallet.
        
        Returns:
            Balance in AR tokens
            
        Raises:
            Exception: If wallet not loaded or network error
        """
        if not self.wallet:
            raise Exception("Wallet not loaded. Call load_wallet() first.")
        
        try:
            balance = self.arweave_client.wallets.get_balance(self.wallet.address)
            return float(balance) / 1000000000000  # Convert from winston to AR
        except Exception as e:
            raise Exception(f"Failed to get wallet balance: {str(e)}")
    
    def check_sufficient_balance(self, estimated_cost: float = 0.1) -> bool:
        """
        Check if wallet has sufficient AR balance for upload.
        
        Args:
            estimated_cost: Estimated cost in AR (default 0.1 AR)
            
        Returns:
            True if sufficient balance, False otherwise
        """
        try:
            balance = self.get_wallet_balance()
            return balance >= estimated_cost
        except Exception:
            return False
    
    def upload_data(self, data: str, tags: Optional[Dict[str, str]] = None) -> str:
        """
        Upload data to Arweave and return transaction ID.
        
        Args:
            data: Data string to upload
            tags: Optional tags for the transaction
            
        Returns:
            Arweave transaction ID
            
        Raises:
            Exception: If upload fails
        """
        if not self.wallet:
            raise Exception("Wallet not loaded. Call load_wallet() first.")
        
        try:
            # Check balance before upload
            if not self.check_sufficient_balance():
                balance = self.get_wallet_balance()
                raise Exception(f"Insufficient AR balance: {balance:.6f} AR. Need at least 0.1 AR for upload.")
            
            # Prepare tags
            if tags is None:
                tags = {}
            
            # Add default tags
            tags.update({
                "Content-Type": "application/json",
                "App-Name": "Cardano-Proposal-Anchoring",
                "App-Version": "1.0.0"
            })
            
            # Upload data
            tx = self.arweave_client.create_transaction(
                data=data,
                wallet=self.wallet,
                tags=tags
            )
            
            # Sign and submit transaction
            tx.sign()
            self.arweave_client.transactions.post(tx)
            
            return tx.id
            
        except Exception as e:
            raise Exception(f"Failed to upload to Arweave: {str(e)}")
    
    def get_data(self, transaction_id: str) -> str:
        """
        Retrieve data from Arweave using transaction ID.
        
        Args:
            transaction_id: Arweave transaction ID
            
        Returns:
            Retrieved data as string
            
        Raises:
            Exception: If retrieval fails
        """
        try:
            # Get transaction data
            data = self.arweave_client.transactions.get_data(transaction_id)
            return data.decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to retrieve data from Arweave: {str(e)}")
    
    def get_transaction_info(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get transaction information from Arweave.
        
        Args:
            transaction_id: Arweave transaction ID
            
        Returns:
            Transaction information dictionary
        """
        try:
            tx = self.arweave_client.transactions.get(transaction_id)
            return {
                "id": tx.id,
                "owner": tx.owner,
                "target": tx.target,
                "quantity": tx.quantity,
                "reward": tx.reward,
                "tags": {tag.name: tag.value for tag in tx.tags},
                "block": tx.block,
                "signature": tx.signature
            }
        except Exception as e:
            raise Exception(f"Failed to get transaction info: {str(e)}")
    
    def get_permanent_url(self, transaction_id: str) -> str:
        """
        Get permanent URL for the transaction.
        
        Args:
            transaction_id: Arweave transaction ID
            
        Returns:
            Permanent URL string
        """
        return f"https://arweave.net/{transaction_id}"

def create_example_key_file() -> Dict[str, Any]:
    """
    Create an example Arweave key file structure.
    This is for documentation purposes only.
    """
    return {
        "kty": "RSA",
        "e": "AQAB",
        "n": "example_modulus_here",
        "d": "example_private_exponent_here",
        "p": "example_prime_p_here",
        "q": "example_prime_q_here",
        "dp": "example_dp_here",
        "dq": "example_dq_here",
        "qi": "example_qi_here"
    }

def main():
    """CLI interface for Arweave management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Arweave Manager")
    parser.add_argument("--check-balance", action="store_true", help="Check wallet balance")
    parser.add_argument("--key-file", default="arweave_key.json", help="Path to Arweave key file")
    parser.add_argument("--network", default="mainnet", choices=["mainnet", "testnet"], help="Arweave network")
    
    args = parser.parse_args()
    
    try:
        manager = ArweaveManager(key_file=args.key_file, network=args.network)
        manager.load_wallet()
        
        if args.check_balance:
            balance = manager.get_wallet_balance()
            print(f"💰 AR Balance: {balance:.6f} AR")
            print(f"📍 Address: {manager.wallet.address}")
            print(f"🔗 Network: {args.network}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
