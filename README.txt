# random_color_hex

A random color generator that produces visually distinct colors, unlike most libraries that rely on arbitrary gradient RGB separation.

This library is special in that it uses Gaurav Sharma's 2001 paper CIEDE2000 to calculate the distance between colors actually ***looks*** different instead of just being mathmatically different. Many versions of RGB generators do the latter, being separated by only some arbitrary number between colors: if they have smart color separation at all.

The library is also designed for easy integration with Matplotlib, or any plotting tool that accepts 6 digit hex codes. Perfect for adding something unique to plotting loss of an AI model, which was actually why it was originally created.

Version 3.0 is the final update (minus small bug fixes) for this library. Enjoy your colors all!

## Installation

```bash
pip install random-color-hex
```

## Quick Start

### Plot Integrated Usage:
```python
import random_color_hex as RCH
import matplotlib.pyplot as plt

x=list(range(1,10))
y1=[x**3-1 for x in x]; y2=[x**2-2 for x in x]; y3=[x-3 for x in x]

# Multiple distinct colors
# All parameters (how_different_should_colors_be) are optional
plt.plot(x, y1, color=RCH.main(how_different_should_colors_be='L'))
plt.plot(x, y2, color=RCH.main(how_different_should_colors_be='L'))
plt.plot(x, y3, color=RCH.main(how_different_should_colors_be='L'))
plt.title("X Equations")
plt.show()
```
It will automatically separate the colors!

***Using color=RCH.main(), as integrated into the plot function, is the intended use. You can make it a variable by "Variable=RCH.main()", but its designed for easy integration with matplotlib (color=RCH.main()).***

### Jupyter/Non Local Usage:
```python
import random_color_hex as RCH; RCH.jupyter_reset()
```
This is needed because the Smart Color Separation subroutine stores its colors as a class variable. When you restart your script on a local machine, it is designed to reset this variable
so you can run it many times without storing the colors from past runs.
However, in some online environments, this doesnt occur because of how they were designed. So, I made a function that specifically clears this to prevent problems in different environments.

### Non-Seperated, RGB generated Color Seperated Colors
```python
import random_color_hex as RCH

print(RCH.basic_main()) #Will print a random hex code
```
This generates a random color via RGB which is not separated. This is only put in to expand what the library *can* do, not really as a drawing feature.

## Key Features/Input Parameters

### Smart Color Separation
Uses CIEDE2000 algorithm to ensure colors are **visually** distinct, not just mathematically different.

```python
# Control color separation
how_different_should_colors_be='s'   # Slight difference (~975 colors)
how_different_should_colors_be='m'   # Clear difference (~99 colors, default)
how_different_should_colors_be='l'   # Very different (~51 colors)
how_different_should_colors_be='sl'  # Extremely different (~26 colors)
```
### Brightness Control

```python
# Avoid light colors (great for white backgrounds)
RCH.main(super_light_colors_allowed=False)

# Avoid dark colors (great for dark mode)
RCH.main(super_dark_colors_allowed=False)

# Mid-tones only
RCH.main(super_light_colors_allowed=False, super_dark_colors_allowed=False)
```

### Tone Control
For all of these tone parameters: the higher the number, the more strict it is. So .5 will allow it to be more lenient than 2 (1 is default for all of these).
```python
# kL: CIEDE2000 lightness weight. >1 = more tolerant of lightness differences.
RCH.main(kl=1) #Default is 1

# kC: CIEDE2000 chroma weight. >1 = more tolerant of saturation differences.
RCH.main(kc=2) #Default is 1

# kH: CIEDE2000 hue weight. >1 = more tolerant of hue differences.
RCH.main(kh=3) #Default is 1
```

### Other Functions

```python
# Get package credits and author information
RCH.credits()

# Display usage examples and help
RCH.help()
```

## Examples

### Multi-line Plot
```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

x = [1, 2, 3, 4, 5]
plt.plot(x, [1, 2, 3, 4, 5], color=RCH.main(), label='Linear')
plt.plot(x, [1, 4, 9, 16, 25], color=RCH.main(), label='Quadratic')
plt.plot(x, [1, 8, 27, 64, 125], color=RCH.main(), label='Cubic')
plt.legend()
plt.show()
```

### Bar Chart
```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

categories = ['Python', 'R', 'Java', 'C++'] #Based off personal opinion :)
values = [100, 2, -100, 70]

for cat, val in zip(categories, values):
    plt.bar(cat, val, color=RCH.main(super_light_colors_allowed=False))
plt.show()
```

### Stateful Generation
```python
# Track color history across calls
generator = RCH.RandomColorHex()
color1 = generator.main()  # First color
color2 = generator.main()  # Guaranteed different from color1
color3 = generator.main()  # Different from both
```
This is an alternative to the much more simple RCH.main() setup. This comes from an older version of this, but I left it in as an option.

## Technical Details

- **Zero dependencies** - stdlib only
- **Python ≥3.11**
- **Cryptographically random** using `secrets` module
- **Auto-fallback**: If color separation is too restrictive, falls back to simple random generation
- **License**: Unlicense (public domain)

## Links

- **PyPI**: [https://pypi.org/project/random-color-hex/](https://pypi.org/project/random-color-hex/)
- **GitHub**: [https://github.com/BobSanders64/RandomColorHex](https://github.com/BobSanders64/RandomColorHex)
- **Author**: Nathan Honn (randomhexman@gmail.com)