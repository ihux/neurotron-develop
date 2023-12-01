"""
neurotron.cluster: neural cluster computing
   classes:
       Cluster   cluster of Neurotrons
       Collab    parameters for collaboration terminal
       Excite    parameters for excitation terminal
       Predict   parameters for prediction terminal
       Terminal  neurotron terminal
       Token     wrapper for token dicts
"""

import neurotron.cluster.cluster
import neurotron.cluster.setup
import neurotron.cluster.terminal

#===============================================================================
# classes
#===============================================================================

Cluster = cluster.Cluster
Collab = setup.Collab
Excite = setup.Excite
Predict = setup.Predict
Terminal = terminal.Terminal
Token = cluster.Token
