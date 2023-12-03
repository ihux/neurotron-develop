"""
neurotron.cluster: neural cluster computing
    classes:
        Cluster     cluster of Neurotrons
        Collab      parameters for collaboration terminal
        Excite      parameters for excitation terminal
        Predict     parameters for prediction terminal
        Terminal    neurotron terminal
        Token       wrapper for token dicts
        SynapseErr  Synapse Exception
        Toy         creating toy stuff

    functions:
        follow      following matrix during matrix iteration
"""

import neurotron.cluster.cluster
import neurotron.cluster.setup
import neurotron.cluster.terminal
import neurotron.cluster.monitor
import neurotron.cluster.toy

#===============================================================================
# classes
#===============================================================================

Collab = setup.Collab
Excite = setup.Excite
Predict = setup.Predict
Terminal = terminal.Terminal

Cluster = cluster.Cluster
Cell = cluster.Cell
Token = cluster.Token
SynapseErr = cluster.SynapseErr
Toy = toy.Toy

Record = monitor.Record

#===============================================================================
# functions
#===============================================================================

follow = cluster.follow
