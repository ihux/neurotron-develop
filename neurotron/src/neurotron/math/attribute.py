"""
module attribute:
- class Attribute      # easy get/set of object attributes

Attribute methods:
- get
- set
"""

#===============================================================================
# class Attribute
#===============================================================================

class Attribute:
    def get(self,tags):
        """
        >>> o = Attribute()
        >>> o.set('A,B,C',(1,2,3))
        >>> o.get('A')
        1
        >>> o.get('A,B,C')
        (1, 2, 3)
        """
        out = ()
        while True:
            idx = tags.find(',')
            if idx < 0:
                tag = tags;  tags = ''
            else:
                tag = tags[:idx]
                tags = tags[idx+1:]
            arg = getattr(self,tag,None)
            out = out + (arg,)
            if tags == '':
                return out if len(out) > 1 else out[0]

    def set(self,tags,args):
        """
        >>> o = Attribute()
        >>> o.set('A,B,C',(7,8,9))
        >>> o.get('A,B,C')
        (7, 8, 9)
        >>> o.set('X',((5,2),))
        >>> o.get('X')
        (5, 2)
        """
        if not isinstance(args,tuple):
            args = (args,)
        for k in range(len(args)):
            idx = tags.find(',')
            if idx < 0:
                tag = tags;  tags = ''
            else:
                tag = tags[:idx]
                tags = tags[idx+1:]
            setattr(self,tag,args[k])
            if tags == '':
                if len(args) > k+1:
                    raise Exception('too many values provided by arg2 tuple')
                return

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
