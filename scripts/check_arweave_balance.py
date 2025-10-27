#!/usr/bin/env python3
"""
Quick script to check Arweave wallet balance.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.arweave_utils import ArweaveManager
from src.config import ARWEAVE_KEY_FILE, ARWEAVE_NETWORK

def main():
    print(f"🔍 Checking Arweave Wallet Balance")
    print(f"📁 Key file: {ARWEAVE_KEY_FILE}")
    print(f"🌐 Network: {ARWEAVE_NETWORK}")
    print("=" * 50)
    
    try:
        # Create Arweave manager
        manager = ArweaveManager(key_file=ARWEAVE_KEY_FILE, network=ARWEAVE_NETWORK)
        
        # Load wallet
        print(f"🔄 Loading wallet from {ARWEAVE_KEY_FILE}...")
        manager.load_wallet()
        print("✅ Wallet loaded successfully")
        
        # Get wallet address
        print(f"📍 Wallet Address: {manager.wallet.address}")
        
        # Get balance
        print("🔄 Fetching balance...")
        balance = manager.get_wallet_balance()
        print(f"💰 AR Balance: {balance:.6f} AR")
        
        # Check if sufficient for uploads
        if balance >= 0.1:
            print("✅ Sufficient balance for uploads")
        else:
            print("⚠️  Low balance - you may need more AR for uploads")
            print("   Recommended: At least 0.1 AR per upload")
        
        print("\n🔗 Fund your wallet:")
        print("   - KuCoin: https://www.kucoin.com/")
        print("   - Gate.io: https://www.gate.io/")
        print("   - Binance: https://www.binance.com/")
        
    except FileNotFoundError:
        print(f"❌ Arweave key file not found: {ARWEAVE_KEY_FILE}")
        print("Please download your Arweave wallet key file and save it to this directory")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Invalid key file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

