import cytoflow

f = r'C:\Users\pract\Documents\4.fcs'

tube = cytoflow.Tube(file = f)

importOp = cytoflow.ImportOp(tubes = [tube], channels = {'R1-A' : 'R1-A', 'B8-A' : 'B8-A'})

experiment = importOp.apply()
print(experiment)

# histogram = cytoflow.HistogramView()
# histogram.channel = 'Y2-A'
# histogram.plot(experiment)

# histogram = cytoflow.HistogramView(channel = 'Y2-A', scale = 'logicle')
# histogram.plot(experiment)

# cytoflow.HistogramView(channel = 'Y2-A', scale = 'logicle', yfacet = 'Dox').plot(experiment)

# cytoflow.HistogramView(channel = 'Y2-A', scale = 'logicle', huefacet = 'Dox').plot(experiment)