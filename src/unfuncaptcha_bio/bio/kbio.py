from typing import Dict, List, Union
from ..event import Event, SubEvent
from random import randint
import itertools


class KeyEvent(Event):
    """
    Represents a keyboard event with a key code and keyboard event type.

    Attributes:
        CODEMAP (Dict[str, int]): Mapping of key names to their respective codes.
        TYPEMAP (Dict[str, int]): Mapping of event types ("Down" or "Up") to their respective codes.

        key (str): The key that was pressed.
        event_type (str): The type of motion ("Down" or "Up").
    """

    CATEGORY = "kbio"
    CODEMAP = {
        "Tab": 0,
        "Enter": 1,
        "Space": 3,
        "ShiftLeft": 4,
        "ShiftRight": 5,
        "ControlLeft": 6,
        "ControlRight": 7,
        "MetaLeft": 8,
        "MetaRight": 9,
        "AltLeft": 10,
        "AltRight": 11,
        "Backspace": 12,
        "Escape": 13,
    }
    TYPEMAP = {"Down": 0, "Up": 1}

    def __init__(self, key: str, event_type: str):
        self.key = key
        self.event_type = event_type

    def __format__(self, format_spec: int):
        return f"{format_spec},{KeyEvent.TYPEMAP[self.event_type]},{KeyEvent.CODEMAP.get(self.key, 14)};"  # 14 represents unsupported keypresses

    @staticmethod
    def generate_full_key_press(key: str):
        """Generates a full key press sequence (key down and key up) for a given key."""

        return [KeyEvent(key, "Down"), KeyEvent(key, "Up")]


class KBioGenerator(object):
    """Generates "kbio" for different game types."""

    def generate(
        answer_index: int,
        game_type: int = 4,
        start_offset: Union[int, None] = None,
        encode_base64: bool = True,
    ) -> str:
        """Generates keyboard events for the given game type and answer index.

        Args:
            answer_index (int): Index of the chosen answer
            game_type (int, optional): Challenges game type. 3 for Tiles, 4 for MatchKey. Defaults to 4.
            start_offset (Union[int, None], optional): Initial timestamp offset. Defaults to a random value between 1000 and 4000.
            encode_base64 (bool, optional): Whether to base64 encode the bio JSON. Defaults to False.

        Returns:
            str: Encoded string of keyboard events
        """

        game_generators: Dict[int, List[KeyEvent]] = {
            4: lambda: KBioGenerator._gametype_4_gen(answer_index),
            3: lambda: KBioGenerator._gametype_3_gen(answer_index),
        }

        return KeyEvent.encode_events(
            game_generators[game_type](),
            start_offset,
            encode_base64,
        )

    @staticmethod
    def _gametype_3_gen(answer_index: int) -> List[SubEvent]:
        return list(
            map(
                lambda event: {"event": event, "since_previous_ms": randint(200, 1000)},
                [
                    KeyEvent("Enter", "Up"),
                    *itertools.chain.from_iterable(
                        KeyEvent.generate_full_key_press("Enter")
                        for _ in range(answer_index + 1)
                    ),
                    *KeyEvent.generate_full_key_press("Enter"),
                ],
            )
        )

    @staticmethod
    def _gametype_4_gen(answer_index: int) -> List[SubEvent]:
        return list(
            map(
                lambda event: {"event": event, "since_previous_ms": randint(200, 1000)},
                [
                    KeyEvent(
                        "Enter", "Up"
                    ),  # "Up" Enter event (The initial "Down" on ENTER triggers the listener so it's not logged)
                    *itertools.chain.from_iterable(
                        KeyEvent.generate_full_key_press("Tab") for _ in range(2)
                    ),  # Selects "Game Type 4" Arrows
                    *itertools.chain.from_iterable(
                        KeyEvent.generate_full_key_press("Enter")
                        for _ in range(answer_index)
                    ),  # Generates answer index selection
                    *KeyEvent.generate_full_key_press("Tab"),  # Selects submit button
                    *KeyEvent.generate_full_key_press("Enter"),  # Submits
                ],
            )
        )
