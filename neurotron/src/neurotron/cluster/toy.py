"""
module neurotron.cluster.toy
    class Toy  # to provide toy stuff for neurotron cluster
"""

from neurotron.cluster.token import Token, Text
from neurotron.shakespear import shakespear

#===============================================================================
# class Toy
#===============================================================================

class Toy:
    """
    >>> Toy()
    Toy('Sarah')
    >>> Toy('Mary')
    Toy('Mary')
    >>> Toy('Tiny',8)  # Tiny Shakespear
    Toy('Tiny')

    see also: toy.sarah, toy.mary, toy.tiny, ...
    """
    def __init__(self,tag='Sarah',n=None):
        self.tag = tag
        self.train = None
        if tag.lower() == 'sarah': self.sarah()
        if tag.lower() == 'mary':  self.mary()
        if tag.lower() == 'tiny':  self.tiny(n)

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
        self.shape = (2,9,6,3)
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
            'climb':[0,0,0,0,1,1,0,1,0],
            '.':    [0,0,0,0,0,0,1,1,1],
            })
        self.train = ['Mary likes to sing','John likes to dance']

    def tiny(self,n):
        """
        Tiny Shakespear:
        >>> toy = Toy('Tiny'); print(toy)
        Toy('Tiny')
        >>> toy.shape
        (2, 8, 4, 3)
        >>> toy.raw[:44]
        'First Citizen: Before we proceed any further'
        >>> toy.text
        Text(139424,8,['First Ci','tizen: B','efore we',...])
        >>> Text(Toy('Tiny').raw,8)
        Text(139424,8,['First Ci','tizen: B','efore we',...])
        """
        n = n if n is not None else 8
        self.shape = (2,8,4,3)
        self.bits = 3
        self.raw = Text().refine(shakespear)
        self.text = Text(self.raw,n)

    def __repr__(self):
        return self.__str__()

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
