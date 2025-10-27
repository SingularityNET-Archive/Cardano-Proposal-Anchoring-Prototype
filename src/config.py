"""
Configuration management for the Cardano proposal anchoring prototype.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Blockfrost API configuration
BLOCKFROST_API_KEY = os.getenv('BLOCKFROST_API_KEY')
BLOCKFROST_NETWORK = os.getenv('BLOCKFROST_NETWORK', 'preview')

# Arweave configuration
ARWEAVE_GATEWAY_URL = os.getenv('ARWEAVE_GATEWAY_URL', 'https://arweave.net')
ARWEAVE_KEY_FILE = os.getenv('ARWEAVE_KEY_FILE', 'arweave_key.json')

# Cardano network configuration
CARDANO_NETWORK = os.getenv('CARDANO_NETWORK', 'testnet')
METADATA_LABEL = int(os.getenv('METADATA_LABEL', '1337'))

# Arweave network configuration
ARWEAVE_NETWORK = os.getenv('ARWEAVE_NETWORK', 'mainnet')

# Validation
def get_blockfrost_url(network: str) -> str:
    """
    Get the appropriate Blockfrost URL based on network.
    
    Args:
        network: Network name (mainnet, preview, preprod)
        
    Returns:
        Blockfrost base URL (SDK will append /v0 automatically)
    """
    network = network.lower()
    
    if network == 'mainnet':
        return "https://cardano-mainnet.blockfrost.io/api"
    elif network == 'preview':
        return "https://cardano-preview.blockfrost.io/api"
    elif network == 'preprod':
        return "https://cardano-preprod.blockfrost.io/api"
    else:
        raise ValueError(f"Unsupported network: {network}. Supported networks: mainnet, preview, preprod")

def validate_config():
    """Validate that required configuration is present."""
    missing_vars = []
    
    if not BLOCKFROST_API_KEY:
        missing_vars.append('BLOCKFROST_API_KEY')
    if not os.path.exists(ARWEAVE_KEY_FILE):
        missing_vars.append(f'Arweave key file not found: {ARWEAVE_KEY_FILE}')
    
    # Validate network
    try:
        get_blockfrost_url(BLOCKFROST_NETWORK)
    except ValueError as e:
        missing_vars.append(str(e))
    
    if missing_vars:
        raise ValueError(f"Missing required configuration: {', '.join(missing_vars)}")
    
    return True
