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
