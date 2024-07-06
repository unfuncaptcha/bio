# bio

Generate mouse, touch, and keyboard motions for Arkose Labs Funcaptcha

```py
>>> from unfuncaptcha_bio.kbio import KBioGenerator

>>> KBioGenerator.generate(1) # Answer index 1, game type 4 (match-key)
'4622,1,1;5229,0,0;6167,1,0;6897,0,0;7122,1,0;8089,0,1;8304,1,1;9158,0,0;10012,1,0;10489,0,1;10897,1,1;'
>>> KBioGenerator.generate(2, game_type = 3) # Answer index 2, game type 3 (tiles)
'4060,1,1;4321,0,1;4763,1,1;5714,0,1;6079,1,1;7068,0,1;7530,1,1;8368,0,1;8743,1,1;'
```

## reverse engineering

When submitting a FunCaptcha answer, there may be a `bio` component in your request. This component represents telemetry mouse, keyboard, **or** touch data.

The biometric data is represented as a base64 encoded JSON string following this format:

```json
{
  // mouse motions collection when using your mouse
  "mbio": "9298,0,369,216;9331,0,378,216; ...",

  // touch motions collected when using the Funcaptcha Mobile SDK
  "tbio": "",

  // keyboard motions collected when using keyboard navigation
  "kbio": "2013,1,1;2918,0,0; ..."
}
```

<br>

Below is the deobfuscated function used for packaging the biometric data, as well as some more information about the variables in use:

```js
{
    key: "getBiometricsData",
    value: function() {
        return window.btoa(JSON.stringify({
            mbio: this.mouseEvents.map(function(LR) {
                return `${LR.timestamp},${LR.type},${LR.x},${LR.y};`;
            }).join(""),
            tbio: this.touchEvents.map(function(LR) {
                return `${LR.timestamp},${LR.type},${LR.x},${LR.y};`;
            }).join(""),
            kbio: this.keyPressEvents.map(function(LR) {
                return `${LR.timestamp},${LR.type},${LR.code};`;
            }).join("")
        }));
    }
}
```

| Variable       | Description                                                                          |
| -------------- | ------------------------------------------------------------------------------------ |
| `LR.timestamp` | Time that motion was recorded subtracted by time that motions started to be recorded |
| `LR.x`, `LR.y` | X and Y coordinates of a touch or mouse location                                     |
| `LR.type`      | Type of motion. Up, Down, Move, etc. _see below_                                     |
| `LR.code`      | KBio only, the key that was pressed. _see below_                                     |

> <details>
>
> <summary>See more on <code>LR.type</code></summary>
>
> ```js
> // LN.[MOTION] = respective number used in bio
>
> // X3 is used in mbio
> var X3 = (function (LN) {
>   LN[(LN.Move = 0)] = "Move";
>   LN[(LN.Down = 1)] = "Down";
>   LN[(LN.Up = 2)] = "Up";
>   return LN;
> })(X3 || {});
>
> // X4 is used in tbio
> var X4 = (function (LN) {
>   LN[(LN.Start = 0)] = "Start";
>   LN[(LN.End = 1)] = "End";
>   LN[(LN.Move = 2)] = "Move";
>   LN[(LN.Cancel = 99)] = "Cancel";
>   return LN;
> })(X4 || {});
>
> // X5 is used in kbio
> var X5 = (function (LN) {
>   LN[(LN.Down = 0)] = "Down";
>   LN[(LN.Up = 1)] = "Up";
>   return LN;
> })(X5 || {});
> ```
>
> </details>

<br>

> <details>
>
> <summary>See more on <code>LR.code</code></summary>
>
> ```js
> {
>     Tab: 0,
>     Enter: 1,
>     Space: 3,
>     ShiftLeft: 4,
>     ShiftRight: 5,
>     ControlLeft: 6,
>     ControlRight: 7,
>     MetaLeft: 8,
>     MetaRight: 9,
>     AltLeft: 10,
>     AltRight: 11,
>     Backspace: 12,
>     Escape: 13,
> } [LW.code] ?? 14 // 14 represents unsupported keys
> ```
>
> </details>
