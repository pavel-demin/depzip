import sys

from PySide6.QtWidgets import QMainWindow, QApplication

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

import numpy as np

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dpi = app.primaryScreen().logicalDotsPerInch()
    rcParams["figure.dpi"] = dpi

    figure = Figure(constrained_layout=True)
    canvas = FigureCanvas(figure)

    ax = figure.add_subplot()

    t = np.linspace(0.0, 2.0 * np.pi, 1000)
    x = np.sin(3.0 * t)
    y = np.sin(4.0 * t)

    ax.plot(x, y)
    ax.grid()

    w = QMainWindow()
    w.setCentralWidget(canvas)
    w.show()

    app.exec()
