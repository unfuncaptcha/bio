# bio

Generate mouse, touch, and keyboard motions for Arkose Labs Funcaptcha

```console
$ python -m pip install unfuncaptcha-bio
```

```py
from unfuncaptcha_bio import KBioGenerator, MBioGenerator, TBioGenerator


KBioGenerator.generate(
    2,                          # Answer index
    game_type = 3               # Game type defaults to 4
)
# eyJrYmlvIjoiMjQ4NCwxLDE7MzQ0M...


loc = {                          # Provide coordinates for each game type 4 component
    "right_arrow": (280, 113),
    "left_arrow": (40, 113),
    "submit_button": (175, 146),
}

MBioGenerator.generate(
    0,
    game_type      = 4,
    location       = loc,
    starting_point = (20, 20),    # Mouse starting point (only required for game type 4)
    start_offset   = 3000,        # Initial timestamp offset (in milliseconds)
    encode_base64  = False,       # Whether to base64 encode the bio JSON
)
# {"mbio":"3078,0,20,20;3097,0,25,21;3109

TBioGenerator.generate(
    0,
    location       = loc,
    encode_base64  = False,
    start_offset   = 3000,
)
# {"mbio":"3078,0,20,20;3097,0,25,21;3109
```

<br>
<br>

# table of contents

- [usage](https://github.com/unfuncaptcha/bio/blob/main/docs/usage.md) (_most of this library is self explanitory_)

  - [location data](https://github.com/unfuncaptcha/bio/blob/main/docs/usage.md#location-and-the-locationdata-type)

- [biometrics customization](https://github.com/unfuncaptcha/bio/blob/main/docs/customization.md)

  - [the `Event` class](https://github.com/unfuncaptcha/bio/blob/main/docs/customization.md#the-event-class)
  - [implementing a custom generator](https://github.com/unfuncaptcha/bio/blob/main/docs/customization.md#implementing-a-custom-generator)

- [reverse engineering](https://github.com/unfuncaptcha/bio/blob/main/docs/reversing.md)
