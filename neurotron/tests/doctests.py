# tests.py: run all relevant doctests

import doctest
import neurotron
from neurotron.ansi import Ansi

err = 0
err += doctest.testmod(neurotron.math.helper, verbose=False).failed
err += doctest.testmod(neurotron.math.attribute, verbose=False).failed
err += doctest.testmod(neurotron.math.matrix, verbose=False).failed
err += doctest.testmod(neurotron.math.matfun, verbose=False).failed
err += doctest.testmod(neurotron.math.field, verbose=False).failed
err += doctest.testmod(neurotron, verbose=False).failed

err += doctest.testmod(neurotron.cluster.setup, verbose=False).failed
err += doctest.testmod(neurotron.cluster.terminal, verbose=False).failed
err += doctest.testmod(neurotron.cluster.cluster, verbose=False).failed

err += doctest.testmod(neurotron.neurotron, verbose=False).failed

err += doctest.testmod(neurotron.cluster.monitor, verbose=False).failed
err += doctest.testmod(neurotron.cluster.toy).failed

if err:
   print(Ansi.R+'doctests: total fails:'+Ansi.N,err)
else:
   print(Ansi.G+'all doctests: PASSED'+Ansi.N)
