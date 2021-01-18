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
        self.count_template = 'Count: {:5d}'
        self.ax_count_form = self.ax_count.text(0.5, 0.5, self.count_template.format(0),
                                 horizontalalignment='center',
                                 verticalalignment='center',
                                 transform=self.ax_count.transAxes)
        self.ax_count.axis('off')

    def setup(self, num_years):

        self.ax_line.set_xlim(0, num_years)
        if self.ymax_animals is None:
            self.ax_line.set_ylim(0, auto=True)
        else:
            self.ax_line.set_ylim(0, self.ymax_animals)

        self.line_herb = self.ax_line.plot(np.arange(num_years),
                                           np.full(num_years, np.nan), 'b-')[0]
        self.line_carn = self.ax_line.plot(np.arange(num_years),
                                           np.full(num_years, np.nan), 'r-')[0]


    def counter(self, year):

        #plt.pause(0.01)

        self.ax_count_form.set_text(self.count_template.format(year))
        plt.pause(0.1)



    def line_plot(self, year, num_herb, num_carn):

        ydata_h = self.line_herb.get_ydata()
        ydata_c = self.line_carn.get_ydata()
        ydata_h[year-1] = num_herb
        ydata_c[year-1] = num_carn
        self.line_herb.set_ydata(ydata_h)
        self.line_carn.set_ydata(ydata_c)
        self.fig.canvas.flush_events()
        plt.pause(1e-6)

    # def mapping(self):
    #
    #
    # def logger(self):


if __name__ == '__main__':
    grafikk = Graphics(ymax_animals=1, cmax_animals={'Herbivore': 50, 'Carnivore': 20})
    grafikk.setup(100)
    grafikk.line_plot()
