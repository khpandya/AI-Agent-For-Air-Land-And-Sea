"""Theater and player stack models."""

from __future__ import annotations

from typing import Optional

from als.card_instance import CardInstance
from als.enums import TheaterType
from als.types import TheaterPosition


class PlayerTheaterStack:
    """A player's ordered stack of cards in one theater.

    The last element ([-1]) is the uncovered (topmost) card;
    everything before it is covered. Covered/uncovered status is
    derived from position, never stored as a separate flag.
    """

    def __init__(self) -> None:
        self._cards: list[CardInstance] = []

    @property
    def cards(self) -> list[CardInstance]:
        return list(self._cards)

    @property
    def uncovered_card(self) -> Optional[CardInstance]:
        return self._cards[-1] if self._cards else None

    @property
    def covered_cards(self) -> list[CardInstance]:
        return list(self._cards[:-1]) if len(self._cards) > 1 else []

    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0

    @property
    def card_count(self) -> int:
        return len(self._cards)

    def place_on_top(self, card: CardInstance) -> None:
        self._cards.append(card)

    def remove_card(self, card: CardInstance) -> None:
        self._cards.remove(card)

    def is_uncovered(self, card: CardInstance) -> bool:
        return len(self._cards) > 0 and self._cards[-1] is card

    def is_covered(self, card: CardInstance) -> bool:
        return card in self._cards and not self.is_uncovered(card)

    def cards_covered_by(self, card: CardInstance) -> list[CardInstance]:
        """Return all cards below the given card in the stack."""
        if card not in self._cards:
            return []
        idx = self._cards.index(card)
        return list(self._cards[:idx])

    def __repr__(self) -> str:
        return f"PlayerTheaterStack({self.card_count} cards)"


class Theater:
    """One theater on the battlefield."""

    def __init__(self, theater_type: TheaterType, position: TheaterPosition) -> None:
        self.theater_type = theater_type
        self.position = position
        self.stacks: dict[int, PlayerTheaterStack] = {}

    def get_stack(self, player_id: int) -> PlayerTheaterStack:
        if player_id not in self.stacks:
            self.stacks[player_id] = PlayerTheaterStack()
        return self.stacks[player_id]

    def total_card_count(self) -> int:
        return sum(stack.card_count for stack in self.stacks.values())

    def all_cards(self) -> list[CardInstance]:
        result: list[CardInstance] = []
        for stack in self.stacks.values():
            result.extend(stack.cards)
        return result

    def __repr__(self) -> str:
        return f"Theater({self.theater_type.name}, pos={self.position.index})"
