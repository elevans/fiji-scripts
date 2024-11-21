from ij.gui import Plot
from java.awt import Color

# create x and y data
x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y = [0.3, 0.0, 0.8, 0.4, 0.3, 0.7]

# initialize the plot
p = Plot("Scatter plot", "x", "y")

# add scatter plot data here
p.setColor(Color.BLUE)
p.addPoints(x, y, Plot.CIRCLE)
p.draw()

# display the plot
p.show()
