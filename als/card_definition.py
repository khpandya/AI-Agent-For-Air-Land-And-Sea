"""Immutable card blueprint — one per unique card in the game."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from als.enums import AbilityTiming, TheaterType

if TYPE_CHECKING:
    from als.abilities import TacticalAbility


@dataclass(frozen=True)
class CardDefinition:
    """The immutable blueprint for one of the 18 battle cards.

    Strength-6 cards have no ability (ability_timing and ability are None).
    """

    card_id: int
    name: str
    theater_type: TheaterType
    printed_strength: int
    ability_timing: Optional[AbilityTiming] = None
    ability: Optional[TacticalAbility] = None

    def __post_init__(self) -> None:
        if not 0 <= self.card_id <= 17:
            raise ValueError(f"card_id must be 0-17, got {self.card_id}")
        if not 1 <= self.printed_strength <= 6:
            raise ValueError(f"printed_strength must be 1-6, got {self.printed_strength}")

    def __repr__(self) -> str:
        label = self.name if self.name else f"{self.theater_type.name} {self.printed_strength}"
        return f"CardDefinition({self.card_id}, {label!r})"
