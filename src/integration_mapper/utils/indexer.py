"""
ComponentIndexer: Maps fully qualified names (FQNs) to integer IDs for compression.

This module provides bidirectional mapping between FQNs and compact integer IDs,
reducing token usage by replacing repeated long FQN strings with small integers.

Example:
    >>> indexer = ComponentIndexer()
    >>> id1 = indexer.get_or_create_id("myapp.models.user.User.save")
    >>> id2 = indexer.get_or_create_id("myapp.models.user.User.save")  # Same ID
    >>> assert id1 == id2
    >>> index = indexer.to_json_index()
    >>> print(index["1"])  # "myapp.models.user.User.save"
"""

from typing import Dict


class ComponentIndexer:
    """Maps fully qualified names to integer IDs for compression.

    Provides bidirectional mapping (FQN ↔ ID) for use in compact JSON output.
    Each unique FQN is assigned an incrementing integer ID to reduce token usage
    from repeated long strings.

    Attributes:
        fqn_to_id: Dict mapping FQN strings to integer IDs
        id_to_fqn: Dict mapping integer IDs to FQN strings
        next_id: Counter for next available ID
    """

    def __init__(self) -> None:
        """Initialize empty indexer with no components."""
        self.fqn_to_id: Dict[str, int] = {}
        self.id_to_fqn: Dict[int, str] = {}
        self.next_id: int = 1

    def get_or_create_id(self, fqn: str) -> int:
        """Get existing ID for FQN or create new one.

        Args:
            fqn: Fully qualified name (e.g., "myapp.models.User.save")

        Returns:
            Integer ID (1-based) for this FQN. Same FQN always returns same ID.

        Example:
            >>> indexer = ComponentIndexer()
            >>> id1 = indexer.get_or_create_id("myapp.User")
            >>> id2 = indexer.get_or_create_id("myapp.User")
            >>> assert id1 == id2 == 1
        """
        if fqn not in self.fqn_to_id:
            new_id = self.next_id
            self.fqn_to_id[fqn] = new_id
            self.id_to_fqn[new_id] = fqn
            self.next_id += 1
            return new_id
        return self.fqn_to_id[fqn]

    def to_json_index(self) -> Dict[str, str]:
        """Export index as JSON-compatible dict.

        Returns:
            Dictionary mapping string IDs to FQN strings suitable for JSON output.
            Keys are stringified integers (required for JSON).

        Example:
            >>> indexer = ComponentIndexer()
            >>> indexer.get_or_create_id("myapp.models.User")
            >>> index = indexer.to_json_index()
            >>> print(index)
            {"1": "myapp.models.User"}
        """
        return {str(idx): fqn for idx, fqn in self.id_to_fqn.items()}

    def get_id(self, fqn: str) -> int:
        """Get ID for FQN without creating new entry.

        Args:
            fqn: Fully qualified name to look up

        Returns:
            Integer ID if FQN exists, -1 if not found

        Raises:
            KeyError: If FQN not in index
        """
        return self.fqn_to_id[fqn]

    def get_fqn(self, idx: int) -> str:
        """Get FQN for ID.

        Args:
            idx: Integer ID to look up

        Returns:
            FQN string for this ID

        Raises:
            KeyError: If ID not in index
        """
        return self.id_to_fqn[idx]

    def __len__(self) -> int:
        """Return number of indexed components."""
        return len(self.fqn_to_id)

    def __contains__(self, fqn: str) -> bool:
        """Check if FQN is in index."""
        return fqn in self.fqn_to_id
