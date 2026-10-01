"""
Dating App Conversation Research Framework

A research tool for studying conversation patterns using synthetic simulation.

WARNING: This tool is designed for academic research on SYNTHETIC data ONLY.
Using this against real Tinder or deceiving real users violates:
- Tinder Terms of Service
- Research ethics standards (IRB)
- Privacy regulations (GDPR, CCPA)
- Potentially criminal laws

See ETHICS_FRAMEWORK.md before using this tool.
"""

__version__ = "0.1.0"
__author__ = "Research Team"

from .utils.config import Config
from .utils.logging import setup_logging

# Initialize logging
setup_logging()

__all__ = ["Config", "setup_logging"]
