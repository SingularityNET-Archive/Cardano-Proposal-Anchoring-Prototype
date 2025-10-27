#!/usr/bin/env python3
"""
Setup script for Cardano Proposal Anchoring Prototype.

This script helps users set up the environment and test the installation.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_virtual_environment():
    """Check if we're in a virtual environment."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return True
    else:
        print("⚠️  Not in a virtual environment")
        print("Consider running: python3 -m venv venv && source venv/bin/activate")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("🔄 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_environment_file():
    """Check if .env file exists."""
    if Path(".env").exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Please copy env.example to .env and configure your API keys")
        return False

def test_imports():
    """Test if all modules can be imported."""
    modules = ["config", "wallet_utils", "arweave_utils", "anchor_proposal", "verify_proposal"]
    
    print("🔄 Testing module imports...")
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    return True

def test_blockfrost():
    """Test Blockfrost API connection."""
    print("🔄 Testing Blockfrost API...")
    try:
        result = subprocess.run([sys.executable, "test_blockfrost.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Blockfrost API test passed")
            return True
        else:
            print(f"❌ Blockfrost API test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Blockfrost API test timed out")
        return False
    except Exception as e:
        print(f"❌ Blockfrost API test error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Cardano Proposal Anchoring Prototype Setup")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Environment File", check_environment_file),
        ("Module Imports", test_imports),
        ("Blockfrost API", test_blockfrost)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 Setup Summary:")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Configure your .env file with API keys")
        print("2. Generate a wallet: python wallet_utils.py --generate")
        print("3. Fund your wallet with testnet ADA")
        print("4. Create an Arweave wallet: arweave_key.json")
        print("5. Test anchoring: python anchor_proposal.py --example")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
