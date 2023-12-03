"""
module neurotron.cluster.toy
    class Toy  # to provide toy stuff for neurotron cluster
"""

#===============================================================================
# class Toy
#===============================================================================

class Toy:
    """
    >>> Toy('Mary')
    Toy('Mary')
    """
    def __init__(self,tag):
        self.tag = tag

    def __str__(self):
        return "Toy('%s')" % self.tag

    def __repr__(self):
        return self.__str__()

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
