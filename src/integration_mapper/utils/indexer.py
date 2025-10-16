"""Component ID indexer for token-efficient compression.

Maps fully qualified names to integer IDs to eliminate FQN string repetition.
Primary compression mechanism: 60% token reduction through ID references.
"""

from typing import Dict, Optional


class ComponentIndexer:
    """Maps fully qualified names to integer IDs for compression.

    This indexer maintains bidirectional mapping between fully qualified names (FQNs)
    and compact integer IDs. This allows replacing repeated FQN strings like
    "myapp.models.user.User.save" with short integer IDs like 142, providing
    ~60% token reduction for large codebases with many repeated references.

    Example:
        >>> indexer = ComponentIndexer()
        >>> id1 = indexer.get_or_create_id("myapp.models.User")
        >>> id2 = indexer.get_or_create_id("myapp.models.User")
        >>> assert id1 == id2  # Same FQN gets same ID
        >>> index = indexer.to_json_index()
        >>> assert index["1"] == "myapp.models.User"
    """

    def __init__(self) -> None:
        """Initialize the indexer with empty mappings."""
        self.fqn_to_id: Dict[str, int] = {}  # FQN string → integer ID
        self.id_to_fqn: Dict[int, str] = {}  # Integer ID → FQN string
        self.next_id: int = 1

    def get_or_create_id(self, fqn: str) -> int:
        """Get existing ID or assign new one for FQN.

        Args:
            fqn: Fully qualified name (e.g., "myapp.models.user.User.save")

        Returns:
            Integer ID (same for identical FQNs)

        Token savings: Replaces 40+ character strings with 1-3 character integers.
        """
        if fqn not in self.fqn_to_id:
            self.fqn_to_id[fqn] = self.next_id
            self.id_to_fqn[self.next_id] = fqn
            self.next_id += 1
        return self.fqn_to_id[fqn]

    def get_id(self, fqn: str) -> Optional[int]:
        """Get ID for FQN if it exists, return None otherwise."""
        return self.fqn_to_id.get(fqn)

    def get_fqn(self, id_: int) -> Optional[str]:
        """Get FQN for ID if it exists, return None otherwise."""
        return self.id_to_fqn.get(id_)

    def to_json_index(self) -> Dict[str, str]:
        """Export index for JSON output.

        Converts integer IDs to strings for JSON serialization.
        Format: {"1": "myapp.models.User", "2": "myapp.models.User.save", ...}

        Returns:
            Dictionary mapping string IDs to FQN strings.
        """
        return {str(id_): fqn for id_, fqn in self.id_to_fqn.items()}

    def get_stats(self) -> Dict[str, int]:
        """Get indexer statistics."""
        return {
            "total_components": len(self.id_to_fqn),
            "next_id": self.next_id
        }
