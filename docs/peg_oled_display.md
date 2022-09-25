# Peg Oled Display

To use this you need to make some changes to `kb.py` and `main.py`.

## What you can and can't do

### Can do

* Display images
* Display text
* Set images or text to react to your layer

### Can't do yet/on the way

* React to battery percentage
* React to WPM

## Required Libs

You need these frozen into your circuitpython or in a `lib` folder at the root
of your drive.

* [Adafruit_CircuitPython_DisplayIO_SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SSD1306)
* [Adafruit_CircuitPython_Display_Text](https://github.com/adafruit/Adafruit_CircuitPython_Display_Text)
* [Download .mpy versions from here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20220415/adafruit-circuitpython-bundle-7.x-mpy-20220415.zip)

## `kb.py`

Your chosen board may already have these changes done; if not, you will need to
add them.

You need to add SCL and SDA to your keyboard. The pins the OLED are connected to
on your controller may not be called "SCL" and "SDA"; they could be "GP21" and
"GP13," for example. The best way to find out what they are is look at the
board's pinout.

```python
SCL=board.SCL
SDA=board.SDA
```

## `main.py`

These are the changes that need to be made/added to your `main.py`.

### Config

No matter how you are going to use the OLED you need this part:

```python
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledDisplayMode,
    OledReactionType,
    OledData,
)
keyboard = KMKKeyboard()
# ... Other oled code
keyboard.extensions.append(oled_ext) 
```

### Photos

#### Preparing the images

You need to include all the images in your circuitpython drive at the root,
alongside `main.py`.

Your images need to be 128x32px and should only be black and white. After you
have made your image you can save as a "monochrome bmp"; this will save you a
lot of space.
So the config for photos is quite simple.

#### Config

Oled takes 2-3 arguments:

1. `OledData`
    * `OledData` can take image **or** `corner_one`, `corner_two`,
      `corner_three`, and `corner_four`
    * Every item in `OledData` has 2 fields:
      * `0`: This is the reaction type; it has values:
        * `OledReactionType.LAYER`
        * `OledReactionType.STATIC`
      * `1`: An array of the items you want to show for the reaction. In the
        following example, 4 images to switch on the 4 layers
2. `toDisplay=OledDisplayMode.TXT` this takes a OledDisplayMode `TXT` or `IMG`.
    * This tells the extension to load images or text.
3. `flip=Boolean` will simply flip your display.

```python
oled_ext = Oled(
    OledData(
        image={
            0: OledReactionType.LAYER,
            1: ["1.bmp","2.bmp","1.bmp","2.bmp"]}
    ),
    toDisplay=OledDisplayMode.IMG,
    flip=False
)
```

In this code example we are saying to react to the layer change and load a image
filed named `1.bmp` for layer one, `2.bmp` for layer two, and so on.

### Text

#### Config

Set the following:

* `toDisplay=OledDisplayMode.TXT`
* configure corners

The corners 1, 2, 3, 4 correspond to the following:

1. Top left
2. Top right
3. Bottom left
4. Bottom right

After that is the same as the previous example. Each one has two fields:

* `0`: the reaction type
* `1`: what to display

In the following example, we will always display the word "layer" in the top
left corner of the screen, and then the other 3 corners will change depending on
the layer.

```python
oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2","3","4"]},
        corner_three={0:OledReactionType.LAYER,1:["base","raise","lower","adjust"]},
        corner_four={0:OledReactionType.LAYER,1:["qwerty","nums","shifted","leds"]}
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=False
)
```

### Note

Your OLED data can be a variable as shown below with images.

```python
oled_display_data=OledData(image={0:OledReactionType.LAYER,1:["1.bmp","2.bmp","1.bmp","2.bmp"]})

oled_ext = Oled(oled_display_data,toDisplay=OledDisplayMode.IMG,flip=False)
```

### Text example

![example](https://boardsource.imgix.net/a4f155e0-bc83-11ec-a4ed-79d542ba3127.gif)
