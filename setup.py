#!/usr/bin/env python3
"""Setup script for Cardano Proposal Anchoring package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cardano-proposal-anchoring",
    version="1.0.0",
    author="Your Name",
    description="Anchor community proposals to Cardano blockchain with Arweave storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AI-Blockchain-Prototype",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "anchor-proposal=src.commands.anchor_proposal:main",
            "verify-proposal=src.commands.verify_proposal:main",
            "cardano-wallet=src.core.wallet_utils:main",
        ],
    },
)
