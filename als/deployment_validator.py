"""Legal deployment checks and post-play triggered effects."""

from __future__ import annotations

from als.abilities_impl import AerodromeAbility, BlockadeAbility, ContainmentAbility
from als.card_instance import CardInstance
from als.enums import AbilityTiming, CardOrientation
from als.game_state import BattleState
from als.theater import Theater


def can_deploy_faceup(
    battle_state: BattleState,
    card: CardInstance,
    theater: Theater,
    player_id: int,
) -> bool:
    """Check if a faceup deployment of card to theater is legal.

    A faceup card must go to its matching theater, UNLESS:
    - Air Drop flag is active (one-time any-theater permission)
    - Aerodrome is active and card strength <= 3
    """
    # Matching theater is always OK
    if card.theater_type == theater.theater_type:
        return True

    # Air Drop flag allows any theater (one-time)
    if battle_state.get_player_flag(player_id, "air_drop_active", False):
        return True

    # Aerodrome: ongoing ability allowing strength <= 3 to non-matching
    active_ongoing = battle_state.get_active_ongoing_abilities()
    for ability_card, ability_owner in active_ongoing:
        if (
            isinstance(ability_card.definition.ability, AerodromeAbility)
            and ability_owner == player_id
            and card.printed_strength <= 3
        ):
            return True

    return False


def post_play_containment_check(
    battle_state: BattleState,
    played_card: CardInstance,
    player_id: int,
) -> bool:
    """Check if Containment triggers and destroys a facedown-played card.

    Returns True if the card should be destroyed.
    """
    if played_card.orientation != CardOrientation.FACEDOWN:
        return False

    active_ongoing = battle_state.get_active_ongoing_abilities()
    for ability_card, ability_owner in active_ongoing:
        if (
            isinstance(ability_card.definition.ability, ContainmentAbility)
            and ability_owner != player_id
        ):
            return True

    return False


def post_play_blockade_check(
    battle_state: BattleState,
    played_card: CardInstance,
    target_theater: Theater,
    cards_before_play: int,
) -> bool:
    """Check if Blockade triggers and destroys a card played to an adjacent theater.

    `cards_before_play` is the total card count in target_theater BEFORE this card
    was placed. Returns True if the card should be destroyed.
    """
    active_ongoing = battle_state.get_active_ongoing_abilities()
    for ability_card, ability_owner in active_ongoing:
        ability = ability_card.definition.ability
        if not isinstance(ability, BlockadeAbility):
            continue
        # Blockade's theater must be adjacent to the target theater
        if (
            ability_card.theater_position is not None
            and ability_card.theater_position.is_adjacent_to(target_theater.position)
            and cards_before_play >= 3
        ):
            return True

    return False
