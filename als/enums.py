"""Enumerations for all Air, Land, and Sea game concepts."""

from enum import Enum, auto


class TheaterType(Enum):
    AIR = auto()
    LAND = auto()
    SEA = auto()


class CardOrientation(Enum):
    FACEUP = auto()
    FACEDOWN = auto()


class AbilityTiming(Enum):
    INSTANT = auto()
    ONGOING = auto()


class PlayerPosition(Enum):
    """1st player wins ties and empty theaters."""
    FIRST = auto()
    SECOND = auto()


class TurnAction(Enum):
    DEPLOY = auto()
    IMPROVISE = auto()
    WITHDRAW = auto()


class BattleEndReason(Enum):
    ALL_CARDS_PLAYED = auto()
    WITHDRAWAL = auto()


class GamePhase(Enum):
    SETUP = auto()
    BATTLE_IN_PROGRESS = auto()
    BATTLE_SCORING = auto()
    GAME_OVER = auto()


class BattlePhase(Enum):
    DEALING = auto()
    PLAYER_TURN = auto()
    ABILITY_RESOLUTION = auto()
    BATTLE_END = auto()


class CardZone(Enum):
    HAND = auto()
    BATTLEFIELD = auto()
    DECK = auto()
