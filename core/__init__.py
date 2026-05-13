"""
Core module for PGP Email Simulation
Contains shared models and PGP functionality.
"""

from .email_message import EmailMessage
from .key_manager import KeyManager
from .pgp_handler import PGPHandler

__all__ = ["EmailMessage", "KeyManager", "PGPHandler"]