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

    def RandomHex(self):
        self.RandomHexCode=[] #Resets the color
        Alphabet = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(6):
            LetterOrNumber=secrets.randbelow(2) #Will decide if it will be a letter or number
            if LetterOrNumber==0:
                Choice=str(secrets.randbelow(10))
            else:
                Choice=secrets.choice(Alphabet)
            self.RandomHexCode.append(Choice)

    def mainI(self): #Instance mode of main
        self.RandomHex()
        self.RandomHexCode.insert(0,'#')
        return ''.join(self.RandomHexCode)

    @staticmethod
    def main(): #Made for if you just wanna do a one off color
        RC=RandomColorHex()
        RC.RandomHex()
        RC.RandomHexCode.insert(0,'#')
        return ''.join(RC.RandomHexCode)

    @staticmethod
    def Credits():
        print("Made by Nathan Honn, randomhexman@gmail.com")

    @staticmethod
    def Help():
        print("""
        import matplotlib.pyplot as plt
        import random_color_hex as RCH
        
        Numbers=list(range(-6,7))
        Line1=[x**2 for x in Numbers]
        Line2=[x**3 for x in Numbers]
        
        #For a one off random color:
        #ColorOfLine1=RCH.main()
        #ColorOfLine2=RCH.main()
        
        #For an instance random color (to be reused later):
        color1, color2 = RCH(), RCH()
        ColorOfLine1=color1.mainI()
        ColorOfLine2=color2.mainI()
        
        plt.plot(Numbers,Line1,color=ColorOfLine1,label="x²")
        plt.plot(Numbers,Line2,color=ColorOfLine2,label="x³")
        plt.title("Graph of X² v X³")
        plt.legend()
        plt.show()
        """)

if __name__=="__main__":
    Color=RandomColorHex()
    Answer=Color.mainI()
    print(f"Your random hex code is: {Answer}")
    print(f"Your random hex code (static version) is: {RandomColorHex.main()}")
    Color.Credits()
    Color.Help()