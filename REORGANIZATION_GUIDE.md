# Repository Reorganization Guide

## 📋 Overview

This guide explains the new organized structure of the Cardano Proposal Anchoring Prototype and how to migrate to it.

## 🎯 Benefits of New Structure

✅ **Better Organization** - Clear separation of concerns  
✅ **Easier Maintenance** - Logical grouping of related files  
✅ **Professional Appearance** - Standard Python project layout  
✅ **Scalability** - Easy to add new features  
✅ **Testing Ready** - Dedicated test directory  
✅ **Documentation Focused** - Centralized docs folder  

## 📁 New Directory Structure

```
AI-Blockchain-Prototype/
│
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup script
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment template
│
├── docs/                        # 📚 Documentation
│   ├── ARWEAVE_SETUP.md        # Arweave wallet guide
│   ├── ARCHITECTURE.md         # System architecture
│   ├── API.md                  # API reference
│   └── TROUBLESHOOTING.md      # Troubleshooting guide
│
├── src/                         # 🔧 Source Code
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   │
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── wallet_utils.py     # Cardano wallet operations
│   │   ├── arweave_utils.py    # Arweave operations
│   │   └── blockchain_utils.py # Blockchain helpers
│   │
│   ├── commands/               # CLI commands
│   │   ├── __init__.py
│   │   ├── anchor_proposal.py  # Anchor command
│   │   └── verify_proposal.py  # Verify command
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── hash_utils.py       # Hashing functions
│       └── validators.py       # Input validation
│
├── scripts/                     # 🔨 Helper Scripts
│   ├── check_status.py         # System status checker
│   ├── check_arweave_balance.py # Arweave balance
│   └── test_blockfrost.py      # Blockfrost API test
│
├── tests/                       # 🧪 Tests
│   ├── __init__.py
│   ├── test_wallet.py          # Wallet tests
│   ├── test_arweave.py         # Arweave tests
│   └── test_anchoring.py       # Integration tests
│
├── examples/                    # 📝 Examples
│   ├── example_proposal.json   # Sample proposal
│   ├── anchor_example.py       # Anchoring example
│   └── verify_example.py       # Verification example
│
└── wallet/                      # 💼 Wallet Storage
    ├── .gitkeep
    └── README.md               # Wallet directory info
```

## 🔄 Migration Steps

### Option 1: Automated Migration (Recommended)

Run the reorganization script:

```bash
# Make script executable
chmod +x reorganize_repo.sh

# Run the reorganization
./reorganize_repo.sh

# Verify the new structure
tree -L 2 -I '__pycache__|*.pyc|venv'
```

### Option 2: Manual Migration

If you prefer manual control:

1. **Create directories:**
```bash
mkdir -p src/{core,commands,utils} scripts docs tests examples wallet
touch src/__init__.py src/core/__init__.py src/commands/__init__.py src/utils/__init__.py tests/__init__.py
```

2. **Move files:**
```bash
# Core files
mv wallet_utils.py src/core/
mv arweave_utils.py src/core/
mv config.py src/

# Commands
mv anchor_proposal.py src/commands/
mv verify_proposal.py src/commands/

# Scripts
mv check_status.py scripts/
mv check_arweave_balance.py scripts/
mv test_blockfrost.py scripts/

# Documentation
mv ARWEAVE_SETUP.md docs/
```

3. **Create wrapper scripts** (for backwards compatibility - see below)

## 🔗 Backwards Compatibility

The reorganization script creates wrapper scripts in the root directory, so existing commands still work:

```bash
# These still work!
python anchor_proposal.py --example
python verify_proposal.py <tx_id>
python wallet_utils.py --generate
```

The wrapper scripts automatically import from the new `src/` structure.

## 📦 Python Package Setup

Create `setup.py` for proper package installation:

```python
from setuptools import setup, find_packages

setup(
    name="cardano-proposal-anchoring",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pycardano>=0.12.0",
        "blockfrost-python>=0.4.0",
        "arweave-python-client>=0.2.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        'console_scripts': [
            'anchor-proposal=src.commands.anchor_proposal:main',
            'verify-proposal=src.commands.verify_proposal:main',
        ],
    },
)
```

Then install as a package:

```bash
pip install -e .
```

This allows you to use commands system-wide:

```bash
anchor-proposal --example
verify-proposal <tx_id>
```

## 📝 Update .gitignore

Add new patterns:

```gitignore
# Wallet directory
wallet/*.json
wallet/*.txt
!wallet/.gitkeep
!wallet/README.md

# Build artifacts
build/
dist/
*.egg-info/

# Tests
.pytest_cache/
.coverage
htmlcov/
```

## 🧪 Testing Setup

Create a basic test structure:

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📚 Documentation Organization

Move documentation to `docs/`:

- `docs/ARWEAVE_SETUP.md` - Arweave wallet setup
- `docs/ARCHITECTURE.md` - System architecture
- `docs/API.md` - API reference
- `docs/TROUBLESHOOTING.md` - Troubleshooting

## 🎯 Next Steps After Reorganization

1. ✅ **Update imports** - Fix import paths in moved files
2. ✅ **Test everything** - Ensure all scripts still work
3. ✅ **Update README** - Reference new structure
4. ✅ **Add tests** - Create unit tests in `tests/`
5. ✅ **CI/CD** - Set up GitHub Actions
6. ✅ **Documentation** - Complete docs in `docs/`

## 🔍 File Locations Quick Reference

| Old Location | New Location | Notes |
|-------------|--------------|-------|
| `wallet_utils.py` | `src/core/wallet_utils.py` | Core utility |
| `arweave_utils.py` | `src/core/arweave_utils.py` | Core utility |
| `config.py` | `src/config.py` | Configuration |
| `anchor_proposal.py` | `src/commands/anchor_proposal.py` | Command |
| `verify_proposal.py` | `src/commands/verify_proposal.py` | Command |
| `check_status.py` | `scripts/check_status.py` | Helper script |
| `ARWEAVE_SETUP.md` | `docs/ARWEAVE_SETUP.md` | Documentation |

## ⚠️ Important Notes

1. **Wrapper scripts** maintain backwards compatibility
2. **Import paths** need updating in moved files
3. **Wallet files** should now go in `wallet/` directory
4. **Tests** can be added incrementally
5. **Examples** help new users get started

## 🆘 Troubleshooting

### "Module not found" errors

Update your imports:

```python
# Old
from config import ...
from wallet_utils import ...

# New
from src.config import ...
from src.core.wallet_utils import ...
```

Or use the wrapper scripts which handle imports automatically.

### Scripts not working

Make sure you're in the project root and virtual environment is activated:

```bash
cd /path/to/AI-Blockchain-Prototype
source venv/bin/activate
```

## 📞 Support

If you encounter issues during reorganization:
1. Check this guide
2. Review the `reorganize_repo.sh` script
3. Manually move files if needed
4. Test each component individually

---

**The reorganized structure makes your project more professional, maintainable, and scalable!** 🚀

