#!/usr/bin/env python3
"""
Comprehensive status check for the Cardano Proposal Anchoring Prototype.
"""

import sys
import os
from arweave_utils import ArweaveManager
from wallet_utils import WalletManager
from config import (
    BLOCKFROST_API_KEY, BLOCKFROST_NETWORK, 
    ARWEAVE_KEY_FILE, ARWEAVE_NETWORK,
    CARDANO_NETWORK, METADATA_LABEL
)

def check_arweave_status():
    """Check Arweave wallet status."""
    print("📦 Arweave Configuration")
    print("=" * 50)
    print(f"   Key File: {ARWEAVE_KEY_FILE}")
    print(f"   Network: {ARWEAVE_NETWORK}")
    
    try:
        manager = ArweaveManager(key_file=ARWEAVE_KEY_FILE, network=ARWEAVE_NETWORK)
        manager.load_wallet()
        
        balance = manager.get_wallet_balance()
        print(f"   ✅ Wallet loaded")
        print(f"   💰 Balance: {balance:.6f} AR")
        print(f"   📍 Address: {manager.wallet.address}")
        
        if balance >= 0.1:
            print(f"   ✅ Sufficient balance for uploads")
        else:
            print(f"   ⚠️  Low balance - recommended: 0.5 AR")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_cardano_wallet():
    """Check Cardano wallet status."""
    print("\n💳 Cardano Wallet")
    print("=" * 50)
    
    wallet_manager = WalletManager()
    
    if wallet_manager.wallet_exists():
        address = wallet_manager.get_payment_address()
        print(f"   ✅ Wallet found")
        print(f"   📍 Address: {address}")
        print(f"   ⚠️  Check if funded at: https://preprod.cardanoscan.io/address/{address}")
        return True
    else:
        print(f"   ❌ No wallet found")
        print(f"   Run: python wallet_utils.py --generate")
        return False

def check_blockfrost():
    """Check Blockfrost configuration."""
    print("\n🔗 Blockfrost API")
    print("=" * 50)
    print(f"   Network: {BLOCKFROST_NETWORK}")
    
    if BLOCKFROST_API_KEY:
        masked_key = f"{BLOCKFROST_API_KEY[:8]}...{BLOCKFROST_API_KEY[-4:]}"
        print(f"   API Key: {masked_key}")
        print(f"   ✅ Configured")
        return True
    else:
        print(f"   ❌ Not configured")
        return False

def check_system_config():
    """Check system configuration."""
    print("\n⚙️  System Configuration")
    print("=" * 50)
    print(f"   Cardano Network: {CARDANO_NETWORK}")
    print(f"   Metadata Label: {METADATA_LABEL}")
    print(f"   ✅ Configuration loaded")

def main():
    """Main status check."""
    print("🚀 Cardano Proposal Anchoring - System Status")
    print("=" * 50)
    print()
    
    # Run all checks
    arweave_ok = check_arweave_status()
    cardano_ok = check_cardano_wallet()
    blockfrost_ok = check_blockfrost()
    check_system_config()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Status Summary")
    print("=" * 50)
    
    checks = [
        ("Arweave Wallet", arweave_ok),
        ("Cardano Wallet", cardano_ok),
        ("Blockfrost API", blockfrost_ok)
    ]
    
    all_ok = True
    for name, status in checks:
        icon = "✅" if status else "❌"
        print(f"   {icon} {name}")
        if not status:
            all_ok = False
    
    print()
    if all_ok:
        print("🎉 All systems ready!")
        print("\n📝 Ready to anchor proposals:")
        print("   python anchor_proposal.py --example")
    else:
        print("⚠️  Some components need attention")
        print("\n📝 Next steps:")
        if not cardano_ok:
            print("   1. Generate Cardano wallet: python wallet_utils.py --generate")
            print("   2. Fund wallet: https://testnets.cardano.org/en/testnets/cardano/tools/faucet/")
        if not arweave_ok:
            print("   1. Check Arweave key file exists")
            print("   2. Fund Arweave wallet if balance is low")
        if not blockfrost_ok:
            print("   1. Add BLOCKFROST_API_KEY to .env file")

if __name__ == "__main__":
    main()

