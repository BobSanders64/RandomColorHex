from .random_color_hex import RandomColorHex

__version__="2.1.6"
__author__="Nathan Honn"
__email__="randomhexman@gmail.com"

__all__=["RandomColorHex", "main", "BasicMain", "Credits", "Help"]

def main(*, SuperLightColorsAllowed=True, SuperDarkColorsAllowed=True, HowDifferentShouldColorsBe='m'):
    return RandomColorHex().main(SuperLightColorsAllowed=SuperLightColorsAllowed, SuperDarkColorsAllowed=SuperDarkColorsAllowed, HowDifferentShouldColorsBe=HowDifferentShouldColorsBe)

def BasicMain(*, SuperLightColorsAllowed=True, SuperDarkColorsAllowed=True):
    return RandomColorHex().BasicMain(SuperLightColorsAllowed=SuperLightColorsAllowed, SuperDarkColorsAllowed=SuperDarkColorsAllowed)

def Credits():
    """Return package credits/about string."""
    return RandomColorHex().Credits()

def Help():
    """Return help/usage string."""
    return RandomColorHex().Help()

def JupyterReset():
    """Manual call, must use if your in Jupyter notebook"""
    return RandomColorHex()._reset()
