"""Effective strength calculator with ongoing modifier application."""

from __future__ import annotations

from als.abilities_impl import CoverFireAbility, EscalationAbility, SupportAbility
from als.game_state import BattleState
from als.theater import Theater


def calculate_theater_strength(
    battle_state: BattleState, theater: Theater, player_id: int
) -> int:
    """Compute total effective strength for a player in a theater.

    Applies ongoing modifiers:
    - Support: +3 to owning player in each adjacent theater
    - Cover Fire: Cards covered by an active Cover Fire card have strength 4
    - Escalation: Owning player's facedown cards have strength 4
    """
    stack = theater.get_stack(player_id)
    if stack.is_empty:
        return 0

    # Build per-card strength overrides
    card_strengths: dict[int, int] = {}  # card id() -> strength

    # Start with base effective strength for each card
    for card in stack.cards:
        card_strengths[id(card)] = card.effective_strength

    # Apply Cover Fire: cards covered by an active Cover Fire have strength 4
    active_ongoing = battle_state.get_active_ongoing_abilities()
    for ability_card, ability_owner in active_ongoing:
        ability = ability_card.definition.ability
        if isinstance(ability, CoverFireAbility) and ability_owner == player_id:
            # Find the stack this Cover Fire card is in
            if ability_card.theater_position == theater.position:
                covered = stack.cards_covered_by(ability_card)
                for c in covered:
                    card_strengths[id(c)] = 4

    # Apply Escalation: owning player's facedown cards have strength 4
    for ability_card, ability_owner in active_ongoing:
        ability = ability_card.definition.ability
        if isinstance(ability, EscalationAbility) and ability_owner == player_id:
            for card in stack.cards:
                if card.is_facedown:
                    card_strengths[id(card)] = 4

    total = sum(card_strengths.values())

    # Apply Support: +3 from adjacent theaters
    for ability_card, ability_owner in active_ongoing:
        ability = ability_card.definition.ability
        if isinstance(ability, SupportAbility) and ability_owner == player_id:
            if (
                ability_card.theater_position is not None
                and ability_card.theater_position != theater.position
                and ability_card.theater_position.is_adjacent_to(theater.position)
            ):
                total += 3

    return total


def calculate_all_strengths(
    battle_state: BattleState,
) -> dict[int, dict[int, int]]:
    """Return {theater_position_index: {player_id: strength}} for all theaters."""
    result: dict[int, dict[int, int]] = {}
    for theater in battle_state.theaters:
        result[theater.position.index] = {}
        for player_id in battle_state.players:
            result[theater.position.index][player_id] = calculate_theater_strength(
                battle_state, theater, player_id
            )
    return result
