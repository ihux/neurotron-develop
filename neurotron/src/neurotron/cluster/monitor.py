"""
module neurotron.cluster.cluster
    class Cluster  # simulate a cluster of Neurotrons
    class Token    # wrapper for token dicts
"""

from neurotron.cluster.cluster import Cluster

#===========================================================================
# class Record
#===========================================================================

class Record:
    """
    >>> cells=Cluster(2,7,2,5)
    >>> cells.U[0]=cells.X[0]=1
    >>> rec = Record(cells)
    >>> rec(cells)
    >>> rec.pattern()
    '|UX|-|-|-|-|-|-|-|-|-|-|-|-|-|'
    """
    def __init__(self,cells):
        self.n = len(cells)
        self.clear()

    def clear(self):                        # clear recorder
        n = self.n
        self.u = [[] for k in range(n)];
        self.q = [[] for k in range(n)];
        self.x = [[] for k in range(n)];
        self.l = [[] for k in range(n)];
        self.b = [[] for k in range(n)];
        self.d = [[] for k in range(n)];
        self.y = [[] for k in range(n)];
        self.s = [[] for k in range(n)];

    def __call__(self,cells):               # record state of cells
        for k in cells.range():
            cell = cells[k]
            self.u[k].append(cell.u.out())
            self.q[k].append(cell.q.out())
            self.x[k].append(cell.x.out())
            self.l[k].append(cell.l.out())
            self.b[k].append(cell.b.out())
            self.d[k].append(cell.d.out())
            self.y[k].append(cell.y.out())
            self.s[k].append(cell.s.out())

            #pdelta,ndelta = cell.predict.synapses.delta
            pdelta,ndelta = cell.delta()
            if pdelta == 0 and ndelta == 0:
                self.l[k][-1] = 0

    def log(self,cells,y,tag=None):
        print('\nSummary:',tag)
        print("   u:",self.u)
        print("   q:",self.q)
        print("   x:",self.x)
        print("   l:",self.l)
        print("   b:",self.b)
        print("   d:",self.d)
        print("   y:",self.y)
        print("   s:",self.s)
        nc,nf = cells[0].sizes
        print("y = [c,f]:",[y[:nc],y[nc:nc+nf]])

    def pattern(self):
        m = len(self.u);  n = len(self.u[0])
        str = '';
        for i in range(m):
            line = '';  sep = ''
            for j in range(n):
                chunk = ''
                if self.u[i][j]: chunk += 'U'
                if self.q[i][j]: chunk += 'Q'
                if self.x[i][j]: chunk += 'X'
                if self.l[i][j]: chunk += 'L'
                if self.d[i][j]: chunk += 'D'
                if self.b[i][j]: chunk += 'B'
                if self.y[i][j]: chunk += 'Y'
                if self.s[i][j]: chunk += 'S'
                if chunk == '':
                    line += '-'
                else:
                    line += sep + chunk;  sep = ','
            str += '|' + line;
        return str + '|'

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
