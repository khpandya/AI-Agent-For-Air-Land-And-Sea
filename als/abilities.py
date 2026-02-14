"""Abstract base for tactical abilities and the context they operate in."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from als.enums import AbilityTiming

if TYPE_CHECKING:
    from als.card_instance import CardInstance
    from als.game_state import BattleState


@dataclass
class AbilityContext:
    """Data passed to an ability during resolution."""

    battle_state: BattleState
    source_card: CardInstance
    source_player_id: int
    opponent_player_id: int


class TacticalAbility(ABC):
    """Base class for all tactical abilities."""

    def __init__(self, timing: AbilityTiming, is_optional: bool = False) -> None:
        self.timing = timing
        self.is_optional = is_optional

    @abstractmethod
    def is_possible(self, ctx: AbilityContext) -> bool:
        """Whether this ability can be executed in the current state.

        If impossible and mandatory, the ability is simply ignored per rules.
        """

    @abstractmethod
    def get_choices(self, ctx: AbilityContext) -> list[Any]:
        """Return valid options the player can choose from.

        For abilities with no choice, returns a single-element list.
        For ongoing abilities that don't use execute(), returns [].
        """

    @abstractmethod
    def execute(self, ctx: AbilityContext, choice: Any) -> None:
        """Apply the ability's effect, mutating game state."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.timing.name})"
