from .random_color_hex import RandomColorHex

__version__="2.1"
__author__="Nathan Honn"
__email__="randomhexman@gmail.com"

__all__=["RandomColorHex", "main", "BasicMain", "Credits", "Help"]

def main(*, SuperLightColorsAllowed=True, SuperDarkColorsAllowed=True, HowDifferentShouldColorsBe='m'):
    return RandomColorHex().main(SuperLightColorsAllowed=SuperLightColorsAllowed, SuperDarkColorsAllowed=SuperDarkColorsAllowed, HowDifferentShouldColorsBe=HowDifferentShouldColorsBe)

def BasicMain(*, SuperLightColorsAllowed=True, SuperDarkColorsAllowed=True):
    return RandomColorHex().BasicMain(SuperLightColorsAllowed=SuperLightColorsAllowed, SuperDarkColorsAllowed=SuperDarkColorsAllowed)

def Credits():
    return RandomColorHex.Credits()

def Help():
    return RandomColorHex.Help()
