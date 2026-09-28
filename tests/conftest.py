"""Global test fixtures enforcing isolation from the network."""

import socket
import urllib.request

import pytest


class UnmockedNetworkError(Exception):
    """Raised when a test attempts an unmocked network call."""


@pytest.fixture(autouse=True)
def block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Raise UnmockedNetworkError for any unmocked download or socket connection."""

    def refuse(*args: object, **kwargs: object) -> None:
        raise UnmockedNetworkError(
            f'Unmocked network call attempted: {args} {kwargs}. Serve it with tests.helpers.serve_mojang.'
        )

    monkeypatch.setattr(urllib.request, 'urlopen', refuse)
    monkeypatch.setattr(socket.socket, 'connect', refuse)
