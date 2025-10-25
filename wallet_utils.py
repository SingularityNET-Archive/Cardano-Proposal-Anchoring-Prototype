"""
Wallet management utilities for the Cardano proposal anchoring prototype.
"""
import json
import os
from typing import Optional, Tuple
from pycardano import (
    PaymentKeyPair, StakeKeyPair, Address, Network,
    ExtendedSigningKey, ExtendedVerificationKey
)
from pycardano.crypto import bech32
from pycardano.key import ExtendedSigningKey, ExtendedVerificationKey
from pycardano.wallet import Wallet

class WalletManager:
    """Manages Cardano wallet operations for the prototype."""
    
    def __init__(self, network: Network = Network.TESTNET):
        self.network = network
        self.wallet_file = "wallet.json"
        self.mnemonic_file = "wallet_mnemonic.txt"
    
    def generate_wallet(self) -> Tuple[str, str]:
        """
        Generate a new Cardano wallet and return mnemonic and payment address.
        
        Returns:
            Tuple of (mnemonic, payment_address)
        """
        # Generate key pairs
        payment_key_pair = PaymentKeyPair.generate()
        stake_key_pair = StakeKeyPair.generate()
        
        # Create address
        address = Address(
            payment_part=payment_key_pair.vkey.hash(),
            staking_part=stake_key_pair.vkey.hash(),
            network=self.network
        )
        
        # Generate mnemonic (simplified - in production use proper mnemonic generation)
        mnemonic = self._generate_mnemonic()
        
        # Save wallet data
        wallet_data = {
            "payment_vkey": payment_key_pair.vkey.to_cbor_hex(),
            "payment_skey": payment_key_pair.skey.to_cbor_hex(),
            "stake_vkey": stake_key_pair.vkey.to_cbor_hex(),
            "stake_skey": stake_key_pair.skey.to_cbor_hex(),
            "address": str(address),
            "network": str(self.network)
        }
        
        with open(self.wallet_file, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        
        with open(self.mnemonic_file, 'w') as f:
            f.write(mnemonic)
        
        print(f"✅ Wallet generated successfully!")
        print(f"📍 Payment Address: {address}")
        print(f"🔑 Mnemonic saved to: {self.mnemonic_file}")
        print(f"💾 Wallet data saved to: {self.wallet_file}")
        print(f"\n⚠️  IMPORTANT: Fund this address with testnet ADA before using!")
        print(f"🔗 Testnet Faucet: https://testnets.cardano.org/en/testnets/cardano/tools/faucet/")
        
        return mnemonic, str(address)
    
    def load_wallet(self) -> Optional[dict]:
        """
        Load existing wallet from file.
        
        Returns:
            Wallet data dictionary or None if not found
        """
        if not os.path.exists(self.wallet_file):
            return None
        
        try:
            with open(self.wallet_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def get_payment_address(self) -> Optional[str]:
        """
        Get the payment address from the loaded wallet.
        
        Returns:
            Payment address string or None if wallet not found
        """
        wallet_data = self.load_wallet()
        if wallet_data:
            return wallet_data.get('address')
        return None
    
    def get_signing_key(self) -> Optional[str]:
        """
        Get the signing key from the loaded wallet.
        
        Returns:
            Signing key hex string or None if wallet not found
        """
        wallet_data = self.load_wallet()
        if wallet_data:
            return wallet_data.get('payment_skey')
        return None
    
    def wallet_exists(self) -> bool:
        """Check if wallet file exists."""
        return os.path.exists(self.wallet_file)
    
    def _generate_mnemonic(self) -> str:
        """
        Generate a mnemonic phrase (simplified version).
        In production, use a proper mnemonic generation library.
        """
        # This is a simplified mnemonic for demonstration
        # In production, use: from mnemonic import Mnemonic
        words = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse",
            "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
            "action", "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit"
        ]
        
        # Generate 24 words (simplified)
        import random
        mnemonic = " ".join(random.choices(words, k=24))
        return mnemonic

def main():
    """CLI interface for wallet management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cardano Wallet Manager")
    parser.add_argument("--generate", action="store_true", help="Generate a new wallet")
    parser.add_argument("--info", action="store_true", help="Show wallet information")
    
    args = parser.parse_args()
    
    wallet_manager = WalletManager()
    
    if args.generate:
        if wallet_manager.wallet_exists():
            print("⚠️  Wallet already exists. Use --info to see details.")
            return
        
        mnemonic, address = wallet_manager.generate_wallet()
        print(f"\n🔐 Mnemonic: {mnemonic}")
        print(f"📍 Address: {address}")
        
    elif args.info:
        if not wallet_manager.wallet_exists():
            print("❌ No wallet found. Use --generate to create one.")
            return
        
        address = wallet_manager.get_payment_address()
        print(f"📍 Payment Address: {address}")
        print(f"💾 Wallet file: {wallet_manager.wallet_file}")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
