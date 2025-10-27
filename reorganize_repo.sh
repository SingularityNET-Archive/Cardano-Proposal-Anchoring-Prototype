#!/bin/bash
# Script to reorganize the Cardano Proposal Anchoring Prototype repository

echo "🔄 Reorganizing repository structure..."

# Create new directory structure
echo "📁 Creating directories..."
mkdir -p src/core
mkdir -p src/commands
mkdir -p src/utils
mkdir -p scripts
mkdir -p docs
mkdir -p tests
mkdir -p examples
mkdir -p wallet

# Create __init__.py files for Python packages
echo "📝 Creating __init__.py files..."
touch src/__init__.py
touch src/core/__init__.py
touch src/commands/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# Move core utilities
echo "🔧 Moving core utilities..."
[ -f wallet_utils.py ] && mv wallet_utils.py src/core/
[ -f arweave_utils.py ] && mv arweave_utils.py src/core/
[ -f config.py ] && mv config.py src/

# Move command scripts
echo "📋 Moving command scripts..."
[ -f anchor_proposal.py ] && mv anchor_proposal.py src/commands/
[ -f verify_proposal.py ] && mv verify_proposal.py src/commands/

# Move helper scripts
echo "🔨 Moving helper scripts..."
[ -f check_status.py ] && mv check_status.py scripts/
[ -f check_arweave_balance.py ] && mv check_arweave_balance.py scripts/
[ -f test_blockfrost.py ] && mv test_blockfrost.py scripts/

# Move documentation
echo "📚 Moving documentation..."
[ -f ARWEAVE_SETUP.md ] && mv ARWEAVE_SETUP.md docs/

# Create wrapper scripts in root for backwards compatibility
echo "🔗 Creating wrapper scripts..."

cat > anchor_proposal.py << 'EOF'
#!/usr/bin/env python3
"""Wrapper script for backwards compatibility."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commands.anchor_proposal import main

if __name__ == "__main__":
    main()
EOF

cat > verify_proposal.py << 'EOF'
#!/usr/bin/env python3
"""Wrapper script for backwards compatibility."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commands.verify_proposal import main

if __name__ == "__main__":
    main()
EOF

cat > wallet_utils.py << 'EOF'
#!/usr/bin/env python3
"""Wrapper script for backwards compatibility."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.wallet_utils import main

if __name__ == "__main__":
    main()
EOF

# Make wrapper scripts executable
chmod +x anchor_proposal.py verify_proposal.py wallet_utils.py

# Create documentation files
echo "📄 Creating documentation files..."

cat > docs/ARCHITECTURE.md << 'EOF'
# Architecture Documentation

## System Overview

[Architecture details here]

## Component Diagram

[Diagram here]

## Data Flow

[Data flow details here]
EOF

cat > docs/API.md << 'EOF'
# API Reference

## Command Line Interface

[CLI documentation here]

## Python API

[Python API documentation here]
EOF

cat > docs/TROUBLESHOOTING.md << 'EOF'
# Troubleshooting Guide

## Common Issues

[Troubleshooting content here]
EOF

cat > wallet/README.md << 'EOF'
# Wallet Directory

This directory is for storing your wallet files securely.

**Files that will be generated here:**
- `wallet.json` - Your Cardano wallet keys (keep secure!)
- `wallet_mnemonic.txt` - Your recovery phrase (keep secure!)
- `*.json` - Your Arweave wallet key files (keep secure!)

⚠️ **IMPORTANT**: Never commit these files to version control!
EOF

cat > examples/example_proposal.json << 'EOF'
{
  "title": "Community Development Initiative",
  "description": "A proposal to improve community infrastructure and engagement",
  "proposer": "Community Lead",
  "timestamp": 1703001600,
  "category": "infrastructure",
  "budget": 10000,
  "duration_months": 6,
  "beneficiaries": ["community_members", "local_businesses"]
}
EOF

cat > examples/anchor_example.py << 'EOF'
#!/usr/bin/env python3
"""Example script showing how to anchor a proposal."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from commands.anchor_proposal import ProposalAnchorer

def main():
    """Anchor an example proposal."""
    anchorer = ProposalAnchorer()
    
    # Example proposal
    proposal = {
        "title": "Example Proposal",
        "description": "This is an example",
        "proposer": "Example User"
    }
    
    result = anchorer.anchor_proposal(proposal)
    print(f"Transaction ID: {result['transaction_id']}")
    print(f"Arweave URL: {result['arweave_url']}")

if __name__ == "__main__":
    main()
EOF

chmod +x examples/anchor_example.py

echo "✅ Repository reorganization complete!"
echo ""
echo "📂 New structure created:"
echo "   - src/core/        - Core utilities (wallet, arweave)"
echo "   - src/commands/    - Main command scripts"
echo "   - src/utils/       - Helper utilities"
echo "   - scripts/         - Helper scripts"
echo "   - docs/            - Documentation files"
echo "   - tests/           - Test files (ready for tests)"
echo "   - examples/        - Example usage"
echo "   - wallet/          - Wallet storage directory"
echo ""
echo "⚠️  Note: Wrapper scripts created in root for backwards compatibility"
echo "📝 Next steps:"
echo "   1. Update import statements in moved files"
echo "   2. Test the wrapper scripts"
echo "   3. Update README.md with new structure"
echo "   4. Consider creating a proper Python package with setup.py"

