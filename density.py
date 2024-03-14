import cytoflow

f = r"1.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A"})
experiment = import_op.apply()
experiment
# print(experiment)

density_gate = cytoflow.DensityGateOp(name = "Density", xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle", keep = 0.5)

density_gate.estimate(experiment)

density_gate.default_view().plot(experiment)

experiment2 = density_gate.apply(experiment)