'''
Will output a random hex code, CSS style 6 digit "RRGGBB" format.
'''

try:
    import secrets
except ImportError:
    import random as secrets

class RandomColorHex:
    def __init__(self):
        self.RandomHexCode=[] #So you can access the code later for any instance
        self.NearWhiteMasks=['FHFHFH','FXFXFX','FHFHFX','XFHFHF','EHFHFH','HHHHHH']  #neutral, warm, cool, very light gray

    def MatchesMask(self, hex6, mask):
        """Check if a hex color matches a given mask pattern"""
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

    def ChannelsClose(self, hex6, max_delta=20):
        """Check if RGB channels are too close together (indicates grayish color)"""
        hex6=hex6.lstrip('#')
        r=int(hex6[0:2], 16)
        g=int(hex6[2:4], 16)
        b=int(hex6[4:6], 16)
        return max(abs(r-g), abs(r-b), abs(g-b))<=max_delta

    def IsNearWhite(self, hex6:str):
        """Check if a color is near white using masks and channel closeness"""
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
        if min(r, g, b) > 180:
            return True

        #Check average brightness for overall light colors
        avg_brightness=(r+g+b)/3
        if avg_brightness>200:
            return True

        #Check if it's a light gray (medium-high values with channels close)
        if avg_brightness>150 and self.ChannelsClose(hex6, 20):
            return True

        return False

    def RandomHex(self):
        """
        Generates a random hexadecimal color code by creating a list of six characters,
        each of which can either be a letter (A-F) or a number (0-9). Letters are selected
        from a predefined alphabet, while numbers are randomly chosen within a specific range.

        :return: A list of six characters that together represent a random hex color code.
        :rtype: list[str]
        """
        self.RandomHexCode=[] #Resets the color
        Alphabet=('A', 'B', 'C', 'D', 'E', 'F')
        for i in range(6):
            LetterOrNumber=secrets.randbelow(2) #Will decide if it will be a letter or number
            if LetterOrNumber==0:
                Choice=str(secrets.randbelow(10))
            else:
                Choice=secrets.choice(Alphabet)
            self.RandomHexCode.append(Choice)

    def mainI(self, SuperLightColorsAllowed=True): #Instance mode of main
        """
        Generates a random hex color code, ensuring it avoids white or near-white colors
        when specified.

        The function generates a random hexadecimal color code in the format '#RRGGBB'.
        If the `SuperLightColorsAllowed` parameter is set to `False`, it prevents generating colors
        that are close to white by continuously regenerating codes until the condition
        is satisfied.

        :param SuperLightColorsAllowed: A boolean indicating whether white or near-white colors
            are allowed in the generated hex code.
        :type SuperLightColorsAllowed: bool
        :return: A string containing the generated hex color code in the format '#RRGGBB'.
        :rtype: str
        """
        self.RandomHex()
        while SuperLightColorsAllowed==False and self.IsNearWhite(''.join(self.RandomHexCode))==True:
            self.RandomHex()

        self.RandomHexCode.insert(0,'#')
        return ''.join(self.RandomHexCode)

    @staticmethod
    def main(SuperLightColorsAllowed=True): #Made for if you just wanna do a one off color
        """
        Generates a random hexadecimal color code. Optionally, the method ensures
        that the generated color is not close to white, if specified.

        :param SuperLightColorsAllowed: Determines whether the generated color can be near
            white. If True, the color may be close to white. Defaults to True.
        :type SuperLightColorsAllowed: bool
        :return: A random hexadecimal color code as a string that may or may
            not be near white, depending on the `SuperLightColorsAllowed` parameter.
        :rtype: str
        """
        RC=RandomColorHex()
        RC.RandomHex()
        while SuperLightColorsAllowed==False and RC.IsNearWhite(''.join(RC.RandomHexCode))==True:
            RC.RandomHex()

        RC.RandomHexCode.insert(0,'#')
        return ''.join(RC.RandomHexCode)

    @staticmethod
    def Credits():
        """
        Giving credit to the creator of the library.
        """
        print("Made by Nathan Honn, randomhexman@gmail.com")

    @staticmethod
    def Help():
        """
        Provides a static method to display a detailed help guide for utilizing the library.

        The help includes an example script demonstrating the usage of both one-off
        random colors and reusable instance-based random colors for graph plotting
        with Matplotlib.

        :rtype: None
        :return: None
        """
        print("""
        import matplotlib.pyplot as plt
        import random_color_hex as RCH
        
        Numbers=list(range(-6,7))
        Line1=[x**2 for x in Numbers]
        Line2=[x**3 for x in Numbers]
        
        #For a one off random color:
        ColorOfLine1=RCH.main()
        ColorOfLine2=RCH.main()
        
        #For an instance random color (to be reused later):
        color1,color2=RCH.RandomColorHex(),RCH.RandomColorHex()
        ColorOfLine1=color1.mainI()
        ColorOfLine2=color2.mainI()
        
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
    Color=RandomColorHex()
    Answer=Color.mainI()
    print(f"Your random hex code is: {Answer}")
    print(f"Your random hex code (static version) is: {RandomColorHex.main()}")
    Color.Credits()
    Color.Help()
