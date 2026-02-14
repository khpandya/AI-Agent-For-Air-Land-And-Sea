"""Value types for the game domain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TheaterPosition:
    """Position of a theater in the row (0, 1, or 2).

    Adjacency: middle (1) is adjacent to both outer positions;
    outer positions (0, 2) are NOT adjacent to each other.
    """

    index: int

    def __post_init__(self) -> None:
        if self.index not in (0, 1, 2):
            raise ValueError(f"Theater position must be 0, 1, or 2, got {self.index}")

    def is_adjacent_to(self, other: TheaterPosition) -> bool:
        return abs(self.index - other.index) == 1
