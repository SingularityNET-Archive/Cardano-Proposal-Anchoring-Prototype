# Cardano Proposal Anchoring Prototype

A minimal working Python prototype that anchors community proposals to the Cardano blockchain using Blockfrost and PyCardano. The system uploads proposals to Arweave for permanent storage, computes SHA256 hashes, and anchors them as metadata in Cardano transactions on the testnet.

## 🏗️ Architecture

```
Proposal JSON → Arweave Upload → Hash Computation → Cardano Transaction → Blockchain
     ↓              ↓              ↓                    ↓              ↓
   JSON File    Arweave TX ID   SHA256 Hash         Metadata         On-chain
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
BLOCKFROST_NETWORK=preview

# Arweave Configuration
ARWEAVE_GATEWAY_URL=https://arweave.net
ARWEAVE_KEY_FILE=arweave_key.json
ARWEAVE_NETWORK=mainnet

# Cardano Network Configuration
CARDANO_NETWORK=testnet
METADATA_LABEL=1337
```

### 3. Get API Keys

#### Blockfrost API Key
1. Visit [Blockfrost.io](https://blockfrost.io/)
2. Sign up for a free account
3. Create a new project for Cardano (choose mainnet, preview, or preprod)
4. Copy your API key to `.env`
5. Set `BLOCKFROST_NETWORK` to match your project (mainnet/preview/preprod)

#### Arweave Wallet
1. Visit [Arweave.org](https://www.arweave.org/)
2. Download the Arweave wallet or use [ArConnect](https://arconnect.io/)
3. Create a new wallet and save the key file as `arweave_key.json`
4. Fund your wallet with AR tokens (see funding instructions below)

### 4. Generate Wallet

```bash
# Generate a new testnet wallet
python wallet_utils.py --generate
```

This will create:
- `wallet.json` - Wallet keys (keep secure!)
- `wallet_mnemonic.txt` - Recovery phrase (keep secure!)

### 5. Fund Your Wallets

#### Cardano Wallet (for transaction fees)
1. Copy the payment address from the wallet generation output
2. For **preview/preprod networks**: Visit the [Cardano Testnet Faucet](https://testnets.cardano.org/en/testnets/cardano/tools/faucet/)
3. For **mainnet**: Transfer ADA from an exchange or wallet
4. Request testnet ADA for your address (preview/preprod only)
5. Wait for the transaction to confirm

#### Arweave Wallet (for permanent storage)
1. Get AR tokens from exchanges like [KuCoin](https://www.kucoin.com/), [Gate.io](https://www.gate.io/), or [Binance](https://www.binance.com/)
2. Transfer AR to your Arweave wallet address
3. You need approximately 0.1-0.5 AR for each upload (cost varies with data size)

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
3. **Arweave Upload**: Upload proposal to Arweave for permanent storage
4. **Transaction Building**: Create Cardano transaction with metadata
5. **Blockchain Submission**: Submit transaction to Cardano testnet
6. **Confirmation**: Return transaction ID and Arweave permanent URL

### Verification Process

1. **Transaction Lookup**: Fetch transaction metadata from Blockfrost
2. **Arweave Retrieval**: Download proposal using stored Arweave transaction ID
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
# Fund your wallet with ADA
# Preview/Preprod: https://testnets.cardano.org/en/testnets/cardano/tools/faucet/
# Mainnet: Transfer ADA from exchange or wallet
```

#### "Arweave key file not found"
```bash
# Create your Arweave wallet key file
# Download from Arweave wallet or ArConnect
# Save as arweave_key.json in the project directory
```

#### "Insufficient AR balance"
```bash
# Check your AR balance
python arweave_utils.py --check-balance

# Fund your Arweave wallet with AR tokens
# You need approximately 0.1-0.5 AR per upload
```

#### "Failed to submit transaction"
```bash
# Check your Blockfrost API key
# Ensure you have sufficient ADA in your wallet
# Verify network configuration (mainnet/preview/preprod)
# Ensure your API key matches the selected network
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
├── arweave_utils.py         # Arweave utilities
├── wallet.json              # Generated wallet (keep secure!)
├── wallet_mnemonic.txt      # Generated mnemonic (keep secure!)
└── arweave_key.json         # Arweave wallet key (keep secure!)
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
- [Arweave Documentation](https://docs.arweave.org/)
- [Arweave Wallet](https://www.arweave.org/wallet)
- [ArConnect Browser Extension](https://arconnect.io/)
- [Cardano Testnet Faucet](https://testnets.cardano.org/en/testnets/cardano/tools/faucet/)
- [AR Token Exchanges](https://www.coingecko.com/en/coins/arweave)