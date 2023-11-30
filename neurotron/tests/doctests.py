# tests.py: run all relevant doctests

import doctest
import neurotron
#import neurotron.math.attribute
#import neurotron.math.matrix
#import neurotron.cluster.setup
from neurotron.ansi import Ansi

err = 0
#err += doctest.testmod(neurotron.neurotron, verbose=False).failed
#err += doctest.testmod(neurotron.cluster.setup, verbose=False).failed
err += doctest.testmod(neurotron.math.attribute, verbose=False).failed
err += doctest.testmod(neurotron.math.matrix, verbose=False).failed
err += doctest.testmod(neurotron.math.matfun, verbose=False).failed
#err += doctest.testmod(neurotron.math.field, verbose=False).failed
#err += doctest.testmod(neurotron.math, verbose=False).failed



if err:
   print(Ansi.R+'doctests: total fails:'+Ansi.N,err)
else:
   print(Ansi.G+'all doctests: PASSED'+Ansi.N)
