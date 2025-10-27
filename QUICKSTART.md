# 🚀 Quick Start Guide

## ✅ Issue Resolved: Module Import Errors

After the repository reorganization, you might see errors like:
```
ModuleNotFoundError: No module named 'config'
```

This is because Python needs to know where to find the `src/` directory.

---

## 📋 Three Ways to Run the Scripts

### **Option 1: Use Wrapper Scripts (Easiest)** ⭐ RECOMMENDED

The wrapper scripts automatically handle all paths for you:

```bash
# Activate your virtual environment first
source venv/bin/activate

# Then run any wrapper script
python anchor_proposal.py --example
python verify_proposal.py <tx_id>
python wallet_utils.py --info
```

**✅ This is the recommended way!**

---

### **Option 2: Use the Activation Script**

Source the `activate.sh` script to set up your environment:

```bash
# One-time setup (makes activate.sh executable)
chmod +x activate.sh

# Then, whenever you start a new terminal:
source activate.sh
```

This will:
- ✅ Activate the virtual environment
- ✅ Set PYTHONPATH correctly
- ✅ Show you available commands

Now you can run scripts directly:

```bash
python scripts/check_status.py
python scripts/check_arweave_balance.py
python -c "from src.config import BLOCKFROST_NETWORK; print(BLOCKFROST_NETWORK)"
```

---

### **Option 3: Manual PYTHONPATH Setup**

If you prefer manual control:

```bash
# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH (do this in each new terminal)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Now run any script
python scripts/check_status.py
```

---

## 🎯 Common Commands

Once your environment is set up (using any option above):

```bash
# Check overall system status
python scripts/check_status.py

# Check Arweave balance
python scripts/check_arweave_balance.py

# Anchor a proposal (using example)
python anchor_proposal.py --example

# Anchor a custom proposal
python anchor_proposal.py --file my_proposal.json

# Verify a proposal
python verify_proposal.py <cardano_tx_id>

# Generate new wallet
python wallet_utils.py --generate

# Show wallet info
python wallet_utils.py --info
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'config'" or similar

**Solution**: You forgot to set PYTHONPATH or use the wrapper scripts.

**Quick Fix**:
```bash
# Either use the wrapper scripts (recommended):
python anchor_proposal.py --example

# Or set PYTHONPATH:
export PYTHONPATH="$(pwd):$PYTHONPATH"
```

### "Virtual environment not activated"

**Solution**: Activate it first:
```bash
source venv/bin/activate
```

### "Network errors" when checking Arweave balance

**Solution**: This is normal in sandboxed environments. Use:
```bash
python scripts/check_arweave_balance.py
```
with network permissions if needed.

---

## 📁 New Project Structure

After reorganization:

```
AI-Blockchain-Prototype/
├── src/                          # Core source code
│   ├── config.py                 # Configuration management
│   ├── core/
│   │   ├── wallet_utils.py       # Cardano wallet utilities
│   │   └── arweave_utils.py      # Arweave operations
│   └── commands/
│       ├── anchor_proposal.py    # Main anchoring logic
│       └── verify_proposal.py    # Verification logic
├── scripts/                      # Utility scripts
│   ├── check_status.py
│   ├── check_arweave_balance.py
│   └── test_blockfrost.py
├── anchor_proposal.py            # ← Wrapper (use this!)
├── verify_proposal.py            # ← Wrapper (use this!)
├── wallet_utils.py               # ← Wrapper (use this!)
├── activate.sh                   # ← Convenience script
└── README.md
```

---

## 💡 Pro Tips

1. **Always use wrapper scripts** from the project root - they handle everything automatically
2. **Use `activate.sh`** if you need to run multiple commands in a session
3. **Check status first** before anchoring: `python scripts/check_status.py`
4. **Keep your virtual environment activated** while working on the project

---

## ✅ Verify Your Setup

Run this quick test:

```bash
source venv/bin/activate
python anchor_proposal.py --help
```

If you see the help message, you're all set! 🎉

---

**Need more help?** Check the main [README.md](README.md) for detailed documentation.

