'''
Will output a random hex code, CSS style 6 digit "RRGGBB" format.
'''

import secrets
import time as tym
import atexit
from .ColorCalculus import DeepColorMath

class RandomColorHex:
    """Stateful random color generator.

    This class can repeatedly generate readable hex colors while:
    - optionally avoiding white and near-white/pastel tones, and
    - ensuring successive colors from the SAME instance are separated
      by a minimum RGB distance.

    Notes
    -----
    * `AllTheColors` is a class-level list of colors previously yielded
      by any instance; it is used to avoid generating a color too close
      to an existing one.
    * Each instance keeps the last generated hex in `self.RandomHexCode`.
    """
    AllTheColors=[]
    EpochCount={'S':0,'M':0,'L':0,'SL':0}
    EpochSize={'S':663,'M':68,'L':40,'SL':23}
    _auto_reset_registered=False
    MassProduction = False

    @classmethod
    def _reset(cls):
        """Clear class-level state that tracks previously used colors."""
        cls.AllTheColors.clear()
        cls.EpochCount={'S':0,'M':0,'L':0,'SL':0}

    @classmethod
    def _register_auto_reset(cls):
        """Register automatic reset on program exit."""
        if not cls._auto_reset_registered:
            atexit.register(cls._reset)
            cls._auto_reset_registered=True
            MassProduction = False

    def __init__(self):
        """Initialize internal buffers and near-white masks.

        Sets:
          - `self.RandomHexCode` (list[str]): last generated 'RRGGBB' (no '#').
          - `self.NearWhiteMasks` (list[str]): patterns like 'FHFHFH', where:
              'X' = any hex digit 0–F,
              'H' = high hex digit 8–F,
              other letters = exact nibble match.
        """
        self.RandomHexCode=[] #So you can access the code later for any instance
        self.NearWhiteMasks=['FHFHFH','FXFXFX','FHFHFX','XFHFHF','EHFHFH','HHHHHH']  #neutral, warm, cool, very light gray
        self._register_auto_reset()

    def MatchesMask(self, hex6, mask):
        """Return True if the 6-char hex string matches a mask.

        Mask semantics:
          - 'X' → any hex digit (0–F).
          - 'H' → high nibble (8–F).
          - other hex characters → must match exactly.

        Both inputs may include or omit the leading '#'.
        """
        hex6=hex6.upper().lstrip('#')
        mask=mask.upper().lstrip('#')
        if len(hex6)!=6 or len(mask)!=6:
            return False

        def ok(h, m):
            if m=='X':
                return h in '0123456789ABCDEF'
            if m=='H':
                return h in '89ABCDEF'
            return h==m

        return all(ok(h, m) for h, m in zip(hex6, mask))

    def ChannelsClose(self, hex6, max_delta=20)->bool:
        """Heuristic for “grayish”: True if RGB channels are very similar.

        Computes max(|R−G|, |R−B|, |G−B|) and compares to `max_delta`.
        Use this to detect low-saturation, gray-like colors.
        """
        hex6=hex6.lstrip('#')
        r=int(hex6[0:2], 16)
        g=int(hex6[2:4], 16)
        b=int(hex6[4:6], 16)
        return max(abs(r-g), abs(r-b), abs(g-b))<=max_delta

    def AreColorsClose(self, InputColor, MetricBar):
        """Return True if `InputColor` is within `MetricBar` of any prior color.

        Uses Euclidean distance in RGB space between the candidate color and
        all entries in `self.AllTheColors`. If any distance ≤ `MetricBar`, the
        color is considered “too close”.

        OUTDATED, USE ONLY FOR BASICMAIN
        """
        R1=int(InputColor[0:2],16)
        G1=int(InputColor[2:4],16)
        B1=int(InputColor[4:6],16)
        for prev in self.AllTheColors:
            R2=int(prev[0:2],16)
            G2=int(prev[2:4],16)
            B2=int(prev[4:6],16)
            #Euclidean distance in RGB
            d=((R1-R2)**2+(G1-G2)**2+(B1-B2)**2)**0.5
            if d<=MetricBar:
                return True
        return False

    def AreColorsClosePerceptual(self, InputColor, threshold):
        """Return True if `InputColor` is within perceptual `threshold` of any prior color.

        Uses CIEDE2000 perceptual distance from ColorCalculus.
        """
        for prev in self.AllTheColors:
            if DeepColorMath.ciede2000(InputColor, prev) < threshold:
                return True
        return False

    def IsNearWhite(self, hex6:str):
        """Return True if the color is near white / very light.

        Checks a combination of:
          * near-white mask matches (e.g., 'FHFHFH'),
          * minimum channel threshold (pastel-like if min(R,G,B) > 180),
          * high average brightness,
          * light gray detection via `ChannelsClose(...)`.
        """
        hex6=hex6.lstrip('#')

        #Check against near-white masks
        for mask in self.NearWhiteMasks:
            if self.MatchesMask(hex6, mask):
                return True

        r=int(hex6[0:2], 16)
        g=int(hex6[2:4], 16)
        b=int(hex6[4:6], 16)

        #If the MINIMUM channel is high, it's a light/pastel color
        #(e.g., light pink has high R,G,B with R slightly higher)
        if min(r,g,b)>180:
            return True

        #Check average brightness for overall light colors
        avg_brightness=(r+g+b)/3
        if avg_brightness>200:
            return True

        #Check if it's a light gray (medium-high values with channels close)
        if avg_brightness>150 and self.ChannelsClose(hex6, 20):
            return True

        return False

    def IsNearBlack(self, hex6: str) -> bool:
        """Return True if the color is very dark/near black."""
        hex6=hex6.lstrip('#')
        r=int(hex6[0:2], 16)
        g=int(hex6[2:4], 16)
        b=int(hex6[4:6], 16)
        avg=(r+g+b)/3
        if max(r, g, b)<40:
            return True
        if avg<35:
            return True
        if avg<70 and self.ChannelsClose(hex6, 15):
            return True
        return False

    def RandomHex(self):
        """Generate a fresh 6-digit hex (no '#') into `self.RandomHexCode`.

        The result is a list of six characters chosen from 0–9 and A–F.
        Callers typically join the list and prepend '#'.
        """
        self.RandomHexCode=[] #Resets the color
        Alphabet=('A', 'B', 'C', 'D', 'E', 'F')
        for _ in range(6):
            LetterOrNumber=secrets.randbelow(2) #Will decide if it will be a letter or number
            if LetterOrNumber==0:
                Choice=str(secrets.randbelow(10))
            else:
                Choice=secrets.choice(Alphabet)
            self.RandomHexCode.append(Choice)

    @staticmethod
    def BasicMain(SuperLightColorsAllowed=True, SuperDarkColorsAllowed=True):
        if RandomColorHex.EpochCount['S']>=RandomColorHex.EpochSize['S']:
            RandomColorHex.AllTheColors.clear()
            RandomColorHex.EpochCount['S']=0
        RC=RandomColorHex()
        RC.RandomHex()
        hex6=''.join(RC.RandomHexCode)
        if not SuperLightColorsAllowed and not SuperDarkColorsAllowed:
            while RC.IsNearWhite(hex6) or RC.IsNearBlack(hex6):
                RC.RandomHex(); hex6=''.join(RC.RandomHexCode)
        elif not SuperLightColorsAllowed:
            while RC.IsNearWhite(hex6):
                RC.RandomHex(); hex6=''.join(RC.RandomHexCode)
        elif not SuperDarkColorsAllowed:
            while RC.IsNearBlack(hex6):
                RC.RandomHex(); hex6=''.join(RC.RandomHexCode)
        RC.RandomHexCode.insert(0,'#')
        out=''.join(RC.RandomHexCode)
        RandomColorHex.EpochCount['S']+=1
        return out

    def main(self, SuperLightColorsAllowed=True, SuperDarkColorsAllowed=True,HowDifferentShouldColorsBe='m'):
        match HowDifferentShouldColorsBe:
            case 'M'|'m':
                mode='M'; PerceptualThreshold=25
            case 'S'|'s':
                mode='S'; PerceptualThreshold=10
            case "L"|"l":
                mode='L'; PerceptualThreshold=30
            case "SL"|"sl"|"sL"|"Sl":
                mode='SL'; PerceptualThreshold=40
            case _:
                raise ValueError('Invalid HowDifferentShouldColorsBe parameter! Please type "s" (small), "m" (medium), "l" (large), or "sl" (super large).')
        if RandomColorHex.EpochCount[mode]>=RandomColorHex.EpochSize[mode]:
            self.AllTheColors.clear()
            RandomColorHex.EpochCount[mode]=0
        self.RandomHex()
        start=tym.time()
        OneNotice=True
        while True:
            if OneNotice and (tym.time()-start)>=40:
                print(
                    "Note! It seems you're generating a lot of colors. The algorithm will keep searching, "
                    "but it's going to take a while!\n"
                    "This may be because the distance metric is too large (HowDifferentShouldColorsBe).\n"
                    "Generally, anything over 40 colors with L set up starts having trouble.\n"
                    "Super Large starts having trouble at 23\n"
                    "Small can do ~663\n"
                    "Medium can do ~68\n"
                    "For quicker results, please use either BasicMain() or HowDifferentShouldColorsBe='S' or 'M'."
                )
                OneNotice=False

            if (tym.time()-start)>80 or self.MassProduction:
                self.MassProduction=True
                print("Timeout reached (80 seconds). Switching to BasicMain mode for remaining colors.")
                #Generate color without distance checking
                return self.BasicMain(SuperLightColorsAllowed=SuperLightColorsAllowed, SuperDarkColorsAllowed=SuperDarkColorsAllowed)

            OutputtedString=''.join(self.RandomHexCode)
            if not SuperLightColorsAllowed and self.IsNearWhite(OutputtedString):
                self.RandomHex()
                continue
            if not SuperDarkColorsAllowed and self.IsNearBlack(OutputtedString):
                self.RandomHex()
                continue
            if self.AreColorsClosePerceptual(OutputtedString, PerceptualThreshold):
                self.RandomHex()
                continue
            break
        self.AllTheColors.append(''.join(self.RandomHexCode))
        self.RandomHexCode.insert(0,'#')
        RandomColorHex.EpochCount[mode]+=1
        return ''.join(self.RandomHexCode)

    @staticmethod
    def Credits():
        """
        Giving credit to the creator of the library.
        """
        print("Made by Nathan Honn, randomhexman@gmail.com")

    @staticmethod
    def Help():
        """Print a short usage example demonstrating both entry points.

        Shows:
          * one-off generation with `BasicMain()`, and
          * instance-based generation with `.main()` that encourages
            color separation for successive lines/series.
        """
        print("""
        import matplotlib.pyplot as plt
        import random_color_hex as RCH
        
        Numbers=list(range(-6,7))
        Line1=[x**2 for x in Numbers]
        Line2=[x**3 for x in Numbers]
        
        #For a one off random color:
        ColorOfLine1=RCH.BasicMain()
        ColorOfLine2=RCH.BasicMain()
        
        #For the main feature of the library, use the normal main() method:
        ColorOfLine1=RCH.main()
        ColorOfLine2=RCH.main()
        
        plt.plot(Numbers,Line1,color=ColorOfLine1,label="x²")
        plt.plot(Numbers,Line2,color=ColorOfLine2,label="x³")
        plt.title("Graph of X² v X³")
        plt.legend()
        plt.show()
        """)

    @staticmethod
    def John_3_Verse_16():
        print("For this is how God loved the world: He gave his one and only Son, so that everyone who believes in him will not perish but have eternal life.")

if __name__=="__main__":
    c=RandomColorHex()
    print(c.main())
    print(c.main(SuperLightColorsAllowed=False, SuperDarkColorsAllowed=False, HowDifferentShouldColorsBe='m'))
    for index in range(5000):
        print(f"{index}, {c.main(HowDifferentShouldColorsBe='m')}")
    print(c.BasicMain())
    c.Credits()
    c.Help()

