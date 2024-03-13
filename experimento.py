import cytoflow
# import pandas
# import matplotlib
import numpy

f = r'C:\Users\pract\Documents\Practicas\4.fcs'
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {'R1-A' : 'R1-A', 'B8-A' : 'B8-A'})
experiment = import_op.apply()

r2d = cytoflow.Range2DOp(name = "Test", xchannel = "R1-A", ychannel = "B8-A")

r2d.default_view(xscale = "logicle", yscale = "logicle", interactive = True).plot(experiment)
cytoflow.DensityView(xchannel = 'R1-A', xscale = 'logicle', ychannel = 'B8-A', yscale = 'logicle').plot(experiment, gridsize = 100, smoothed = True)

kmeans = cytoflow.KMeansOp(name = "KMeans", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, num_clusters = 5)
kmeans.estimate(experiment)
experiment_kmeans = kmeans.apply(experiment)
kmeans.default_view().plot(experiment_kmeans)

gauss = cytoflow.GaussianMixtureOp(name = "Gauss", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, num_components = 2)

gauss.estimate(experiment)
experiment_gauss = gauss.apply(experiment)

gauss.default_view().plot(experiment_gauss, alpha = 0.1)

new_experiment = cytoflow.ImportOp(tubes = [cytoflow.Tube(file = f)]).apply()
new_experiment
print(new_experiment)

flow_peaks = cytoflow.FlowPeaksOp(name = "FP", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, h0 = 0.8)

flow_peaks.estimate(new_experiment)
new_experiment2 = flow_peaks.apply(new_experiment)
flow_peaks.default_view().plot(new_experiment2)
cytoflow.ScatterplotView(xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle", huefacet = "FP").plot(new_experiment2)

new_experiment2.data
print(new_experiment2.data)

count = new_experiment2[["FP"]].groupby(by = new_experiment2["FP"]).count()
count
print(count)

umbral = abs(new_experiment2["R1-A"].max()/new_experiment2["R1-A"].min())
umbral
print(umbral)

indice = new_experiment2["R1-A"].loc[new_experiment2["R1-A"] < umbral].index
indice
print(indice)

cluster = new_experiment2[["FP"]].drop(indice).groupby(by = new_experiment2["FP"].drop(indice)).count()
cluster
print(cluster)

pcluster = cluster.index[numpy.argmax(cluster.to_numpy())]
pcluster
print(pcluster)

bead_cluster = new_experiment2[new_experiment2['FP'] == pcluster]
bead_cluster
print(bead_cluster)

media = bead_cluster['B4-A'].mean()
media
print(media)

stats = bead_cluster["B4-A"].describe()
stats
print(stats)

full_stats = bead_cluster.describe()
full_stats
print(full_stats)