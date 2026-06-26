'''Generate random hex codes in CSS-style 6-digit "RRGGBB" format.
basic_main and main are in the same class because they are interrelated function wise.
I call basic_main if main stalls too long. Thats why its 1 class vs 2 (plus ease of programming)
'''

import secrets
import time
import atexit
try:
    from .ColorCalculus import DeepColorMath
except (ImportError, ValueError):
    from ColorCalculus import DeepColorMath

class RandomColorHex:
    """Stateful random color generator that avoids repeating visually similar colors.

    Tracks previously generated colors at the class level so successive calls
    from any instance maintain perceptual distance between colors.
    """
    all_colors = []
    _auto_reset_registered = False
    _mass_production = False

    @classmethod
    def _reset(cls):
        """Clear previously used color history."""
        cls.all_colors.clear()

    @classmethod
    def _register_auto_reset(cls):
        if not cls._auto_reset_registered:
            atexit.register(cls._reset)
            cls._auto_reset_registered = True
            cls._mass_production = False

    def __init__(self):
        self.random_hex_code = []
        # Mask key: X=any hex digit, H=high nibble (8-F), letter=exact match
        self.near_white_masks = ['FHFHFH', 'FXFXFX', 'FHFHFX', 'XFHFHF', 'EHFHFH', 'HHHHHH']
        self._register_auto_reset()

    def matches_mask(self, hex6, mask):
        """True if hex6 matches the mask pattern.

        Args:
            hex6: 6-char hex string, with or without '#'.
            mask: 6-char pattern, 'X'=any hex digit, 'H'=high nibble (8-F),
                  any other hex char=exact match.
        """
        hex6 = hex6.upper().lstrip('#')
        mask = mask.upper().lstrip('#')
        if len(hex6) != 6 or len(mask) != 6:
            return False

        def ok(h, m):
            if m == 'X':
                return h in '0123456789ABCDEF'
            if m == 'H':
                return h in '89ABCDEF'
            return h == m

        return all(ok(h, m) for h, m in zip(hex6, mask))

    def channels_close(self, hex6, max_delta=20) -> bool:
        """True if all RGB channels are within max_delta of each other (grayish)."""
        hex6 = hex6.lstrip('#')
        r = int(hex6[0:2], 16)
        g = int(hex6[2:4], 16)
        b = int(hex6[4:6], 16)
        return max(abs(r - g), abs(r - b), abs(g - b)) <= max_delta

    def are_colors_close_perceptual(self, input_color, threshold, kL=1.0, kC=1.0, kH=1.0):
        """True if input_color is within perceptual threshold of any prior color.

        Args:
            input_color: 6-char hex string (no '#').
            threshold: CIEDE2000 deltaE value. Lower = stricter (5 is tight, 20 is loose).
            kL, kC, kH: CIEDE2000 weighting factors for lightness, chroma, hue.
        """
        for prev in self.all_colors:
            if DeepColorMath.ciede2000(input_color, prev, kL, kC, kH) < threshold:
                return True
        return False

    def is_near_white(self, hex6: str):
        """True if the color is near-white, pastel, or light gray."""
        hex6 = hex6.lstrip('#')

        for mask in self.near_white_masks:
            if self.matches_mask(hex6, mask):
                return True

        r = int(hex6[0:2], 16)
        g = int(hex6[2:4], 16)
        b = int(hex6[4:6], 16)

        if min(r, g, b) > 180:
            return True

        avg_brightness = (r + g + b) / 3
        if avg_brightness > 200:
            return True

        if avg_brightness > 150 and self.channels_close(hex6, 20):
            return True

        return False

    def is_near_black(self, hex6: str) -> bool:
        """True if the color is very dark or near-black."""
        hex6 = hex6.lstrip('#')
        r = int(hex6[0:2], 16)
        g = int(hex6[2:4], 16)
        b = int(hex6[4:6], 16)
        avg = (r + g + b) / 3
        if max(r, g, b) < 40:
            return True
        if avg < 35:
            return True
        if avg < 70 and self.channels_close(hex6, 15):
            return True
        return False

    def random_hex(self):
        """Generate a random 6-digit hex into self.random_hex_code."""
        self.random_hex_code = []
        alphabet = ('A', 'B', 'C', 'D', 'E', 'F')
        for _ in range(6):
            letter_or_number = secrets.randbelow(2)
            if letter_or_number == 0:
                choice = str(secrets.randbelow(10))
            else:
                choice = secrets.choice(alphabet)
            self.random_hex_code.append(choice)

    @staticmethod
    def basic_main(super_light_colors_allowed=True, super_dark_colors_allowed=True):
        """Quick random color without perceptual distance checking.

        Returns:
            str: CSS hex color string like '#A3F02B'.
        """
        rc = RandomColorHex()
        rc.random_hex()
        hex6 = ''.join(rc.random_hex_code)
        if not super_light_colors_allowed and not super_dark_colors_allowed:
            while rc.is_near_white(hex6) or rc.is_near_black(hex6):
                rc.random_hex(); hex6 = ''.join(rc.random_hex_code)
        elif not super_light_colors_allowed:
            while rc.is_near_white(hex6):
                rc.random_hex(); hex6 = ''.join(rc.random_hex_code)
        elif not super_dark_colors_allowed:
            while rc.is_near_black(hex6):
                rc.random_hex(); hex6 = ''.join(rc.random_hex_code)
        rc.random_hex_code.insert(0, '#')
        return ''.join(rc.random_hex_code)

    def main(self, super_light_colors_allowed=True, super_dark_colors_allowed=True,
             how_different_should_colors_be='m', kL=1.0, kC=1.0, kH=1.0):
        """Generate a random hex color with perceptual distance from prior colors.

        Rejection sampling gets slower as the color list grows. After 21 seconds
        of searching, falls back to basic_main for remaining colors.

        Args:
            how_different_should_colors_be: Minimum distance between colors.
                's' (small), 'm' (medium), 'l' (large), 'sl' (super large).
            kL: CIEDE2000 lightness weight. >1 = more tolerant of lightness differences.
            kC: CIEDE2000 chroma weight. >1 = more tolerant of saturation differences.
            kH: CIEDE2000 hue weight. >1 = more tolerant of hue differences.

        Returns:
            str: CSS hex color string like '#A3F02B'.
        """
        match how_different_should_colors_be:
            case 'M' | 'm':
                perceptual_threshold = 12
            case 'S' | 's':
                perceptual_threshold = 5
            case 'L' | 'l':
                perceptual_threshold = 15
            case 'SL' | 'sl' | 'sL' | 'Sl':
                perceptual_threshold = 20
            case _:
                raise ValueError(
                    'Invalid how_different_should_colors_be parameter! '
                    'Please type "s" (small), "m" (medium), "l" (large), or "sl" (super large).'
                )
        self.random_hex()
        start = time.time()
        one_notice = True
        while True:
            if one_notice and (time.time() - start) >= 12:
                print(
                    "Note! It seems you're generating a lot of colors. The algorithm will keep searching, "
                    "but it's going to take a while!\n"
                    "This may be because the distance metric is too large (how_different_should_colors_be).\n"
                    "Generally, anything over 26 colors with Super Large starts having trouble.\n"
                    "Large starts having trouble at 51\n"
                    "Medium can do ~99\n"
                    "Small can do ~975\n"
                    "For quicker results, please use either basic_main() or how_different_should_colors_be='s' or 'm'."
                    "Allowing light/dark colors, or changing the tones, also helps!"
                )
                one_notice = False

            if (time.time() - start) > 21 or self._mass_production:
                self._mass_production = True
                print("Timeout reached (21 seconds). Switching to basic_main mode for remaining colors.")
                return self.basic_main(
                    super_light_colors_allowed=super_light_colors_allowed,
                    super_dark_colors_allowed=super_dark_colors_allowed,
                )

            candidate = ''.join(self.random_hex_code)
            if not super_light_colors_allowed and self.is_near_white(candidate):
                self.random_hex()
                continue
            if not super_dark_colors_allowed and self.is_near_black(candidate):
                self.random_hex()
                continue
            if self.are_colors_close_perceptual(candidate, perceptual_threshold, kL, kC, kH):
                self.random_hex()
                continue
            break
        self.all_colors.append(''.join(self.random_hex_code))
        self.random_hex_code.insert(0, '#')
        return ''.join(self.random_hex_code)

    @staticmethod
    def credits():
        print("Made by Nathan Honn, randomhexman@gmail.com")

    @staticmethod
    def help():
        print("""
        import matplotlib.pyplot as plt
        import random_color_hex as RCH

        numbers=list(range(-6,7))
        line1=[x**2 for x in numbers]
        line2=[x**3 for x in numbers]

        #For a one off random color:
        color_of_line1=RCH.basic_main()
        color_of_line2=RCH.basic_main()

        #For the main feature of the library, use the normal main() method:
        color_of_line1=RCH.main()
        color_of_line2=RCH.main()

        plt.plot(numbers,line1,color=color_of_line1,label="x²")
        plt.plot(numbers,line2,color=color_of_line2,label="x³")
        plt.title("Graph of X² v X³")
        plt.legend()
        plt.show()
        """)

    @staticmethod
    def john_3_verse_16():
        print("For this is how God loved the world: He gave his one and only Son, so that everyone who believes in him will not perish but have eternal life.")

if __name__ == "__main__":
    c = RandomColorHex()
    print(c.main())
    print(c.main(super_light_colors_allowed=False, super_dark_colors_allowed=False, how_different_should_colors_be='m'))
    for index in range(5000):
        print(f"{index}, {c.main(how_different_should_colors_be='s',kH=.2)}")
    print(c.basic_main())
    c.credits()
    c.help()
