# usage

As you may know, Arkose Labs collects 3 types of data in `bio`:

- touch biometrics, _`tbio`_
- mouse biometrics, _`mbio`_
- and keyboard biometrics, _`kbio`_

Multiple event types can be used at once, eg. mouse and touch events can and are logged at the same time _(due to browser event listening functionality)_.

This library provides both generator functions for each biometric type, and a low level interface to generate your own [customized biometric data](#customization).

<br>

## location and the `LocationData` type

A big problem arose when writing this library, how would I generate the coordinates of important game components?

<img width="500" alt="Arkose Labs Funcaptcha challenge" src="https://github.com/user-attachments/assets/7d364ff1-d573-4833-b53b-0c61af0fa21a">

<br>

The answer is: **I don't, you do.** I provided a way for you to pass in location points, providing the level of personalization I initially wanted with this project.

<br>
<br>

```py
# https://github.com/unfuncaptcha/bio/tree/main/src/unfuncaptcha_bio/points.py
class LocationData(TypedDict):
    """Location data related to game type 4 components.

    Attributes:
        left_arrow (Tuple[int, int]): The x and y coordinates of the left arrow.
        right_arrow (Tuple[int, int]): The x and y coordinates of the right arrow.
        submit_button (Tuple[int, int]): The x and y coordinates of the submit button.
    """

    left_arrow: Tuple[int, int]
    right_arrow: Tuple[int, int]
    submit_button: Tuple[int, int]


example_loc: LocationData = {
    left_arrow: (x, y),
    right_arrow: (x, y),
    submit_button: (x, y)
}
```

You can then pass the location dictionary into your touch/mouse generation functions.

```py
TBioGenerator.generate(
    0,
    game_type = 4,
    location = {
        "right_arrow": (280, 113),
        "left_arrow": (40, 113),
        "submit_button": (175, 146),
    }
)
```
