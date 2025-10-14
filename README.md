# random_color_hex library

Have you ever thought to yourself, "man, I really wish I could make this plot a random color so debugging is less boring"?

Alternatively, "I need 20 different colors for my chart, but I don't want them to look too similar."

Congratulations! You've just located the right package/library! Just do:

```python
import random_color_hex as RCH
Color=RCH.main()
```

And then use that color in your plot

## Quick Example with Matplotlib

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

x=[1, 2, 3, 4, 5]
y=[2, 4, 6, 8, 10]

plt.plot(x, y, color=RCH.main())
plt.show()
```

That's it. Your line is now a random color

Want multiple lines with different colors? Easy:

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

x=[1, 2, 3, 4, 5]

plt.plot(x, [1, 2, 3, 4, 5], color=RCH.main(), label='Linear')
plt.plot(x, [1, 4, 9, 16, 25], color=RCH.main(), label='Quadratic')
plt.plot(x, [1, 8, 27, 64, 125], color=RCH.main(), label='Cubic')
plt.legend()
plt.show()
```

Each line gets its own random color

## The Cool Part: Smart Color Separation

This library is special in that it uses Gaurav Sharma's 2001 paper CIEDE2000 to calculate the distance between colors actually ***looks*** different instead of just being mathmatically different. Many versions of RGB generators do the latter, being separated by only some arbitrary number between colors: if they have smart color separation at all. (See below for continued discussion on this topic)

```python
import random_color_hex as RCH

# Generate colors that are guaranteed to be visually distinct
color1=RCH.main(HowDifferentShouldColorsBe='L')  # First color
color2=RCH.main(HowDifferentShouldColorsBe='L')  # Will be noticeably different
color3=RCH.main(HowDifferentShouldColorsBe='L')  # Different from both
```

The `HowDifferentShouldColorsBe` parameter controls the minimum distance between colors:
- `'s'` (small) - Slightly different
- `'m'` (medium) - Clearly different (default)
- `'l'` (large) - Very different
- `'sl'` (super large) - Extremely different

This is perfect when you need multiple colors that won't blend together

---

For most people, this will be enough no problems. However, for individuals who are using dozens of colors in one run of a program, trying to get colors that are distinct becomes less relevant than getting colors out. This library also has a backup to allow for standard RGB generation. The program will never gets stuck trying to generate a "unique" color forever if you really just want 50000 colors.

If the program gets stuck, it will let you know and request you lower your separation. If you don't, it will assume you want just a high amount of colors and will generate them with no separation. No human interaction is required for this!

Each color is generated using the secrets module as well, meaning the colors are near true random.

## Install

```bash
pip install random-color-hex
```

## Command Line Usage

You can also use it directly from the command line:

```bash
# Generate a random color
python -m random_color_hex

# Generate a color that's not super light
python -m random_color_hex --no-superlight

# Generate with specific distance from previous colors
python -m random_color_hex --distance l
```

---

## Basic Usage

### Quick One-Off Color

```python
import random_color_hex as RCH
color=RCH.main()  # Returns something like '#A3F2B6'
```

### Avoiding Light Colors (Great for White Backgrounds)

```python
import random_color_hex as RCH
color=RCH.main(SuperLightColorsAllowed=False)  # No pastels or near-white
```

### Avoiding Dark Colors (Great for Dark Mode)

```python
import random_color_hex as RCH
color=RCH.main(SuperDarkColorsAllowed=False)  # No near-black colors
```

### Mid-Tone Colors Only

```python
import random_color_hex as RCH
# Perfect for when you need colors that work on any background
color=RCH.main(SuperLightColorsAllowed=False, SuperDarkColorsAllowed=False)
```

---

## Other Useful Functions

### Instance-Based Generation (Stateful)

```python
import random_color_hex as RCH

# Create an instance to track color history
generator=RCH.RandomColorHex()

# Each call remembers previous colors
color1=generator.main()  
color2=generator.main()  # Guaranteed different from color1
color3=generator.main()  # Different from both color1 and color2
```

### Simple Random Without Distance Checking

If you just want truly random colors without any fancy separation:

```python
import random_color_hex as RCH
color=RCH.BasicMain()  # Fast, simple, no distance checking
```

---

## Real-World Examples

### Example 1: Multi-Line Plot with Super Distinct Colors

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH
import numpy as np

# Generate data
x=np.linspace(0, 10, 100)

# Plot with guaranteed distinct colors using direct call
plt.plot(x, np.sin(x), color=RCH.main(HowDifferentShouldColorsBe='SL'), label='sin(x)')
plt.plot(x, np.cos(x), color=RCH.main(HowDifferentShouldColorsBe='SL'), label='cos(x)')
plt.plot(x, np.sin(2*x), color=RCH.main(HowDifferentShouldColorsBe='SL'), label='sin(2x)')
plt.plot(x, np.cos(2*x), color=RCH.main(HowDifferentShouldColorsBe='SL'), label='cos(2x)')

plt.legend()
plt.title("Trig Functions with Super Distinct Colors")
plt.show()
```

### Example 2: Bar Chart with Random Colors

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

categories=['Python', 'JavaScript', 'Java', 'C++', 'Kotlin']
values=[100, -20, 65, 90, 45]

# Direct usage in bar chart - each bar gets a unique color
for i, (cat, val) in enumerate(zip(categories, values)):
    plt.bar(cat, val, color=RCH.main(SuperLightColorsAllowed=False))

plt.title("Programming Language Popularity")
plt.ylabel("Score")
plt.xlabel("Language")
plt.xticks(rotation=39)
plt.show()
```

### Example 3: Scatter Plot with Category Colors

```python
import matplotlib.pyplot as plt
import numpy as np
import random_color_hex as RCH

# Generate random data for 5 categories
Npoints=50
Ncategories=5

for i in range(Ncategories):
    x=np.random.normal(i, 0.5, Npoints)
    y=np.random.normal(i, 0.5, Npoints)
    
    # Direct usage - each scatter gets a distinct color
    plt.scatter(x, y, color=RCH.main(HowDifferentShouldColorsBe='L'), 
                label=f'Category {i+1}', alpha=0.6)

plt.legend()
plt.title("Clustered Data with Distinct Colors")
plt.show()
```

### Example 4: Storing Colors for Reuse

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

# Sometimes you want to store the color for multiple uses
MyFavoriteColor=RCH.main(SuperLightColorsAllowed=False)

x=[1, 2, 3, 4, 5]
y1=[2, 4, 6, 8, 10]
y2=[1, 3, 5, 7, 9]

# Use the same color for related plots
plt.subplot(1, 2, 1)
plt.plot(x, y1, color=MyFavoriteColor)
plt.title("Dataset 1")

plt.subplot(1, 2, 2)
plt.plot(x, y2, color=MyFavoriteColor)
plt.title("Dataset 2 (same color)")

plt.tight_layout()
plt.show()
```

---

## What Do The Parameters Actually Do

### SuperLightColorsAllowed=False
Excludes:
- Near-white colors (like #FFFFFF, #FEFEFE)
- Light pastels (like light pink #FFB0B0, light blue #B0B0FF)
- Light grays and neutral tones

### SuperDarkColorsAllowed=False
Excludes:
- Near-black colors (like #000000, #0A0A0A)
- Very dark shades

### HowDifferentShouldColorsBe
Uses CIEDE2000 (ΔE00) perceptual distance to ensure colors are separated:
- `'s'`: ~10 units apart (subtle difference, can generate ~663 colors)
- `'m'`: ~25 units apart (clear difference, can generate ~68 colors)
- `'l'`: ~30 units apart (strong difference, can generate ~40 colors)
- `'sl'`: ~40 units apart (maximum contrast, can generate ~23 colors)

**Note:** The algorithm will keep searching for valid colors, but generation slows down as you approach these limits

---

## Technical Notes

* **Zero deps:** stdlib-only; uses `secrets` for cryptographically random colors
* **OS:** Works on Windows/macOS/Linux/Raspberry Pi/z OS - if it can run Python 3.11, this can run.
* **Python:** >=3.11.0
* **Algorithm:** Smart RGB distance checking to ensure color separation
* **Performance:** Fast for reasonable numbers of colors. Maximum practical limits:
  - Small distance ('s'): ~663 colors
  - Medium distance ('m'): ~68 colors
  - Large distance ('l'): ~40 colors
  - Super large distance ('sl'): ~23 colors
  - After the program runs, and you plot your colors, the colors saved are reset.
* **Thread-safe:** Uses `secrets` module for random generation
* **License:** Unlicense (public domain) - Do whatever you want

---

## API Reference

### Main Functions
- `RCH.main(**kwargs)` → Returns `#RRGGBB` with smart separation
- `RCH.BasicMain(**kwargs)` → Returns `#RRGGBB` without separation checking
- `RCH.Credits()` → Shows author info
- `RCH.Help()` → Shows usage examples

### RandomColorHex Class
- `RandomColorHex().main(**kwargs)` → Stateful generation with history
- `RandomColorHex().BasicMain(**kwargs)` → Simple generation
- `RandomColorHex.AllTheColors` → Class variable tracking all generated colors

### Command Line Interface
- `python -m random_color_hex` → Generate a random color
- `python -m random_color_hex --no-superlight` → Exclude light colors
- `python -m random_color_hex --distance [s|m|l|sl]` → Set color separation

### Parameters
- `SuperLightColorsAllowed` (bool): Allow near-white/pastel colors (default: True)
- `SuperDarkColorsAllowed` (bool): Allow near-black colors (default: True)  
- `HowDifferentShouldColorsBe` (str): Color separation ['s', 'm', 'l', 'sl'] (default: 'm')

---

## Fun Facts

- The color separation algorithm runs in real-time, continuously generating until it finds a suitable color
- With any setting at its max, you're essentially creating a maximally diverse color palette
---

## Links

* **PyPI:** [https://pypi.org/project/random-color-hex/](https://pypi.org/project/random-color-hex/)
* **Source:** [https://github.com/BobSanders64/RandomColorHex](https://github.com/BobSanders64/RandomColorHex)
* **Author:** Nathan Honn (randomhexman@gmail.com)

---

Enjoy your daily dose of randomness
