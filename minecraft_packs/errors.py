"""Exception type shared by every stage of loading, fetching, building and verifying a pack."""


class PackError(Exception):
    """Raised when a pack cannot be loaded, fetched, built or verified."""
