# random_color_hex

Have you ever thought to yourself, "man, I really wish I could make this plot a random color so debugging is less boring"?

Well congratulations, you've just found the package for that! Just simply do:

```python
import random_color_hex as RCH
Color = RCH.main()
```

And then use that color in your plot!

Alternatively, you can also use the instance method:

```python
import random_color_hex as RCH
color = RCH.RandomColorHex()
ColorOne = color.mainI()
```

To make sure the color generated is not a super light color close to white (as that could be problematic):

```python
import random_color_hex as RCH
Color = RCH.main(SuperLightColorsAllowed=False)
```

Or with the instance method:

```python
import random_color_hex as RCH
color = RCH.RandomColorHex()
ColorOne = color.mainI(SuperLightColorsAllowed=False)
```

Enjoy your daily dose of randomness!

---

## Install

```bash
pip install random-color-hex
```

---

## Technical Notes

* **Zero deps:** stdlib-only; uses `secrets` (cryptographic) with a safe fallback to `random`
* **OS:** Works on Windows/macOS/Linux. If it can run Python 3.11.0, this can run
* **Python:** ≥3.11.0 (pure-Python wheel)
* **API:**
  * `RCH.main()` → one-off `#RRGGBB` 
  * `RCH.RandomColorHex().mainI()` → new `#RRGGBB` each call from an instance
  * `SuperLightColorsAllowed=False` → exclude pastels and near-white colors
* **CLI:** `python -m random_color_hex` prints a random color and shows help/credits
* **License:** Unlicense (public domain). Do whatever

---

## Tiny Matplotlib Demo

### Example 1: Basic Usage

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

Numbers = list(range(-6, 7))
Line1 = [x**2 for x in Numbers]
Line2 = [x**3 for x in Numbers]

# One-off colors
ColorOfLine1 = RCH.main()
ColorOfLine2 = RCH.main()

# Or: instance you can reuse
c = RCH.RandomColorHex()
ColorOfLine3 = c.mainI()

plt.plot(Numbers, Line1, color=ColorOfLine1, label="x²")
plt.plot(Numbers, Line2, color=ColorOfLine2, label="x³")
plt.plot(Numbers, Line1, color=ColorOfLine3, linestyle="--", label="x² (inst)")
plt.legend()
plt.show()
```

### Example 2: Light vs Dark Colors Comparison

```python
import matplotlib.pyplot as plt
import numpy as np
import random_color_hex as RCH

# Figure 1: No Light Colors
plt.figure(1)
fig, axes = plt.subplots(20, 20)
xaxis = np.linspace(-10, 10, 41)
yaxis = [x**2 for x in xaxis]
for i in range(20):
    for j in range(20):
        axes[i,j].plot(xaxis, yaxis, color=RCH.main(SuperLightColorsAllowed=False))
        axes[i,j].axis('off')
plt.suptitle("No Light Colors Allowed")
plt.show()

# Figure 2: All Colors
plt.figure(2)
fig, axes = plt.subplots(20, 20)
xaxis = np.linspace(-10, 10, 41)
yaxis = [x**2 for x in xaxis]
for i in range(20):
    for j in range(20):
        axes[i,j].plot(xaxis, yaxis, color=RCH.main())
        axes[i,j].axis('off')
plt.suptitle("Light Colors Allowed")
plt.show()
```

---

## What Does SuperLightColorsAllowed=False Do?

When `SuperLightColorsAllowed=False`, the generator excludes:
- Near-white colors (like #FFFFFF, #FEFEFE)
- Light pastels (like light pink #FFB0B0, light blue #B0B0FF)
- Light grays and neutral tones
- Any color where all RGB channels are high

This ensures you get vibrant, saturated colors that stand out well against white backgrounds!

---

## Links

* **PyPI:** [https://pypi.org/project/random-color-hex/](https://pypi.org/project/random-color-hex/)
* **Source:** [https://github.com/BobSanders64/RandomColorHex](https://github.com/BobSanders64/RandomColorHex)
* **Author:** Nathan Honn (randomhexman@gmail.com)
