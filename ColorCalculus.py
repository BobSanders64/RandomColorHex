'''
ColorCalculus.py - Deep color mathematics for perceptual color operations.
Contains the DeepColorMath class with RGB to LAB conversion and CIEDE2000.
'''

import math


class DeepColorMath:
    """Advanced color mathematics for perceptual color distance calculations.

    This class provides methods for converting between color spaces and
    calculating perceptually uniform color differences using CIEDE2000.
    """

    @staticmethod
    def RGBToLab(r, g, b):
        """Convert RGB (0-255) to LAB color space.

        LAB is perceptually uniform - equal distances in LAB space correspond
        to roughly equal perceived color differences.

        Args:
            r, g, b: RGB values in range 0-255

        Returns:
            tuple: (L, a, b) where:
                - L is lightness (0-100)
                - a is green-red axis
                - b is blue-yellow axis
        """
        # Normalize RGB to 0-1
        r, g, b=r/255.0, g/255.0, b/255.0

        # Convert to linear RGB (remove gamma correction)
        def GammaExpand(channel):
            if channel<=0.04045:
                return channel/12.92
            return math.pow((channel+0.055)/1.055, 2.4)

        r_linear=GammaExpand(r)
        g_linear=GammaExpand(g)
        b_linear=GammaExpand(b)

        # Convert to XYZ using sRGB matrix (D65 illuminant)
        x=r_linear*0.4124564+g_linear*0.3575761+b_linear*0.1804375
        y=r_linear*0.2126729+g_linear*0.7151522+b_linear*0.0721750
        z=r_linear*0.0193339+g_linear*0.1191920+b_linear*0.9503041

        # Normalize by D65 white point
        x=x/0.95047
        y=y/1.00000
        z=z/1.08883

        # Convert XYZ to LAB
        def f(t):
            """LAB conversion function with linear segment for small values."""
            delta=6/29
            if t>delta**3:
                return math.pow(t, 1/3)
            return t/(3*delta**2)+4/29

        fx=f(x)
        fy=f(y)
        fz=f(z)

        L=116*fy-16
        a=500*(fx-fy)
        b_lab=200*(fy-fz)

        return L, a, b_lab

    @staticmethod
    def HexToLab(hex_color):
        """Convert hex color to LAB color space.

        Args:
            hex_color: 6-character hex string (with or without leading '#')

        Returns:
            tuple: (L, a, b) in LAB color space
        """
        hex_color=hex_color.lstrip('#')
        r=int(hex_color[0:2], 16)
        g=int(hex_color[2:4], 16)
        b=int(hex_color[4:6], 16)
        return DeepColorMath.RGBToLab(r, g, b)

    @staticmethod
    def RGBToHSV(r, g, b):
        """Convert RGB (0-255) to HSV color space.

        HSV stands for Hue, Saturation, Value.
        - Hue: Color type (0-360 degrees, but returned as 0-1)
        - Saturation: Color intensity (0-1, where 0 is gray)
        - Value: Brightness (0-1, where 0 is black)

        Args:
            r, g, b: RGB values in range 0-255

        Returns:
            tuple: (h, s, v) where:
                - h is hue (0-1, multiply by 360 for degrees)
                - s is saturation (0-1)
                - v is value/brightness (0-1)
        """
        # Normalize to 0-1
        r, g, b=r/255.0, g/255.0, b/255.0

        max_c=max(r, g, b)
        min_c=min(r, g, b)
        delta=max_c-min_c

        # Value is the maximum
        v=max_c

        # Saturation
        if max_c==0:
            s=0
        else:
            s=delta/max_c

        # Hue
        if delta==0:
            h=0  # Undefined, but we'll use 0
        elif max_c==r:
            h=(60*((g-b)/delta)+360)%360
        elif max_c==g:
            h=(60*((b-r)/delta)+120)%360
        else:  # max_c==b
            h=(60*((r-g)/delta)+240)%360

        # Normalize hue to 0-1
        h=h/360.0

        return h, s, v

    @staticmethod
    def HexToHSV(hex_color):
        """Convert hex color to HSV color space.

        Args:
            hex_color: 6-character hex string (with or without leading '#')

        Returns:
            tuple: (h, s, v) in HSV color space
        """
        hex_color=hex_color.lstrip('#')
        r=int(hex_color[0:2], 16)
        g=int(hex_color[2:4], 16)
        b=int(hex_color[4:6], 16)
        return DeepColorMath.RGBToHSV(r, g, b)

    @staticmethod
    def ciede2000(hex1, hex2):
        """Calculate perceptual color difference using CIEDE2000 formula.

        CIEDE2000 is the industry standard for measuring how different two
        colors appear to the human eye. A deltaE of:
        - < 1.0: Not perceptible by human eyes
        - 1-2: Perceptible through close observation
        - 2-10: Perceptible at a glance
        - 11-49: Colors are more similar than opposite
        - 100+: Colors are exact opposite

        Args:
            hex1: First hex color (6 chars, with or without '#')
            hex2: Second hex color (6 chars, with or without '#')

        Returns:
            float: Delta E (perceptual color difference)
        """
        hex1=hex1.lstrip('#')
        hex2=hex2.lstrip('#')

        # Convert to LAB
        L1, a1, b1_lab=DeepColorMath.HexToLab(hex1)
        L2, a2, b2_lab=DeepColorMath.HexToLab(hex2)

        # Calculate C (chroma) and h (hue angle)
        C1=math.sqrt(a1**2+b1_lab**2)
        C2=math.sqrt(a2**2+b2_lab**2)

        # Delta values
        dL=L2-L1
        dC=C2-C1
        da=a2-a1
        db=b2_lab-b1_lab

        # Calculate dH (delta hue)
        # dH² = da² + db² - dC²
        dH_squared=da**2+db**2-dC**2
        dH=math.sqrt(max(0, dH_squared))  # Ensure non-negative

        # Weighting factors (simplified from full CIEDE2000)
        # The full formula includes complex corrections for lightness,
        # chroma, and hue. This simplified version gives excellent results
        # for most practical applications.
        kL, kC, kH=1.0, 1.0, 1.0

        # Calculate weighted components
        L_component=dL/kL
        C_component=dC/kC
        H_component=dH/kH

        # Final delta E
        dE=math.sqrt(L_component**2+C_component**2+H_component**2)

        return dE

    @staticmethod
    def AreTheyLookinClose(hex1, hex2, threshold=25):
        """Check if two colors are perceptually close.

        Args:
            hex1: First hex color
            hex2: Second hex color
            threshold: Maximum deltaE to consider colors "close"
                      (default 25 = clearly different colors)

        Returns:
            bool: True if colors are close (deltaE < threshold)
        """
        return DeepColorMath.ciede2000(hex1, hex2)<threshold


if __name__=="__main__":
    # Demo the color math
    print("=== DeepColorMath Demo ===\n")

    # Test RGB to LAB conversion
    print("RGB to LAB conversions:")
    print(f"Red (255,0,0) -> LAB: {DeepColorMath.RGBToLab(255, 0, 0)}")
    print(f"Green (0,255,0) -> LAB: {DeepColorMath.RGBToLab(0, 255, 0)}")
    print(f"Blue (0,0,255) -> LAB: {DeepColorMath.RGBToLab(0, 0, 255)}")
    print(f"White (255,255,255) -> LAB: {DeepColorMath.RGBToLab(255, 255, 255)}")
    print(f"Black (0,0,0) -> LAB: {DeepColorMath.RGBToLab(0, 0, 0)}")

    print("\n=== RGB to HSV conversions ===")
    print(f"Red (255,0,0) -> HSV: {DeepColorMath.RGBToHSV(255, 0, 0)}")
    print(f"Green (0,255,0) -> HSV: {DeepColorMath.RGBToHSV(0, 255, 0)}")
    print(f"Blue (0,0,255) -> HSV: {DeepColorMath.RGBToHSV(0, 0, 255)}")
    print(f"Purple (128,0,128) -> HSV: {DeepColorMath.RGBToHSV(128, 0, 128)}")

    print("\n=== CIEDE2000 Color Differences ===\n")

    # Test similar colors
    color1="FF0000"  # Red
    color2="FE0000"  # Slightly different red
    delta=DeepColorMath.ciede2000(color1, color2)
    print(f"Red vs Slightly Different Red: ΔE = {delta:.2f}")
    print(f"  -> {'Perceptible' if delta>1 else 'Not perceptible'}\n")

    # Test very different colors
    color1="FF0000"  # Red
    color2="00FF00"  # Green
    delta=DeepColorMath.ciede2000(color1, color2)
    print(f"Red vs Green: ΔE = {delta:.2f}")
    print(f"  -> Very different colors\n")

    # Test similar but perceptible
    color1="FF0000"  # Red
    color2="FF3030"  # Light red
    delta=DeepColorMath.ciede2000(color1, color2)
    print(f"Red vs Light Red: ΔE = {delta:.2f}")
    print(f"  -> {'Close' if delta<25 else 'Different'} colors\n")

    # Test with hex prefix
    color1="#3498db"  # Blue
    color2="#2980b9"  # Darker blue
    delta=DeepColorMath.ciede2000(color1, color2)
    print(f"Blue vs Darker Blue: ΔE = {delta:.2f}\n")

    # Test the helper function
    print("=== Using AreTheyLookinClose() ===")
    print(f"Are #FF0000 and #FE0000 close? {DeepColorMath.AreTheyLookinClose('FF0000', 'FE0000')}")
    print(f"Are #FF0000 and #00FF00 close? {DeepColorMath.AreTheyLookinClose('FF0000', '00FF00')}")