"""Game state containers: Deck, PlayerState, BattleState, GameState."""

from __future__ import annotations

import random
from typing import Any, Optional

from als.card_instance import CardInstance
from als.enums import (
    BattlePhase,
    CardOrientation,
    CardZone,
    GamePhase,
    PlayerPosition,
    TheaterType,
)
from als.theater import Theater
from als.types import TheaterPosition


class Deck:
    """Remaining cards pile."""

    def __init__(self, cards: Optional[list[CardInstance]] = None) -> None:
        self._cards: list[CardInstance] = list(cards) if cards else []

    @property
    def cards(self) -> list[CardInstance]:
        return list(self._cards)

    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0

    @property
    def size(self) -> int:
        return len(self._cards)

    def peek(self) -> Optional[CardInstance]:
        return self._cards[-1] if self._cards else None

    def draw(self) -> Optional[CardInstance]:
        if self._cards:
            card = self._cards.pop()
            return card
        return None

    def place_on_bottom(self, card: CardInstance) -> None:
        card.orientation = CardOrientation.FACEDOWN
        card.zone = CardZone.DECK
        card.owner = None
        card.theater_position = None
        self._cards.insert(0, card)

    def shuffle(self, rng: Optional[random.Random] = None) -> None:
        if rng:
            rng.shuffle(self._cards)
        else:
            random.shuffle(self._cards)


class PlayerState:
    """Per-player state within a battle."""

    def __init__(self, player_id: int, position: PlayerPosition) -> None:
        self.player_id = player_id
        self.position = position
        self.hand: list[CardInstance] = []
        self.victory_points: int = 0
        self.has_withdrawn: bool = False
        self.flags: dict[str, Any] = {}

    @property
    def cards_in_hand(self) -> int:
        return len(self.hand)

    def add_to_hand(self, card: CardInstance) -> None:
        card.zone = CardZone.HAND
        card.owner = self.player_id
        card.theater_position = None
        card.orientation = CardOrientation.FACEDOWN
        self.hand.append(card)

    def remove_from_hand(self, card: CardInstance) -> None:
        self.hand.remove(card)


class BattleState:
    """Complete state of one battle."""

    def __init__(
        self,
        theaters: list[Theater],
        players: dict[int, PlayerState],
        deck: Deck,
        active_player_id: int,
    ) -> None:
        self.theaters = theaters
        self.players = players
        self.deck = deck
        self.active_player_id = active_player_id
        self.turn_number: int = 1
        self.phase: BattlePhase = BattlePhase.PLAYER_TURN
        self.extra_turns: list[int] = []

    # --- Query methods ---

    def get_theater_at_position(self, index: int) -> Theater:
        for theater in self.theaters:
            if theater.position.index == index:
                return theater
        raise ValueError(f"No theater at position {index}")

    def get_theater_by_type(self, theater_type: TheaterType) -> Theater:
        for theater in self.theaters:
            if theater.theater_type == theater_type:
                return theater
        raise ValueError(f"No theater of type {theater_type}")

    def adjacent_theaters(self, theater: Theater) -> list[Theater]:
        return [
            t for t in self.theaters
            if t.position.is_adjacent_to(theater.position)
        ]

    def get_all_battlefield_cards(self, player_id: int) -> list[CardInstance]:
        result: list[CardInstance] = []
        for theater in self.theaters:
            stack = theater.get_stack(player_id)
            result.extend(stack.cards)
        return result

    def get_active_ongoing_abilities(self) -> list[tuple[CardInstance, int]]:
        """Return (card, player_id) for all faceup cards with ongoing abilities."""
        from als.enums import AbilityTiming

        result: list[tuple[CardInstance, int]] = []
        for theater in self.theaters:
            for player_id, stack in theater.stacks.items():
                for card in stack.cards:
                    if (
                        card.has_active_ability
                        and card.definition.ability is not None
                        and card.definition.ability.timing == AbilityTiming.ONGOING
                    ):
                        result.append((card, player_id))
        return result

    # --- Mutation methods ---

    def flip_card(self, card: CardInstance) -> None:
        if card.orientation == CardOrientation.FACEUP:
            card.orientation = CardOrientation.FACEDOWN
        else:
            card.orientation = CardOrientation.FACEUP

    def destroy_card(self, card: CardInstance) -> None:
        """Remove card from battlefield and place on bottom of deck."""
        if card.zone != CardZone.BATTLEFIELD:
            return
        # Remove from theater stack
        for theater in self.theaters:
            if card.theater_position == theater.position:
                for stack in theater.stacks.values():
                    if card in stack._cards:
                        stack.remove_card(card)
                        break
                break
        self.deck.place_on_bottom(card)

    def move_card(self, card: CardInstance, player_id: int, dest_theater: Theater) -> None:
        """Move a card from its current theater to another (same player's side)."""
        # Remove from old theater
        if card.theater_position is not None:
            old_theater = self.get_theater_at_position(card.theater_position.index)
            old_stack = old_theater.get_stack(player_id)
            old_stack.remove_card(card)

        # Place on top of destination
        card.theater_position = dest_theater.position
        dest_stack = dest_theater.get_stack(player_id)
        dest_stack.place_on_top(card)

    def play_card_to_theater(
        self,
        card: CardInstance,
        player_id: int,
        theater: Theater,
        orientation: CardOrientation,
    ) -> None:
        """Place a card on the battlefield in a theater."""
        card.orientation = orientation
        card.zone = CardZone.BATTLEFIELD
        card.owner = player_id
        card.theater_position = theater.position
        stack = theater.get_stack(player_id)
        stack.place_on_top(card)

    def return_card_to_hand(self, card: CardInstance, player_id: int) -> None:
        """Return a card from battlefield to player's hand."""
        if card.zone == CardZone.BATTLEFIELD and card.theater_position is not None:
            theater = self.get_theater_at_position(card.theater_position.index)
            stack = theater.get_stack(player_id)
            stack.remove_card(card)
        player = self.players[player_id]
        player.add_to_hand(card)

    def grant_extra_turn(self, player_id: int) -> None:
        self.extra_turns.append(player_id)

    def set_player_flag(self, player_id: int, flag: str, value: Any) -> None:
        self.players[player_id].flags[flag] = value

    def get_player_flag(self, player_id: int, flag: str, default: Any = None) -> Any:
        return self.players[player_id].flags.get(flag, default)


class GameState:
    """Top-level game state spanning a series of battles."""

    def __init__(
        self,
        player_ids: tuple[int, int],
        first_player_id: int,
        winning_score: int = 12,
    ) -> None:
        self.player_ids = player_ids
        self.first_player_id = first_player_id
        self.winning_score = winning_score
        self.phase: GamePhase = GamePhase.SETUP
        self.battle_number: int = 0
        self.theater_order: list[TheaterType] = [
            TheaterType.AIR, TheaterType.LAND, TheaterType.SEA
        ]
        self.current_battle: Optional[BattleState] = None

        # Player states persist across battles (for VP tracking)
        second_id = player_ids[1] if player_ids[0] == first_player_id else player_ids[0]
        self.players: dict[int, PlayerState] = {
            first_player_id: PlayerState(first_player_id, PlayerPosition.FIRST),
            second_id: PlayerState(second_id, PlayerPosition.SECOND),
        }

    def is_game_over(self) -> bool:
        return any(p.victory_points >= self.winning_score for p in self.players.values())

    def get_winner(self) -> Optional[int]:
        for pid, p in self.players.items():
            if p.victory_points >= self.winning_score:
                return pid
        return None

    def rotate_theater_order(self) -> None:
        """Shift theater boards one position (leftmost goes to rightmost)."""
        self.theater_order = self.theater_order[1:] + self.theater_order[:1]

    def swap_first_player(self) -> None:
        """Exchange Supreme Commander cards between battles."""
        for p in self.players.values():
            if p.position == PlayerPosition.FIRST:
                p.position = PlayerPosition.SECOND
            else:
                p.position = PlayerPosition.FIRST
        # Update first_player_id
        for pid, p in self.players.items():
            if p.position == PlayerPosition.FIRST:
                self.first_player_id = pid
                break
