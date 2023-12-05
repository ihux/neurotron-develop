"""
module neurotron.cluster.toy
    class Toy  # to provide toy stuff for neurotron cluster
"""

from neurotron.cluster.token import Token, Text

#===============================================================================
# class Toy
#===============================================================================

class Toy:
    """
    >>> Toy()
    Toy('Sarah')
    >>> Toy('Mary')
    Toy('Mary')
    >>> Toy('Tiny')  # Tiny Shakespear
    Toy('Tiny')

    see also: toy.sarah, toy.mary, toy.tiny, ...
    """
    def __init__(self,tag='Sarah'):
        self.tag = tag
        if tag.lower() == 'sarah': self.sarah()
        if tag.lower() == 'mary':  self.mary()
        if tag.lower() == 'tiny':  self.tiny()

    def __str__(self):
        return "Toy('%s')" % self.tag

    def sarah(self):
       self.shape = (1,3,1,3)
       self.token = Token({
           'Sarah':[1,1,0,1,1,1,0,1,0,1],
           'loves':[0,1,1,1,0,1,1,0,1,1],
           'music':[1,1,1,0,0,1,0,1,1,1],
           '.':    [0,0,0,0,0,0,0,0,0,0],
           })

    def mary(self):
        self.shape = (2,9,4,3)
        self.token = Token({
            'Mary': [1,0,0,0,0,0,0,1,1],
            'John': [0,1,0,0,0,0,0,1,1],
            'Lisa': [1,0,0,0,0,0,1,1,0],
            'Andy': [0,1,0,0,0,0,1,1,0],
            'likes':[0,0,1,0,0,0,0,1,1],
            'to':   [0,0,0,1,0,0,0,1,1],
            'sing': [0,0,0,0,1,0,0,1,1],
            'dance':[0,0,0,0,1,0,1,1,0],
            'hike': [0,0,0,0,0,1,0,1,1],
            'paint':[0,0,0,0,0,1,1,1,0],
            'climb':[0,0,0,0,1,0,1,1,0],
            '.':    [0,0,0,0,0,0,1,1,1],
            })

    def tiny(self):
        """
        Tiny Shakespear:
        >>> toy = Toy('Tiny'); print(toy)
        Toy('Tiny')
        >>> toy.shape
        (2, 8, 4, 3)
        >>> toy.raw[:45]
        'First Citizen: We are accounted poor citizens'
        >>> toy.text
        Text(67,8,['First Ci','tizen: W','e are ac',...])
        >>> Text(Toy('Tiny').raw,8)
        Text(67,8,['First Ci','tizen: W','e are ac',...])
        """
        self.shape = (2,8,4,3)
        self.bits = 3
        self.raw = Text().refine(tiny_shakespear)
        self.text = Text(self.raw,8)

    def __repr__(self):
        return self.__str__()

#===============================================================================
# Tiny Shakespear
#===============================================================================

tiny_shakespear = \
"""
First Citizen:
We are accounted poor citizens, the patricians good.
What authority surfeits on would relieve us: if they
would yield us but the superfluity, while it were
wholesome, we might guess they relieved us humanely;
but they think we are too dear: the leanness that
afflicts us, the object of our misery, is as an
inventory to particularise their abundance; our
sufferance is a gain to them Let us revenge this with
our pikes, ere we become rakes: for the gods know I
speak this in hunger for bread, not in thirst for revenge.
"""

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
