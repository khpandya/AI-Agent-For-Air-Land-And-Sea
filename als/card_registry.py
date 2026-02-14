"""Factory for all 18 CardDefinition objects."""

from __future__ import annotations

from als.abilities_impl import (
    AerodromeAbility,
    AirDropAbility,
    AmbushAbility,
    BlockadeAbility,
    ContainmentAbility,
    CoverFireAbility,
    DisruptAbility,
    EscalationAbility,
    ManeuverAbility,
    RedeployAbility,
    ReinforceAbility,
    SupportAbility,
    TransportAbility,
)
from als.card_definition import CardDefinition
from als.enums import AbilityTiming, TheaterType


def create_all_card_definitions() -> list[CardDefinition]:
    """Create and return all 18 CardDefinition objects for Air, Land, and Sea."""
    return [
        # --- AIR cards ---
        CardDefinition(
            card_id=0, name="Support", theater_type=TheaterType.AIR,
            printed_strength=1, ability_timing=AbilityTiming.ONGOING,
            ability=SupportAbility(),
        ),
        CardDefinition(
            card_id=1, name="Air Drop", theater_type=TheaterType.AIR,
            printed_strength=2, ability_timing=AbilityTiming.INSTANT,
            ability=AirDropAbility(),
        ),
        CardDefinition(
            card_id=2, name="Maneuver", theater_type=TheaterType.AIR,
            printed_strength=3, ability_timing=AbilityTiming.INSTANT,
            ability=ManeuverAbility(),
        ),
        CardDefinition(
            card_id=3, name="Aerodrome", theater_type=TheaterType.AIR,
            printed_strength=4, ability_timing=AbilityTiming.ONGOING,
            ability=AerodromeAbility(),
        ),
        CardDefinition(
            card_id=4, name="Containment", theater_type=TheaterType.AIR,
            printed_strength=5, ability_timing=AbilityTiming.ONGOING,
            ability=ContainmentAbility(),
        ),
        CardDefinition(
            card_id=5, name="", theater_type=TheaterType.AIR,
            printed_strength=6,
        ),
        # --- LAND cards ---
        CardDefinition(
            card_id=6, name="Reinforce", theater_type=TheaterType.LAND,
            printed_strength=1, ability_timing=AbilityTiming.INSTANT,
            ability=ReinforceAbility(),
        ),
        CardDefinition(
            card_id=7, name="Ambush", theater_type=TheaterType.LAND,
            printed_strength=2, ability_timing=AbilityTiming.INSTANT,
            ability=AmbushAbility(),
        ),
        CardDefinition(
            card_id=8, name="Maneuver", theater_type=TheaterType.LAND,
            printed_strength=3, ability_timing=AbilityTiming.INSTANT,
            ability=ManeuverAbility(),
        ),
        CardDefinition(
            card_id=9, name="Cover Fire", theater_type=TheaterType.LAND,
            printed_strength=4, ability_timing=AbilityTiming.ONGOING,
            ability=CoverFireAbility(),
        ),
        CardDefinition(
            card_id=10, name="Disrupt", theater_type=TheaterType.LAND,
            printed_strength=5, ability_timing=AbilityTiming.INSTANT,
            ability=DisruptAbility(),
        ),
        CardDefinition(
            card_id=11, name="", theater_type=TheaterType.LAND,
            printed_strength=6,
        ),
        # --- SEA cards ---
        CardDefinition(
            card_id=12, name="Transport", theater_type=TheaterType.SEA,
            printed_strength=1, ability_timing=AbilityTiming.INSTANT,
            ability=TransportAbility(),
        ),
        CardDefinition(
            card_id=13, name="Escalation", theater_type=TheaterType.SEA,
            printed_strength=2, ability_timing=AbilityTiming.ONGOING,
            ability=EscalationAbility(),
        ),
        CardDefinition(
            card_id=14, name="Maneuver", theater_type=TheaterType.SEA,
            printed_strength=3, ability_timing=AbilityTiming.INSTANT,
            ability=ManeuverAbility(),
        ),
        CardDefinition(
            card_id=15, name="Redeploy", theater_type=TheaterType.SEA,
            printed_strength=4, ability_timing=AbilityTiming.INSTANT,
            ability=RedeployAbility(),
        ),
        CardDefinition(
            card_id=16, name="Blockade", theater_type=TheaterType.SEA,
            printed_strength=5, ability_timing=AbilityTiming.ONGOING,
            ability=BlockadeAbility(),
        ),
        CardDefinition(
            card_id=17, name="", theater_type=TheaterType.SEA,
            printed_strength=6,
        ),
    ]
