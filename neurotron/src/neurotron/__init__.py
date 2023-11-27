"""
neurotron: building blocks for neural computing circuits
   classes:
       Attribute base class to support compact attribute access
       Matrix    matrix class
       Field     field class (matrix of matrices)
       Collab    parameters for collaboration terminal

   functions:
       isa       is object a given class instance (same as isinstance)
"""

import neurotron.matrix
import neurotron.cluster.setup

#===============================================================================
# class attribute setup
#===============================================================================

Attribute = neurotron.matrix.Attribute
Collab = neurotron.cluster.setup.Collab
Matrix = neurotron.matrix.Matrix
Field  = neurotron.matrix.Field

#===============================================================================
# function attribute setup
#===============================================================================

isa = isinstance
