#!/bin/bash
# Convenience script to activate virtual environment and set PYTHONPATH

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Set PYTHONPATH to include project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

echo "✅ Virtual environment activated"
echo "✅ PYTHONPATH configured"
echo ""
echo "📝 You can now run:"
echo "   python anchor_proposal.py --example"
echo "   python verify_proposal.py <tx_id>"
echo "   python wallet_utils.py --info"
echo "   python scripts/check_status.py"
echo ""
echo "💡 To deactivate: deactivate"

