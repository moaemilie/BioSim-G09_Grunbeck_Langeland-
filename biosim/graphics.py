# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.histograms import Age_hist, Weight_hist, Fitness_hist
import matplotlib.pyplot as plt
import numpy as np


class Graphics:
    def __init__(self, ymax_animals=None, cmax_animals=None):
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals

        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(2, 3, 1)
        self.ax_line = self.fig.add_subplot(2, 3, 3)
        self.ax3 = self.fig.add_subplot(2, 3, 4)
        self.ax4 = self.fig.add_subplot(2, 3, 5)
        self.ax5 = self.fig.add_subplot(2, 3, 6)
        self.ax_count = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])

    def setup(self, num_years):

        self.ax_line.set_xlim(0, num_years)
        if self.ymax_animals is None:
            self.ax_line.set_ylim(0, auto=True)
        else:
            self.ax_line.set_ylim(0, self.ymax_animals)

        line_herb = self.ax_line.plot(np.arange(num_years),
                                      np.full(num_years, np.nan), 'b-')[0]
        line_carn = self.ax_line.plot(np.arange(num_years),
                                      np.full(num_years, np.nan), 'r-')[0]

        self.ax_count.axis('off')
        template = 'Count: {:5d}'
        txt = self.ax_count.text(0.5, 0.5, template.format(0),
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=self.ax_count.transAxes)

        #plt.pause(0.01)

        #input('Press ENTER to begin counting')

        # for k in range(num_years):
        #     txt.set_text(template.format(k))
        #     plt.pause(0.1)

        #plt.show()


    def line_plot(self):
        num_years = 100

        for year in range(num_years):
            ydata_h = line_herb.get_ydata()
            ydata_c = line_carn.get_ydata()
            ydata_h[year] = np.random.random()
            ydata_c[year] = np.random.random()
            line_herb.set_ydata(ydata_h)
            line_carn.set_ydata(ydata_c)
            self.fig.canvas.flush_events()
            plt.pause(1e-6)



    # def mapping(self):
    #
    #
    def logger(self):



if __name__ == '__main__':
    grafikk = Graphics(ymax_animals=1, cmax_animals={'Herbivore': 50, 'Carnivore': 20})
    grafikk.setup(100)
    grafikk.line_plot()
