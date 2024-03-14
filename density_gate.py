import cytoflow

f = r"1.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A"})
experiment = import_op.apply()
experiment
# print(experiment)

density_gate_op = cytoflow.DensityGateOp(name = "DensityGate", xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle", keep = 0.5)

density_gate_op.estimate(experiment)

density_gate_op.default_view().plot(experiment)

experiment2 = density_gate_op.apply(experiment)