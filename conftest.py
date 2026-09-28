"""Root conftest applying the isolation fixtures to every test."""

from tests.conftest import block_network

__all__ = ['block_network']
