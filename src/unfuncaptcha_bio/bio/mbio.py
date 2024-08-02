from ..points import Points, LocationData, tile_to_location
from typing import Tuple, List, Dict, Union
from ..event import Event, SubEvent
from random import randint
from typing import Tuple


class MouseEvent(Event):
    """
    Represents a keyboard event with a key code and keyboard event type.

    Attributes:
        CODEMAP (Dict[str, int]): Mapping of key names to their respective codes.
        TYPEMAP (Dict[str, int]): Mapping of event types ("Down" or "Up") to their respective codes.

        type (str): The mouse event type: "Up", "Down", or "Move".
        x (int): The x-coordinate of the mouse event.
        y (int): The y-coordinate of the mouse event.
    """

    CATEGORY = "mbio"
    CODEMAP = {"Move": 0, "Down": 1, "Up": 2}

    def __init__(self, event_type: str, coordinates: Tuple[int, int] = (0, 0)):
        self.type = event_type
        self.x, self.y = coordinates

    def __format__(self, format_spec: int):
        return f"{format_spec},{self.CODEMAP[self.type]},{self.x},{self.y};"

    @staticmethod
    def generate_mouse_click_event(coordinates: Tuple[int, int]) -> List[SubEvent]:
        return [
            {
                "event": MouseEvent("Up", coordinates),
                "since_previous_ms": 0,
            },
            {
                "event": MouseEvent("Up", coordinates),
                "since_previous_ms": randint(0, 10),
            },
        ]


class MBioGenerator(object):
    """Generates "mbio" for different game types."""

    def generate(
        answer_index: int,
        game_type: int = 4,
        location: Union[LocationData, None] = None,
        starting_point: Tuple[int, int] = (randint(0, 300), randint(0, 250)),
        start_offset: Union[int, None] = None,
        encode_base64: bool = True,
    ) -> str:
        """Generates mouse events for the given game type and answer index.

        Args:
            answer_index (int): Index of the chosen answer
            game_type (int, optional): Challenges game type. 3 for Tiles, 4 for MatchKey. Defaults to 4.
            location (LocationData): Location data for the game
            start_offset (Union[int, None], optional): Initial timestamp offset. Defaults to a random value between 1000 and 4000.
            starting_point (Tuple[int, int], optional): Starting point for the events. Defaults to (randint(0, 300), randint(0, 250)).
            encode_base64 (bool, optional): Whether to base64 encode the bio JSON. Defaults to False.

        Returns:
            str: Encoded string of keyboard events
        """

        location = {  # Override/Adjust the coordinates to be somewhat random
            "left_arrow": Points(*location["left_arrow"]).generate_point_around(36),
            "right_arrow": Points(*location["right_arrow"]).generate_point_around(36),
            "submit_button": Points(*location["submit_button"]).generate_point_around(
                28
            ),
        }
        game_generators: Dict[int, List[SubEvent]] = {
            3: lambda: MBioGenerator._gametype_3_gen(
                answer_index, starting_point, location
            ),
            4: lambda: MBioGenerator._gametype_4_gen(
                answer_index, starting_point, location
            ),
        }

        return MouseEvent.encode_events(
            game_generators[game_type]()[
                :150
            ],  # Arkose Labs records a maximum of 150 events
            start_offset,
            encode_base64,
        )

    @staticmethod
    def _gametype_3_gen(
        answer_index: int, starting_point: Tuple[int, int], location: LocationData
    ) -> List[SubEvent]:
        tile_coordinate = tile_to_location(answer_index)

        return [
            *[
                {
                    "event": MouseEvent("Move", coord),
                    "since_previous_ms": randint(10, 20),
                }
                for coord in Points.generate_bezier_path(
                    [starting_point, tile_coordinate],
                    20,
                    1.5,
                )
            ],
            *MouseEvent.generate_mouse_click_event(tile_coordinate),
        ]

    @staticmethod
    def _gametype_4_gen(
        answer_index: int,
        starting_point: Tuple[int, int],
        location: Union[LocationData, None],
    ) -> List[SubEvent]:
        if not location:
            raise ValueError("Location data is required for game type 4")

        return [
            *[
                {
                    "event": MouseEvent("Move", coord),
                    "since_previous_ms": randint(10, 20),
                }
                for coord in Points.generate_bezier_path(
                    [starting_point, location["right_arrow"]], 20, 1.5
                )
            ],
            *[
                MouseEvent.generate_mouse_click_event(location["right_arrow"])
                for _ in range(answer_index)
            ],
            *[
                {
                    "event": MouseEvent("Move", coord),
                    "since_previous_ms": randint(10, 20),
                }
                for coord in Points.generate_bezier_path(
                    [location["right_arrow"], location["submit_button"]],
                    20,
                    1.5,
                )
            ],
            *MouseEvent.generate_mouse_click_event(location["submit_button"]),
        ]
