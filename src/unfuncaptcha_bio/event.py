from typing import TypedDict, List, Dict, Union, ClassVar
from abc import ABC, abstractmethod
from functools import reduce
from base64 import b64encode
from random import randint
from json import dumps


class Event(ABC):
    CODEMAP: ClassVar[Dict[str, int]]
    CATEGORY: ClassVar[str]

    class TranscodingAccumulator(TypedDict):
        bio: str
        time_elapsed_ms: int

    @staticmethod
    def encode_events(
        events: List["SubEvent"],
        start_offset: Union[int, None] = None,
        encode_base64: bool = True,
    ) -> str:
        """Encodes the list of KeyEvent instances into Arkose Labs' bio string representation.

        Args:
            events (List['SubEvent']): List of SubEvent instances
            start_offset (int, optional): Initial timestamp offset. Defaults to a random value between 1000 and 4000
            encode_base64 (bool, optional): Encode the output as base64. Defaults to True

        Returns:
            str: Encoded string of keyboard events

        """

        def transcoding_reducer(acc: Dict[str, Union[str, int]], curr: SubEvent):
            time_elapsed_ms = acc["time_elapsed_ms"] + curr["since_previous_ms"]
            event_category = curr["event"].CATEGORY

            acc[event_category] = acc.setdefault(event_category, "") + curr[
                "event"
            ].__format__(time_elapsed_ms)
            acc["time_elapsed_ms"] = time_elapsed_ms

            return acc

        reduced_events = reduce(
            transcoding_reducer,
            events,
            {
                "time_elapsed_ms": (
                    start_offset if start_offset is not None else randint(1000, 4000)
                )
            },
        )
        reduced_events.pop("time_elapsed_ms")

        packed_bio = dumps(
            {
                **reduced_events,
                **{
                    key: reduced_events.get(key, "") for key in ["tbio", "mbio", "kbio"]
                },
            },
            separators=(",", ":"),
        )

        return (
            packed_bio if not encode_base64 else b64encode(packed_bio.encode()).decode()
        )

    @abstractmethod
    def __format__(self, time_elapsed_ms: int) -> str:
        pass


class SubEvent(TypedDict):
    event: Event
    since_previous_ms: int  # time elapsed since previous event
