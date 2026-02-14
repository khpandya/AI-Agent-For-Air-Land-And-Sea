"""Victory point scoring calculator."""

from __future__ import annotations

from als.enums import BattleEndReason, PlayerPosition


def calculate_vps(
    battle_end_reason: BattleEndReason,
    withdrawing_player_position: PlayerPosition | None,
    cards_remaining_in_hand: int,
    beginner_mode: bool = False,
) -> int:
    """Calculate VPs the winner earns for this battle.

    Args:
        battle_end_reason: How the battle ended.
        withdrawing_player_position: The PlayerPosition of the withdrawing player
            (FIRST or SECOND). None if no withdrawal.
        cards_remaining_in_hand: Number of cards left in the withdrawing player's hand.
        beginner_mode: If True, always return 1 VP.

    Returns:
        Number of victory points the winner earns.
    """
    if beginner_mode:
        return 1

    if battle_end_reason == BattleEndReason.ALL_CARDS_PLAYED:
        return 6

    # Withdrawal scoring depends on who withdrew
    assert withdrawing_player_position is not None
    n = cards_remaining_in_hand

    if withdrawing_player_position == PlayerPosition.FIRST:
        # 1st player withdraws
        if n >= 4:
            return 2
        if n >= 2:
            return 3
        if n == 1:
            return 4
        return 6  # n == 0

    # 2nd player withdraws
    if n >= 5:
        return 2
    if n >= 3:
        return 3
    if n == 2:
        return 4
    return 6  # n <= 1
