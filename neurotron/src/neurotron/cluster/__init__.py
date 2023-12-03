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

    functions:
        follow      following matrix during matrix iteration
"""

import neurotron.cluster.cluster
import neurotron.cluster.setup
import neurotron.cluster.terminal
import neurotron.cluster.monitor

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

Record = monitor.Record

#===============================================================================
# functions
#===============================================================================

follow = cluster.follow
