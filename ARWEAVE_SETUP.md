# Arweave Wallet Setup Guide

## Your Arweave Configuration

Your `.env` file should contain:
```env
ARWEAVE_KEY_FILE=your_arweave_wallet_key.json
```

Replace `your_arweave_wallet_key.json` with your actual Arweave key file name.

## Quick Setup Checklist

- [ ] Downloaded Arweave key file (e.g., `your_arweave_wallet_key.json`)
- [ ] Placed key file in project directory
- [ ] Updated `.env` with `ARWEAVE_KEY_FILE=your_arweave_wallet_key.json`
- [ ] Checked wallet balance: `python check_arweave_balance.py`
- [ ] Funded wallet with AR tokens (if needed)

## Commands

### Check Wallet Balance
```bash
# Using the helper script (reads from .env)
python check_arweave_balance.py

# Using arweave_utils directly
python arweave_utils.py --check-balance
```

### Get Wallet Address
```bash
# Your wallet address is displayed when you check balance
python check_arweave_balance.py
```

### Fund Your Wallet

Purchase AR tokens from exchanges:
- **KuCoin**: https://www.kucoin.com/
- **Gate.io**: https://www.gate.io/
- **Binance**: https://www.binance.com/

Minimum recommended: **0.5 AR** (covers ~5 proposal uploads)

### Test Upload

Once your wallet has AR tokens:
```bash
# Test with example proposal
python anchor_proposal.py --example
```

## Expected Costs

- **Small proposal (<10KB)**: ~0.05-0.1 AR
- **Medium proposal (<100KB)**: ~0.1-0.2 AR
- **Large proposal (<1MB)**: ~0.3-0.5 AR

**Note**: These are approximate costs. Actual costs vary based on:
- Data size
- Current network demand
- Arweave network fees

## Troubleshooting

### "Arweave key file not found"
```bash
# Check if file exists
ls -la your_arweave_wallet_key.json

# Verify .env configuration
cat .env | grep ARWEAVE_KEY_FILE
```

### "Insufficient AR balance"
```bash
# Check current balance
python check_arweave_balance.py

# Fund your wallet from an exchange
# Send AR to your wallet address
```

### "Invalid key file format"
```bash
# Verify JSON format
python -c "import json; print(json.load(open('your_arweave_wallet_key.json')))"
```

## Security Notes

- ✅ Your key file is in `.gitignore` and won't be committed
- ⚠️ **Never** share your key file publicly
- ⚠️ **Never** commit your key file to version control
- ✅ Keep a backup of your key file in a secure location
- ✅ Consider using a separate wallet for testing vs production

## Next Steps

After setting up Arweave:

1. ✅ Check balance: `python check_arweave_balance.py`
2. ✅ Ensure you have at least 0.5 AR
3. ✅ Test with example: `python anchor_proposal.py --example`
4. ✅ Verify the proposal: `python verify_proposal.py <tx_id>`

## Support

If you encounter issues:
- Check the main README.md troubleshooting section
- Verify your `.env` file configuration
- Ensure your key file is valid JSON
- Check Arweave network status: https://viewblock.io/arweave

