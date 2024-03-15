import cytoflow
import numpy

f = r"1.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A", "B4-A" : "B4-A"})
experiment = import_op.apply()
experiment
# print(experiment)

threshold_op = cytoflow.ThresholdOp(name = "Threshold", channel = "R1-A", threshold = 2000)

threshold_op.default_view(scale = "logicle", interactive = True).plot(experiment)

experiment_threshold = threshold_op.apply(experiment)
# print(experiment_threshold.data.groupby('Threshold').size())
experiment_threshold = experiment_threshold.query("Threshold")

density_gate_op = cytoflow.DensityGateOp(name = "DensityGate", xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle", keep = 0.5)

density_gate_op.estimate(experiment_threshold)

density_gate_op.default_view().plot(experiment_threshold)

experiment_density_gate = density_gate_op.apply(experiment_threshold)
experiment_density_gate = experiment_density_gate.query("DensityGate")

flow_peaks_op = cytoflow.FlowPeaksOp(name = "FlowPeaks", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, h0 = 3)

flow_peaks_op.estimate(experiment_density_gate)

flow_peaks_op.default_view(density = True).plot(experiment_density_gate)

experiment_flow_peaks = flow_peaks_op.apply(experiment_density_gate)
count = experiment_flow_peaks[["FlowPeaks"]].groupby(by = experiment_flow_peaks["FlowPeaks"]).count()
count
# print(count)

flow_peaks_op.default_view().plot(experiment_flow_peaks)

# Ordenamos los datos
sorted_data = numpy.sort(experiment_flow_peaks["B4-A"])
# Obtenemos el número total de datos
total_number_data = len(sorted_data)
# Si el número de datos es par
if total_number_data % 2 == 0:
    median_fluorescence_intensity = (sorted_data[total_number_data // 2 - 1] + sorted_data[total_number_data // 2]) / 2
# Si el número de datos es impar
else:
    median_fluorescence_intensity = sorted_data[total_number_data // 2]
print(f"                          Number of events: {experiment_flow_peaks.data.shape[0]}")
print(f"The Median Fluorescence Intensity (MFI) is: {median_fluorescence_intensity}")