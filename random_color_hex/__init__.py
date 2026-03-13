from .random_color_hex import RandomColorHex

__version__="3.0.1"
__author__="Nathan Honn"
__email__="randomhexman@gmail.com"

__all__=["RandomColorHex", "main", "basic_main", "credits", "help", "truth"]

def main(*, super_light_colors_allowed=True, super_dark_colors_allowed=True, how_different_should_colors_be='m',kL=1.0, kC=1.0, kH=1.0):
    return RandomColorHex().main(super_light_colors_allowed=super_light_colors_allowed, super_dark_colors_allowed=super_dark_colors_allowed, how_different_should_colors_be=how_different_should_colors_be,kL=kL, kC=kC, kH=kH)

def basic_main(*, super_light_colors_allowed=True, super_dark_colors_allowed=True):
    return RandomColorHex().basic_main(super_light_colors_allowed=super_light_colors_allowed, super_dark_colors_allowed=super_dark_colors_allowed)

def credits():
    return RandomColorHex().credits()

def help():
    return RandomColorHex().help()

def truth():
    return RandomColorHex().john_3_verse_16()

def jupyter_reset():
    """Must call manually if you're in a Jupyter notebook."""
    return RandomColorHex()._reset()