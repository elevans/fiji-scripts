#@ UIService ui
#@ PlotService ps

from org.scijava.plot import LineStyle, MarkerStyle
from org.scijava.util import ColorRGB

# create plot
plot = ps.newXYPlot()
plot.setTitle("Test")

# add data to the plot
x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y = [0.3, 0.0, 0.8, 0.4, 0.3, 0.7]
series = plot.addXYSeries()
series.setLabel("Series A")
series.setValues(x, y)

# set the plot style to scatter
series.setStyle(ps.newSeriesStyle(
    ColorRGB("blue"),
    LineStyle.NONE,
    MarkerStyle.CIRCLE))

# show the plot
ui.show(plot)
