"""
module neurotron.cluster.toy
    class Toy  # to provide toy stuff for neurotron cluster
"""

from neurotron.cluster.cells import Token

#===============================================================================
# class Toy
#===============================================================================

class Toy:
    """
    >>> Toy()
    Toy('Sarah')
    >>> Toy('Mary')
    Toy('Mary')
    """
    def __init__(self,tag='Sarah'):
        self.tag = tag
        if tag.lower() == 'sarah': self._sarah()
        if tag.lower() == 'mary':  self._mary()

    def __str__(self):
        return "Toy('%s')" % self.tag

    def _sarah(self):
       self.shape = (1,3,1,3)
       self.token = Token({
           'Sarah':[1,1,0,1,1,1,0,1,0,1],
           'loves':[0,1,1,1,0,1,1,0,1,1],
           'music':[1,1,1,0,0,1,0,1,1,1],
           '.':    [0,0,0,0,0,0,0,0,0,0],
           })

    def _mary(self):
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

    def __repr__(self):
        return self.__str__()

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
