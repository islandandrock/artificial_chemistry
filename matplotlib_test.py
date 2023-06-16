import matplotlib.pyplot
import time
import random
import numpy

rates = numpy.array([0])
results = numpy.array([50])
hl, = matplotlib.pyplot.plot(rates, results, marker='o')
h2, = matplotlib.pyplot.plot(rates, results, marker='o')
#matplotlib.pyplot.ion()
matplotlib.pyplot.xlim(0, 100)
matplotlib.pyplot.ylim(0, 100)
matplotlib.pyplot.xlabel("Learning Rate")
matplotlib.pyplot.ylabel("Accuracy")


for i in range(100):
    matplotlib.pyplot.pause(0.01)
    hl.set_xdata(numpy.append(hl.get_xdata(), [i+1]))
    hl.set_ydata(numpy.append(hl.get_ydata(), [random.randint(1,100)]))
    h2.set_xdata(numpy.append(h2.get_xdata(), [i+1]))
    h2.set_ydata(numpy.append(h2.get_ydata(), [random.randint(1,100)]))
    matplotlib.pyplot.draw()


matplotlib.pyplot.show()
