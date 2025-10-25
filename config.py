"""
Configuration management for the Cardano proposal anchoring prototype.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Blockfrost API configuration
BLOCKFROST_API_KEY = os.getenv('BLOCKFROST_API_KEY')
BLOCKFROST_NETWORK = os.getenv('BLOCKFROST_NETWORK', 'testnet')

# Infura IPFS configuration
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
INFURA_PROJECT_SECRET = os.getenv('INFURA_PROJECT_SECRET')

# Cardano network configuration
CARDANO_NETWORK = os.getenv('CARDANO_NETWORK', 'testnet')
METADATA_LABEL = int(os.getenv('METADATA_LABEL', '1337'))

# IPFS gateway configuration
IPFS_GATEWAY_URL = "https://ipfs.infura.io:5001"

# Validation
def validate_config():
    """Validate that required configuration is present."""
    missing_vars = []
    
    if not BLOCKFROST_API_KEY:
        missing_vars.append('BLOCKFROST_API_KEY')
    if not INFURA_PROJECT_ID:
        missing_vars.append('INFURA_PROJECT_ID')
    if not INFURA_PROJECT_SECRET:
        missing_vars.append('INFURA_PROJECT_SECRET')
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True
