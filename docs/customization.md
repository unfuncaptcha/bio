# biometrics customization

The generation functions provided may not suffice for your use, so you may want to implement your own generator or override current generator functions.

<br>

## the `Event` class and `SubEvent` type

The `Event` class is an abstract base class used to represent a single event of any type. This class includes an important function, the `encode_events` function, which is used to encode a list of `SubEvents` into Arkose Labs' bio string representation.

<br>

### the `Event` Class

The `Event` class includes the following:

- **CODEMAP**: A class variable dictionary mapping string keys to integer values.
- **CATEGORY**: A class variable string representing the event type/category (`tbio`, `mbio`, `kbio`).

<br>

```python
class SubEvent(TypedDict):
    event: Event
    since_previous_ms: int  # time elapsed since previous event


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
        ...

    @abstractmethod
    def __format__(self, time_elapsed_ms: int) -> str:
        pass
```

You use the `SubEvent` type to pass the encoder function both an event, and the time elapsed since the previous event, in milliseconds.

### implementing a custom generator

The generators have been written in a way where you can override the game type generator functions, allowing you to write your own generation algorithms.

<br>

> [!NOTE]  
> **These function signatures stay the same!**
> <br>
> <br> Troughout each generator, these function signatures always take in/return the same types as shown here.
> <br> The only exception to this rule is `KBioGenerator._gametype_4_gen`, which does **not** require a `location` argument

```py
from unfuncaptcha_bio.points import LocationData
from unfuncaptcha_bio import TBioGenerator
from unfuncaptcha_bio.event import SubEvent
from typing import List


class TBioGenOverride(TBioGenerator):
    """Overrides the game type 3 method to use a custom generator function."""

    @staticmethod
    def _gametype_3_gen(answer_index: int) -> List[SubEvent]:
        return [...]

    @staticmethod
    def _gametype_4_gen(
        answer_index: int, location: Union[LocationData, None]
    ) -> List[SubEvent]:
        return [...]


if __name__ == "__main__":
    answer_index: int = 2
    print(
        TBioGenOverride().generate(
            answer_index,
            3,
            {...},
        )
    )

```
