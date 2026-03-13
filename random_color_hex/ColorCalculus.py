'''Color math utilities for perceptual color distance.'''

import math

class DeepColorMath:
    """RGB-to-LAB conversion and CIE2000 color distance."""

    @staticmethod
    def rgb_to_lab(r, g, b):
        """Convert RGB (0-255) to CIELAB.

        Returns:
            tuple: (L, a, b) where L is lightness 0-100,
                   a is green(-) to red(+), b is blue(-) to yellow(+).
        """
        r, g, b=r/255.0, g/255.0, b/255.0

        def gamma_expand(channel):
            if channel<=0.04045:
                return channel/12.92
            return math.pow((channel+0.055)/1.055, 2.4)

        r_linear=gamma_expand(r)
        g_linear=gamma_expand(g)
        b_linear=gamma_expand(b)

        # converts sRGB -> XYZ
        x=r_linear*0.4124564+g_linear*0.3575761+b_linear*0.1804375
        y=r_linear*0.2126729+g_linear*0.7151522+b_linear*0.0721750
        z=r_linear*0.0193339+g_linear*0.1191920+b_linear*0.9503041

        # D65 white point normalization
        x=x/0.95047
        y=y/1.00000
        z=z/1.08883

        def f(t):
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
    def hex_to_lab(hex_color):
        """Convert 6-char hex string to CIELAB. Returns (L, a, b)."""
        hex_color=hex_color.lstrip('#')
        r=int(hex_color[0:2], 16)
        g=int(hex_color[2:4], 16)
        b=int(hex_color[4:6], 16)
        return DeepColorMath.rgb_to_lab(r, g, b)

    @staticmethod
    def rgb_to_hsv(r, g, b):
        """Convert RGB (0-255) to HSV. Returns (h, s, v) with h in 0-1."""
        r, g, b=r/255.0, g/255.0, b/255.0

        max_c=max(r, g, b)
        min_c=min(r, g, b)
        delta=max_c-min_c

        v=max_c

        if max_c==0:
            s=0
        else:
            s=delta/max_c

        if delta==0:
            h=0
        elif max_c==r:
            h=(60*((g-b)/delta)+360)%360
        elif max_c==g:
            h=(60*((b-r)/delta)+120)%360
        else:
            h=(60*((r-g)/delta)+240)%360

        h=h/360.0

        return h, s, v

    @staticmethod
    def hex_to_hsv(hex_color):
        """Convert 6-char hex string to HSV. Returns (h, s, v)."""
        hex_color=hex_color.lstrip('#')
        r=int(hex_color[0:2], 16)
        g=int(hex_color[2:4], 16)
        b=int(hex_color[4:6], 16)
        return DeepColorMath.rgb_to_hsv(r, g, b)

    @staticmethod
    def ciede2000(hex1, hex2, kL=1.0, kC=1.0, kH=1.0):
        """Shows user the ciede2000 color distance between two colors.

        Args:
            hex1, hex2: 6-char hex strings, with or without '#'.
            kL, kC, kH: Weighting factors (1.0 for reference conditions).

        Returns:
            float: deltaE. Roughly <1 imperceptible, 1-2 barely,
                   2-10 noticeable, 11-49 obvious, 100+ opposite.
        """
        hex1 = hex1.lstrip('#')
        hex2 = hex2.lstrip('#')

        L1, a1, b1 = DeepColorMath.hex_to_lab(hex1)
        L2, a2, b2 = DeepColorMath.hex_to_lab(hex2)

        '''
        Lab's green-red axis is known to be too narrow compared to
        blue-yellow. G stretches it proportionally to average chroma
        so high-saturation reds don't get over-penalized.
        '''
        C1_ab = math.sqrt(a1**2 + b1**2)
        C2_ab = math.sqrt(a2**2 + b2**2)
        C_ab_avg = (C1_ab + C2_ab) / 2.0
        C_ab_avg_7 = C_ab_avg**7
        G = 0.5 * (1.0 - math.sqrt(C_ab_avg_7 / (C_ab_avg_7 + 25.0**7)))

        a1_prime = a1 * (1.0 + G)
        a2_prime = a2 * (1.0 + G)

        C1_prime = math.sqrt(a1_prime**2 + b1**2)
        C2_prime = math.sqrt(a2_prime**2 + b2**2)
        h1_prime = math.degrees(math.atan2(b1, a1_prime)) % 360.0
        h2_prime = math.degrees(math.atan2(b2, a2_prime)) % 360.0

        dL_prime = L2 - L1
        dC_prime = C2_prime - C1_prime

        # Hue difference needs special handling for the 0/360 wraparound
        if C1_prime * C2_prime == 0:
            dh_prime = 0.0
        elif abs(h2_prime - h1_prime) <= 180.0:
            dh_prime = h2_prime - h1_prime
        elif h2_prime - h1_prime > 180.0:
            dh_prime = h2_prime - h1_prime - 360.0
        else:
            dh_prime = h2_prime - h1_prime + 360.0

        dH_prime = 2.0 * math.sqrt(C1_prime * C2_prime) * math.sin(math.radians(dh_prime / 2.0))

        L_avg = (L1 + L2) / 2.0
        C_avg = (C1_prime + C2_prime) / 2.0

        # Average hue also wraps around 0/360
        if C1_prime * C2_prime == 0:
            h_avg = h1_prime + h2_prime
        elif abs(h1_prime - h2_prime) <= 180.0:
            h_avg = (h1_prime + h2_prime) / 2.0
        elif h1_prime + h2_prime < 360.0:
            h_avg = (h1_prime + h2_prime + 360.0) / 2.0
        else:
            h_avg = (h1_prime + h2_prime - 360.0) / 2.0

        # Hue-dependent weighting, these magic numbers are
        T = (1.0
             - 0.17 * math.cos(math.radians(h_avg - 30.0))
             + 0.24 * math.cos(math.radians(2.0 * h_avg))
             + 0.32 * math.cos(math.radians(3.0 * h_avg + 6.0))
             - 0.20 * math.cos(math.radians(4.0 * h_avg - 63.0)))

        L_avg_offset = (L_avg - 50.0)**2
        SL = 1.0 + 0.015 * L_avg_offset / math.sqrt(20.0 + L_avg_offset)
        SC = 1.0 + 0.045 * C_avg
        SH = 1.0 + 0.015 * C_avg * T

        C_avg_7 = C_avg**7
        RC = 2.0 * math.sqrt(C_avg_7 / (C_avg_7 + 25.0**7))
        d_theta = 30.0 * math.exp(-((h_avg - 275.0) / 25.0)**2)
        RT = -math.sin(math.radians(2.0 * d_theta)) * RC

        L_term = dL_prime / (kL * SL)
        C_term = dC_prime / (kC * SC)
        H_term = dH_prime / (kH * SH)

        return math.sqrt(L_term**2 + C_term**2 + H_term**2 + RT * C_term * H_term)

    @staticmethod
    def _are_they_looking_close(hex1, hex2, threshold=25):
        """True if two colors are within `threshold` deltaE of each other. Used for internal testing"""
        return DeepColorMath.ciede2000(hex1, hex2)<threshold


if __name__=="__main__":
    print("Red vs Green ΔE:", f"{DeepColorMath.ciede2000('FF0000', '00FF00'):.2f}")
    print("Red vs Dark Red ΔE:", f"{DeepColorMath.ciede2000('FF0000', 'FF3030'):.2f}")
    print("Blue vs Darker Blue ΔE:", f"{DeepColorMath.ciede2000('3498db', '2980b9'):.2f}")