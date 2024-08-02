from ..points import Points, LocationData, tile_to_location
from typing import Tuple, List, Dict, Union
from ..event import Event, SubEvent
from .mbio import MouseEvent
from random import randint
import itertools


class TouchEvent(Event):
    """
    Represents a mobile touch event with a opcode and coordinates.

    Attributes:
        CODEMAP (Dict[str, int]): Mapping of operation names to their respective codes.

        type (str): The mouse event type: "Start", "End", "Move", or "Cancel".
        x (int): The x-coordinate of the touch event.
        y (int): The y-coordinate of the touch event.
    """

    CATEGORY = "tbio"
    CODEMAP = {"Start": 0, "End": 1, "Move": 2, "Cancel": 99}

    def __init__(self, event_type: str, coordinates: Tuple[int, int] = (0, 0)):
        self.type = event_type
        self.x, self.y = coordinates

    def __format__(self, format_spec: int):
        return f"{format_spec},{self.CODEMAP[self.type]},{self.x},{self.y};"

    @staticmethod
    def generate_touch_event(coordinates: Tuple[int, int]) -> List[SubEvent]:
        """Generates a touch/mouse events for the given coordinates."""
        return [
            {
                "event": TouchEvent("Start", coordinates),
                "since_previous_ms": randint(100, 400),
            },
            *[
                {
                    "event": MouseEvent(motion, coordinates),
                    "since_previous_ms": randint(0, 1),
                }
                for motion in [
                    "Move",
                    "Down",
                    "Up",
                ]  # Each "mouse" motion occurs between 0-1 ms of eachother
            ],
        ]


class TBioGenerator(object):
    """Generates "tbio" for different game types."""

    @classmethod
    def generate(
        cls,
        answer_index: int,
        game_type: int = 4,
        location: Union[LocationData, None] = None,
        start_offset: Union[int, None] = None,
        encode_base64: bool = True,
    ) -> str:
        """Generates touch/mouse events for the given game type and answer index.

        Args:
            answer_index (int): Index of the chosen answer
            game_type (int, optional): Challenges game type. 3 for Tiles, 4 for MatchKey. Defaults to 4.
            location (LocationData, optional): Location data for the game, required for game type 4.
            start_offset (Union[int, None], optional): Initial timestamp offset. Defaults to a random value between 1000 and 4000.
            encode_base64 (bool, optional): Whether to base64 encode the bio JSON. Defaults to False.

        Returns:
            str: Encoded string of keyboard events
        """

        game_generators = {
            3: lambda: cls._gametype_3_gen(answer_index),
            4: lambda: cls._gametype_4_gen(answer_index, location),
        }

        return TouchEvent.encode_events(
            game_generators[game_type](), start_offset, encode_base64
        )

    @staticmethod
    def _gametype_3_gen(answer_index: int) -> List[SubEvent]:
        return TouchEvent.generate_touch_event(tile_to_location(answer_index))

    @staticmethod
    def _gametype_4_gen(
        answer_index: int, location: Union[LocationData, None]
    ) -> List[SubEvent]:
        if not location:
            raise ValueError("Location data is required for game type 4")

        return [
            *itertools.chain.from_iterable(
                TouchEvent.generate_touch_event(
                    Points(*location["right_arrow"]).generate_point_around(36)
                )
                for _ in range(answer_index)
            ),
            *TouchEvent.generate_touch_event(
                Points(*location["submit_button"]).generate_point_around(28)
            ),
        ]
