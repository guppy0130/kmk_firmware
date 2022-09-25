import supervisor

from kb import KMKKeyboard

from kmk.extensions.peg_oled_display import (
    Oled,
    OledDisplayMode,
    OledReactionType,
    OledData,
)
from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.handlers.sequences import send_string
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.split import Split, SplitType

keyboard = KMKKeyboard()
modtap = ModTap()
layers_ext = Layers()
keyboard.modules.append(layers_ext)
keyboard.modules.append(modtap)

# oled
oled_ext = Oled(
    OledData(
        corner_one={0: OledReactionType.STATIC, 1: ["LAYER: "]},
        corner_two={0: OledReactionType.LAYER, 1: ["1", "2", "3", "4"]},
        corner_three={
            0: OledReactionType.LAYER,
            1: ["DEFAULT", "LOWER", "RAISE", "ADJUST"],
        },
        corner_four={
            0: OledReactionType.LAYER,
            1: ["QWERTY", "NUMS", "MEDIA", "LEDS/DIR"],
        },
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=False,
)
keyboard.extensions.append(oled_ext)

# ledmap
rgb_red = [255, 0, 0]
rgb_orange = [255, 157, 0]
rgb_yellow = [255, 225, 0]
rgb_green = [0, 255, 0]
rgb_blue = [0, 0, 255]
rgb_purple = [255, 0, 255]
rgb_black = [0, 0, 0]
# fmt: off
rgb_ext = Rgb_matrix(
    ledDisplay=[
        rgb_red, rgb_red, rgb_orange, rgb_orange, rgb_yellow, rgb_yellow,                       rgb_green, rgb_green, rgb_blue, rgb_blue, rgb_purple, rgb_purple,
        rgb_red, rgb_red, rgb_orange, rgb_orange, rgb_yellow, rgb_yellow,                       rgb_green, rgb_green, rgb_blue, rgb_blue, rgb_purple, rgb_purple,
        rgb_red, rgb_red, rgb_orange, rgb_orange, rgb_yellow, rgb_yellow,                       rgb_green, rgb_green, rgb_blue, rgb_blue, rgb_purple, rgb_purple,
        rgb_red, rgb_red, rgb_orange, rgb_orange, rgb_yellow, rgb_yellow, rgb_black, rgb_black, rgb_green, rgb_green, rgb_blue, rgb_blue, rgb_purple, rgb_purple,  # row 4 + encoder
                                      rgb_orange, rgb_orange, rgb_yellow, rgb_black, rgb_black, rgb_green, rgb_green, rgb_blue                                  ,  # thumb cluster
        rgb_red,          rgb_orange,             rgb_yellow,                                              rgb_green,           rgb_blue,             rgb_purple,  # underglow top
        rgb_red,          rgb_orange,             rgb_yellow,                                              rgb_green,           rgb_blue,             rgb_purple,  # underglow bottom
    ],
    split=True,
    rightSide=False,
    disable_auto_write=True
)
# fmt: on
keyboard.extensions.append(rgb_ext)

split = Split(data_pin=keyboard.rx, data_pin2=keyboard.tx, uart_flip=False)
keyboard.modules.append(split)

# fmt: off
LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.MO(3)
XXXXXXX = KC.NO
TABSHFT = KC.MT(KC.TAB, KC.LSFT)

keyboard.keymap = [
    # DEFAULT
    [
        KC.ESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                     KC.N6,  KC.N7,   KC.N8,    KC.N9,   KC.N0,    KC.BSPC,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                      KC.Y,   KC.U,    KC.I,     KC.O,    KC.P,     KC.BSPC,
        TABSHFT, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                      KC.H,   KC.J,    KC.K,     KC.L,    KC.SCLN,  KC.QUOT,
        KC.LCTL, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,   KC.LBRC,  KC.RBRC, KC.N,   KC.M,    KC.COMMA, KC.DOT,  KC.SLSH,  KC.ENT,
                                   KC.LGUI, KC.LGUI, KC.GRV, LOWER,    RAISE,   KC.SPC, KC.RALT, KC.RALT,
        # Encoders
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
    # LOWER
    [
        KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,                     KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,
        KC.ESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                     KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        KC.LSFT, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                     KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
        KC.LCTL, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.TRNS, KC.TRNS, KC.F12,  KC.HOME, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
                                   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, ADJUST,  KC.SPC,  KC.END,  KC.END,
        # Encoders
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
    # RAISE
    [
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                   XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                   XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                   KC.MPRV, KC.VOLD, KC.VOLU, KC.MNXT, KC.MPLY, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
                                   KC.TRNS, KC.TRNS, KC.TRNS, ADJUST,  KC.TRNS, KC.SPC,  KC.END,  KC.END,
        # Encoders
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
    # ADJUST
    [
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.RGB_TOG,                XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.RGB_BRI,                XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.RGB_BRD,                KC.LEFT, KC.DOWN, KC.UP  , KC.RGHT, KC.NO,   XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
                                   XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        # Encoders
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_NEXT_TRACK,
    ],
]
# fmt: on

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
