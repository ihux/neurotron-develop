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
        >>> toy.raw[:44]
        'First Citizen: Before we proceed any further'
        >>> toy.text
        Text(139424,8,['First Ci','tizen: B','efore we',...])
        >>> Text(Toy('Tiny').raw,8)
        Text(139424,8,['First Ci','tizen: B','efore we',...])
        """
        self.shape = (2,8,4,3)
        self.bits = 3
        self.raw = Text().refine(shakespear)
        self.text = Text(self.raw,8)

    def __repr__(self):
        return self.__str__()

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
