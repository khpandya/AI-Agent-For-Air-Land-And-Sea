"""Mutable card state during a battle."""

from __future__ import annotations

from typing import Optional

from als.card_definition import CardDefinition
from als.enums import CardOrientation, CardZone, TheaterType
from als.types import TheaterPosition


class CardInstance:
    """A card in play — tracks orientation, zone, owner, and location."""

    def __init__(self, definition: CardDefinition) -> None:
        self.definition = definition
        self.orientation = CardOrientation.FACEDOWN
        self.zone = CardZone.DECK
        self.owner: Optional[int] = None
        self.theater_position: Optional[TheaterPosition] = None

    # --- Properties ---

    @property
    def card_id(self) -> int:
        return self.definition.card_id

    @property
    def theater_type(self) -> TheaterType:
        return self.definition.theater_type

    @property
    def printed_strength(self) -> int:
        return self.definition.printed_strength

    @property
    def is_faceup(self) -> bool:
        return self.orientation == CardOrientation.FACEUP

    @property
    def is_facedown(self) -> bool:
        return self.orientation == CardOrientation.FACEDOWN

    @property
    def effective_strength(self) -> int:
        """Base effective strength: 2 if facedown, else printed strength.

        Does NOT include ongoing modifiers (Support, Cover Fire, Escalation).
        Those are computed by StrengthCalculator.
        """
        if self.is_facedown:
            return 2
        return self.definition.printed_strength

    @property
    def has_active_ability(self) -> bool:
        """True if this card is faceup and has an ability."""
        return self.is_faceup and self.definition.ability is not None

    def __repr__(self) -> str:
        orient = "UP" if self.is_faceup else "DN"
        label = self.definition.name or f"{self.theater_type.name}{self.printed_strength}"
        return f"CardInstance({label}, {orient}, {self.zone.name})"
