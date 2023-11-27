# tests.py: run all relevant doctests

import doctest
import neurotron.neurotron
import neurotron.matrix
import neurotron.cluster.setup

def failed(msg):
    chunks = msg.split(',')
    fail = chunks[0];  prefix = 'failed='
    idx = fail.find(prefix) + len(prefix)
    return int(fail[idx:])

#doctest.testmod(neurotron.neurotron, verbose=True)
doctest.testmod(neurotron.cluster.setup, verbose=False)

result = doctest.testmod(neurotron.matrix, verbose=False)
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@ msg:',result,type(result))
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@ failed:',result.failed)
