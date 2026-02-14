"""Concrete implementations of all 13 tactical abilities.

Ongoing abilities that modify strength or deployment (Support, Cover Fire,
Escalation, Aerodrome, Containment, Blockade) are primarily checked by
StrengthCalculator and DeploymentValidator. Their execute() is a no-op.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from als.abilities import AbilityContext, TacticalAbility
from als.enums import AbilityTiming, CardOrientation, CardZone


# ---------------------------------------------------------------------------
# Ongoing abilities (strength/deployment modifiers — checked externally)
# ---------------------------------------------------------------------------

class SupportAbility(TacticalAbility):
    """Air 1 — Ongoing: +3 strength in each adjacent theater.

    Handled by StrengthCalculator. No execute() action needed.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.ONGOING, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return []

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        pass


class AerodromeAbility(TacticalAbility):
    """Air 4 — Ongoing: May deploy strength <= 3 cards to non-matching theaters.

    Handled by DeploymentValidator. No execute() action needed.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.ONGOING, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return []

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        pass


class ContainmentAbility(TacticalAbility):
    """Air 5 — Ongoing: Facedown-played cards are destroyed.

    Handled by DeploymentValidator post-play check. No execute() action needed.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.ONGOING, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return []

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        pass


class CoverFireAbility(TacticalAbility):
    """Land 4 — Ongoing: Cards covered by this card have strength 4.

    Handled by StrengthCalculator. No execute() action needed.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.ONGOING, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return []

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        pass


class EscalationAbility(TacticalAbility):
    """Sea 2 — Ongoing: Your facedown cards have strength 4.

    Handled by StrengthCalculator. No execute() action needed.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.ONGOING, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return []

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        pass


class BlockadeAbility(TacticalAbility):
    """Sea 5 — Ongoing: Card played to adjacent theater with 3+ existing cards
    is destroyed.

    Handled by DeploymentValidator post-play check. No execute() action needed.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.ONGOING, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return []

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        pass


# ---------------------------------------------------------------------------
# Instant abilities
# ---------------------------------------------------------------------------

@dataclass
class FlipChoice:
    """Choice for abilities that flip a card."""
    card_to_flip: Any  # CardInstance


@dataclass
class ReinforceChoice:
    """Choice for Reinforce: which adjacent theater to play to (or None to skip)."""
    target_theater_index: Optional[int]  # None = decline to play


@dataclass
class DisruptChoice:
    """Choice for Disrupt: opponent's card to flip, then your card to flip."""
    opponent_card_to_flip: Any  # CardInstance
    own_card_to_flip: Any  # CardInstance


@dataclass
class TransportChoice:
    """Choice for Transport: card to move and destination theater."""
    card_to_move: Any  # CardInstance
    destination_theater_index: int


@dataclass
class RedeployChoice:
    """Choice for Redeploy: facedown card to return to hand (or None to skip)."""
    card_to_return: Any  # Optional[CardInstance]


class AirDropAbility(TacticalAbility):
    """Air 2 — Instant: Next turn, may deploy to non-matching theater.

    Sets a flag on the player state.
    """

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return True

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        return [None]  # No choice needed — just sets the flag

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        ctx.battle_state.set_player_flag(ctx.source_player_id, "air_drop_active", True)


class ManeuverAbility(TacticalAbility):
    """Air 3 / Land 3 / Sea 3 — Instant: Flip any card in an adjacent theater."""

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=True)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return len(self.get_choices(ctx)) > 0

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        bs = ctx.battle_state
        source_pos = ctx.source_card.theater_position
        if source_pos is None:
            return []
        choices: list[FlipChoice] = []
        for theater in bs.theaters:
            if theater.position.is_adjacent_to(source_pos):
                for card in theater.all_cards():
                    choices.append(FlipChoice(card_to_flip=card))
        return choices

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        assert isinstance(choice, FlipChoice)
        ctx.battle_state.flip_card(choice.card_to_flip)


class AmbushAbility(TacticalAbility):
    """Land 2 — Instant: Flip any card in any theater."""

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=True)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return len(self.get_choices(ctx)) > 0

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        choices: list[FlipChoice] = []
        for theater in ctx.battle_state.theaters:
            for card in theater.all_cards():
                choices.append(FlipChoice(card_to_flip=card))
        return choices

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        assert isinstance(choice, FlipChoice)
        ctx.battle_state.flip_card(choice.card_to_flip)


class ReinforceAbility(TacticalAbility):
    """Land 1 — Instant: Peek top deck card, may play it facedown to adjacent theater."""

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=True)

    def is_possible(self, ctx: AbilityContext) -> bool:
        bs = ctx.battle_state
        return not bs.deck.is_empty and ctx.source_card.theater_position is not None

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        if not self.is_possible(ctx):
            return []
        bs = ctx.battle_state
        source_pos = ctx.source_card.theater_position
        if source_pos is None:
            return []
        choices: list[ReinforceChoice] = [ReinforceChoice(target_theater_index=None)]  # Decline
        for theater in bs.theaters:
            if theater.position.is_adjacent_to(source_pos):
                choices.append(ReinforceChoice(target_theater_index=theater.position.index))
        return choices

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        assert isinstance(choice, ReinforceChoice)
        if choice.target_theater_index is None:
            return  # Player declines
        bs = ctx.battle_state
        card = bs.deck.draw()
        if card is None:
            return
        target_theater = bs.get_theater_at_position(choice.target_theater_index)
        bs.play_card_to_theater(
            card, ctx.source_player_id, target_theater, CardOrientation.FACEDOWN
        )


class DisruptAbility(TacticalAbility):
    """Land 5 — Instant: Opponent flips one of theirs, then you flip one of yours."""

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=False)

    def is_possible(self, ctx: AbilityContext) -> bool:
        opponent_cards = ctx.battle_state.get_all_battlefield_cards(ctx.opponent_player_id)
        own_cards = ctx.battle_state.get_all_battlefield_cards(ctx.source_player_id)
        return len(opponent_cards) > 0 and len(own_cards) > 0

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        if not self.is_possible(ctx):
            return []
        bs = ctx.battle_state
        opponent_cards = bs.get_all_battlefield_cards(ctx.opponent_player_id)
        own_cards = bs.get_all_battlefield_cards(ctx.source_player_id)
        choices: list[DisruptChoice] = []
        for opp_card in opponent_cards:
            for own_card in own_cards:
                choices.append(DisruptChoice(
                    opponent_card_to_flip=opp_card,
                    own_card_to_flip=own_card,
                ))
        return choices

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        assert isinstance(choice, DisruptChoice)
        bs = ctx.battle_state
        bs.flip_card(choice.opponent_card_to_flip)
        bs.flip_card(choice.own_card_to_flip)


class TransportAbility(TacticalAbility):
    """Sea 1 — Instant: May move one of your cards to a different theater."""

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=True)

    def is_possible(self, ctx: AbilityContext) -> bool:
        return len(self.get_choices(ctx)) > 0

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        bs = ctx.battle_state
        own_cards = bs.get_all_battlefield_cards(ctx.source_player_id)
        choices: list[TransportChoice] = []
        for card in own_cards:
            for theater in bs.theaters:
                if card.theater_position != theater.position:
                    choices.append(TransportChoice(
                        card_to_move=card,
                        destination_theater_index=theater.position.index,
                    ))
        return choices

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        assert isinstance(choice, TransportChoice)
        bs = ctx.battle_state
        dest_theater = bs.get_theater_at_position(choice.destination_theater_index)
        bs.move_card(choice.card_to_move, ctx.source_player_id, dest_theater)


class RedeployAbility(TacticalAbility):
    """Sea 4 — Instant: Return a facedown card to hand; if you do, extra turn."""

    def __init__(self) -> None:
        super().__init__(AbilityTiming.INSTANT, is_optional=True)

    def is_possible(self, ctx: AbilityContext) -> bool:
        bs = ctx.battle_state
        own_cards = bs.get_all_battlefield_cards(ctx.source_player_id)
        return any(c.is_facedown for c in own_cards)

    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        bs = ctx.battle_state
        own_cards = bs.get_all_battlefield_cards(ctx.source_player_id)
        facedown = [c for c in own_cards if c.is_facedown]
        choices: list[RedeployChoice] = [RedeployChoice(card_to_return=None)]  # Decline
        for card in facedown:
            choices.append(RedeployChoice(card_to_return=card))
        return choices

    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        assert isinstance(choice, RedeployChoice)
        if choice.card_to_return is None:
            return  # Player declines
        bs = ctx.battle_state
        bs.return_card_to_hand(choice.card_to_return, ctx.source_player_id)
        bs.grant_extra_turn(ctx.source_player_id)
