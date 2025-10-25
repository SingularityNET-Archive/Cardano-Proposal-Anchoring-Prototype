# Cardano Proposal Anchoring Prototype

A minimal working Python prototype that anchors community proposals to the Cardano blockchain using Blockfrost and PyCardano. The system uploads proposals to IPFS, computes SHA256 hashes, and anchors them as metadata in Cardano transactions on the testnet.

## 🏗️ Architecture

```
Proposal JSON → IPFS Upload → Hash Computation → Cardano Transaction → Blockchain
     ↓              ↓              ↓                    ↓              ↓
   JSON File    IPFS CID      SHA256 Hash         Metadata         On-chain
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd AI-Blockchain-Prototype

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the environment template and configure your API keys:

```bash
cp env.example .env
```

Edit `.env` with your credentials:

```env
# Blockfrost API Configuration
BLOCKFROST_API_KEY=your_blockfrost_api_key_here
BLOCKFROST_NETWORK=testnet

# Infura IPFS Configuration
INFURA_PROJECT_ID=your_infura_project_id_here
INFURA_PROJECT_SECRET=your_infura_project_secret_here

# Cardano Network Configuration
CARDANO_NETWORK=testnet
METADATA_LABEL=1337
```

### 3. Get API Keys

#### Blockfrost API Key
1. Visit [Blockfrost.io](https://blockfrost.io/)
2. Sign up for a free account
3. Create a new project for Cardano testnet
4. Copy your API key to `.env`

#### Infura IPFS Credentials
1. Visit [Infura.io](https://infura.io/)
2. Sign up for a free account
3. Create a new project and select "IPFS" as the service
4. Copy your Project ID and Secret to `.env`

### 4. Generate Wallet

```bash
# Generate a new testnet wallet
python wallet_utils.py --generate
```

This will create:
- `wallet.json` - Wallet keys (keep secure!)
- `wallet_mnemonic.txt` - Recovery phrase (keep secure!)

### 5. Fund Your Wallet

1. Copy the payment address from the wallet generation output
2. Visit the [Cardano Testnet Faucet](https://testnets.cardano.org/en/testnets/cardano/tools/faucet/)
3. Request testnet ADA for your address
4. Wait for the transaction to confirm

## 📖 Usage

### Anchor a Proposal

#### Using Example Proposal
```bash
python anchor_proposal.py --example
```

#### Using a JSON File
```bash
# Create a proposal file
cat > my_proposal.json << EOF
{
  "title": "Community Garden Initiative",
  "description": "Proposal to establish a community garden in the local park",
  "proposer": "Alice Johnson",
  "timestamp": 1703001600,
  "category": "community_development",
  "budget": 5000,
  "duration_months": 12
}
EOF

# Anchor the proposal
python anchor_proposal.py --file my_proposal.json
```

#### Using stdin
```bash
echo '{"title": "Test Proposal", "description": "A test proposal", "proposer": "Test User"}' | python anchor_proposal.py --stdin
```

### Verify a Proposal

```bash
# Verify using transaction ID
python verify_proposal.py <transaction_id>

# Show full proposal content
python verify_proposal.py <transaction_id> --show-proposal

# Save results to file
python verify_proposal.py <transaction_id> --output verification_results.json
```

## 📋 Proposal Schema

The system accepts proposals with the following structure:

```json
{
  "title": "string (required)",
  "description": "string (required)", 
  "proposer": "string (required)",
  "timestamp": "number (optional)",
  "category": "string (optional)",
  "budget": "number (optional)",
  "duration_months": "number (optional)",
  "beneficiaries": "array (optional)"
}
```

## 🔧 API Reference

### Wallet Management

```bash
# Generate new wallet
python wallet_utils.py --generate

# Show wallet info
python wallet_utils.py --info
```

### Proposal Anchoring

```bash
# Anchor from file
python anchor_proposal.py --file proposal.json

# Anchor from stdin
python anchor_proposal.py --stdin

# Use example proposal
python anchor_proposal.py --example

# Save results to file
python anchor_proposal.py --file proposal.json --output results.json
```

### Proposal Verification

```bash
# Basic verification
python verify_proposal.py <tx_id>

# Show proposal content
python verify_proposal.py <tx_id> --show-proposal

# Save results
python verify_proposal.py <tx_id> --output results.json
```

## 🔍 How It Works

### Anchoring Process

1. **Proposal Input**: Accept JSON proposal via file, stdin, or example
2. **Hash Computation**: Compute SHA256 hash of normalized JSON
3. **IPFS Upload**: Upload proposal to IPFS and get CID
4. **Transaction Building**: Create Cardano transaction with metadata
5. **Blockchain Submission**: Submit transaction to Cardano testnet
6. **Confirmation**: Return transaction ID and metadata

### Verification Process

1. **Transaction Lookup**: Fetch transaction metadata from Blockfrost
2. **IPFS Retrieval**: Download proposal using stored IPFS CID
3. **Hash Comparison**: Compute hash of retrieved proposal
4. **Verification**: Compare computed hash with on-chain hash
5. **Result**: Report success/failure with details

## 🛡️ Security Considerations

- **Testnet Only**: This prototype is designed for Cardano testnet only
- **Wallet Security**: Keep your wallet files and mnemonics secure
- **API Keys**: Don't commit API keys to version control
- **Environment Variables**: Use `.env` file for sensitive configuration

## 🐛 Troubleshooting

### Common Issues

#### "No wallet found"
```bash
# Generate a wallet first
python wallet_utils.py --generate
```

#### "No UTxOs found"
```bash
# Fund your wallet with testnet ADA
# Visit: https://testnets.cardano.org/en/testnets/cardano/tools/faucet/
```

#### "IPFS connection failed"
```bash
# Check your Infura credentials in .env
# Ensure INFURA_PROJECT_ID and INFURA_PROJECT_SECRET are set
```

#### "Failed to submit transaction"
```bash
# Check your Blockfrost API key
# Ensure you have sufficient ADA in your wallet
# Verify network configuration (testnet)
```

### Debug Mode

Enable verbose logging by setting environment variable:
```bash
export PYTHONPATH=.
python -v anchor_proposal.py --example
```

## 📁 Project Structure

```
AI-Blockchain-Prototype/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── config.py                # Configuration management
├── wallet_utils.py          # Wallet management
├── anchor_proposal.py       # Proposal anchoring script
├── verify_proposal.py       # Proposal verification script
├── wallet.json              # Generated wallet (keep secure!)
└── wallet_mnemonic.txt      # Generated mnemonic (keep secure!)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is a prototype for educational and testing purposes only. Do not use for production applications without proper security audits and testing.

## 🔗 Useful Links

- [Cardano Documentation](https://docs.cardano.org/)
- [PyCardano Documentation](https://pycardano.readthedocs.io/)
- [Blockfrost API Documentation](https://docs.blockfrost.io/)
- [IPFS Documentation](https://docs.ipfs.io/)
- [Cardano Testnet Faucet](https://testnets.cardano.org/en/testnets/cardano/tools/faucet/)