#!/usr/bin/env python3
"""
Test script for Blockfrost API key validation.

This script tests the Blockfrost API key by making a simple request
to verify the connection and key validity.
"""

import os
import sys
import json
import subprocess
from dotenv import load_dotenv

def load_config():
    """Load configuration from .env file."""
    load_dotenv()
    
    api_key = os.getenv('BLOCKFROST_API_KEY')
    network = os.getenv('BLOCKFROST_NETWORK', 'preview')
    
    if not api_key:
        print("❌ BLOCKFROST_API_KEY not found in environment variables")
        print("Please set BLOCKFROST_API_KEY in your .env file")
        return None, None
    
    return api_key, network

def test_blockfrost_api(api_key, network):
    """
    Test Blockfrost API key with curl request.
    
    Args:
        api_key: Blockfrost API key
        network: Network (mainnet/preview/preprod)
        
    Returns:
        bool: True if API key is valid, False otherwise
    """
    # Determine the base URL based on network
    if network.lower() == 'mainnet':
        base_url = "https://cardano-mainnet.blockfrost.io/api/v0"
    elif network.lower() == 'preview':
        base_url = "https://cardano-preview.blockfrost.io/api/v0"
    elif network.lower() == 'preprod':
        base_url = "https://cardano-preprod.blockfrost.io/api/v0"
    else:
        print(f"❌ Unsupported network: {network}")
        print("Supported networks: mainnet, preview, preprod")
        return False
    
    # Test endpoint - get network info
    url = f"{base_url}/network"
    
    print(f"🔄 Testing Blockfrost API connection...")
    print(f"📍 Network: {network}")
    print(f"🌐 URL: {url}")
    
    try:
        # Make curl request
        curl_cmd = [
            'curl', '-s', '-H',
            f'project_id: {api_key}',
            url
        ]
        
        print(f"🔧 Running: {' '.join(curl_cmd)}")
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                response_data = json.loads(result.stdout)
                
                print("✅ API request successful!")
                print(f"📊 Response: {json.dumps(response_data, indent=2)}")
                
                # Check if we got valid network info
                if 'supply' in response_data and 'stake' in response_data:
                    print("✅ API key is valid and working!")
                    return True
                else:
                    print("⚠️  API response doesn't contain expected network data")
                    return False
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from API")
                print(f"Raw response: {result.stdout}")
                return False
        else:
            print(f"❌ API request failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            print(f"Response: {result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ API request timed out")
        return False
    except FileNotFoundError:
        print("❌ curl command not found. Please install curl.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_alternative_endpoints(api_key, network):
    """
    Test alternative endpoints if the main test fails.
    
    Args:
        api_key: Blockfrost API key
        network: Network (mainnet/preview/preprod)
    """
    if network.lower() == 'mainnet':
        base_url = "https://cardano-mainnet.blockfrost.io/api/v0"
    elif network.lower() == 'preview':
        base_url = "https://cardano-preview.blockfrost.io/api/v0"
    elif network.lower() == 'preprod':
        base_url = "https://cardano-preprod.blockfrost.io/api/v0"
    else:
        print(f"❌ Unsupported network: {network}")
        return False
    
    # Alternative endpoints to try
    endpoints = [
        "/health",
        "/blocks/latest",
        "/epochs/latest"
    ]
    
    print("\n🔄 Trying alternative endpoints...")
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"📍 Testing: {endpoint}")
        
        try:
            curl_cmd = [
                'curl', '-s', '-H',
                f'project_id: {api_key}',
                url
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                try:
                    response_data = json.loads(result.stdout)
                    print(f"✅ {endpoint}: Success")
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True
                except json.JSONDecodeError:
                    print(f"⚠️  {endpoint}: Invalid JSON response")
            else:
                print(f"❌ {endpoint}: Failed (code {result.returncode})")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error - {str(e)}")
    
    return False

def main():
    """Main function to test Blockfrost API."""
    print("🧪 Blockfrost API Key Test")
    print("=" * 50)
    
    # Load configuration
    api_key, network = load_config()
    if not api_key:
        sys.exit(1)
    
    print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"🌐 Network: {network}")
    print()
    
    # Test main endpoint
    if test_blockfrost_api(api_key, network):
        print("\n🎉 Blockfrost API key is working correctly!")
        sys.exit(0)
    else:
        print("\n⚠️  Main endpoint test failed. Trying alternatives...")
        
        # Try alternative endpoints
        if test_alternative_endpoints(api_key, network):
            print("\n✅ At least one endpoint is working!")
            sys.exit(0)
        else:
            print("\n❌ All endpoint tests failed.")
            print("\n🔧 Troubleshooting tips:")
            print("1. Verify your API key is correct")
            print("2. Check if you have sufficient API credits")
            print("3. Ensure your network setting matches your API key")
            print("4. Check your internet connection")
            print("5. Visit https://blockfrost.io/ to verify your project status")
            sys.exit(1)

if __name__ == "__main__":
    main()
