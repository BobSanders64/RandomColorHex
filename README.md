````markdown
# random_color_hex

Have you ever thought to yourself, "man, I really wish I could make this plot a random color so debugging is less boring."
Well congratulations, you've just found the package for that! Just simply do:

```python
import random_color_hex as RCH
Color=RCH.main()
````

And then use that color in your plot!

Alternatively, you can also use the instance method:

```python
import random_color_hex as RCH
color=RCH.RandomColorHex()
ColorOne=color.mainI()
```

To make sure the color generated is not white (as that could be problematic):

```python
import random_color_hex as RCH
Color=RCH.main(WhiteAllowed=False)
````

or

```python
import random_color_hex as RCH
color=RCH.RandomColorHex(WhiteAllowed=False)
ColorOne=color.mainI(WhiteAllowed=False)
```


Enjoy your daily dose of randomness!

---

## Install

```bash
pip install random-color-hex
```

---

## Technical notes

* **Zero deps:** stdlib-only; uses `secrets` (cryptographic) with a safe fallback.
* **OS:** works on Windows/macOS/Linux. If it can run python 3.11.0, this can be run.
* **Python:** >=3.11.0 (pure-Python wheel).
* **API:**

  * `RCH.main()` → one-off `#RRGGBB`
  * `RCH.RandomColorHex().mainI()` → new `#RRGGBB` each call from an instance
* **CLI:** `python -m random_color_hex.random_color_hex` prints a random color and shows help/credits.
* **License:** Unlicense (public domain). Do whatever.

---

## Tiny matplotlib demo

```python
import matplotlib.pyplot as plt
import random_color_hex as RCH

Numbers=list(range(-6,7))
Line1=[x**2 for x in Numbers]
Line2=[x**3 for x in Numbers]

#One-off colors
ColorOfLine1=RCH.main()
ColorOfLine2=RCH.main()

#Or: instance you can reuse
c=RCH.RandomColorHex()
ColorOfLine3=c.mainI()

plt.plot(Numbers,Line1,color=ColorOfLine1,label="x^2")
plt.plot(Numbers,Line2,color=ColorOfLine2,label="x^3")
plt.plot(Numbers,Line1,color=ColorOfLine3,linestyle="--",label="x^2 (inst)")
plt.legend(); plt.show()
```

---

## Links

* PyPI: [https://pypi.org/project/random-color-hex/](https://pypi.org/project/random-color-hex/)
* Source: [https://github.com/BobSanders64/RandomColorHex](https://github.com/BobSanders64/RandomColorHex)

```
::contentReference[oaicite:0]{index=0}
```
