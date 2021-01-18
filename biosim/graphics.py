# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.histograms import Age_hist, Weight_hist, Fitness_hist
import matplotlib.pyplot as plt
import numpy as np
import textwrap


class Graphics:
    def __init__(self, ymax_animals=None, cmax_animals=None, hist_specs=None, sim_island=None):
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.island = sim_island

        self.fig = plt.figure()
        self.ax_map = self.fig.add_subplot(3, 3, 1)
        self.ax_line = self.fig.add_subplot(3, 3, 3)
        self.ax_herb_dist = self.fig.add_subplot(3, 3, 4)
        self.ax_carn_dist = self.fig.add_subplot(3, 3, 6)
        self.ax_hist_fit = self.fig.add_subplot(3, 3, 7)
        self.ax_hist_age = self.fig.add_subplot(3, 3, 8)
        self.ax_hist_weight = self.fig.add_subplot(3, 3, 9)
        self.ax_count = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])
        self.count_template = '[Year: {:5d}]'
        self.ax_count_form = self.ax_count.text(0.5, 0.5, self.count_template.format(0),
                                 horizontalalignment='center',
                                 verticalalignment='center',
                                 transform=self.ax_count.transAxes)
        self.ax_count.axis('off')
        self.fig.tight_layout()

    def setup(self, num_years):

        font = 9

        self.ax_line.set_title('Animal count', fontsize=font)
        self.ax_line.set_xlim(0, num_years)
        if self.ymax_animals is None:
            self.ax_line.set_ylim(0, auto=True)
        else:
            self.ax_line.set_ylim(0, self.ymax_animals)

        self.ax_map.set_title('Island', fontsize=font)

        self.ax_hist_fit.set_title('Fitness', fontsize=font)

        self.ax_hist_age.set_title('Age', fontsize=font)

        self.ax_hist_weight.set_title('Weight', fontsize=font)

        self.ax_herb_dist.set_title('Herbivore distribution', fontsize=font)

        self.ax_carn_dist.set_title('Carnivore distribution', fontsize=font)

        self.line_herb = self.ax_line.plot(np.arange(num_years),
                                           np.full(num_years, np.nan), 'b-')[0]
        self.line_carn = self.ax_line.plot(np.arange(num_years),
                                           np.full(num_years, np.nan), 'r-')[0]
        if self.hist_specs is None:
            self.hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05}, 'age': {'max': 60.0, 'delta': 2},
                               'weight': {'max': 60, 'delta': 2}}

    def counter(self, year):

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

    def hist_plot(self, fitness_data, age_data, weight_data):
        self.ax_hist_fit.clear()
        self.ax_hist_age.clear()
        self.ax_hist_weight.clear()
        self.ax_hist_fit.hist(fitness_data[0], bins=round(self.hist_specs['fitness']['max'] / self.hist_specs['fitness']['delta']), histtype=u'step')
        self.ax_hist_age.hist(age_data[0], bins=round(self.hist_specs['age']['max'] / self.hist_specs['age']['delta']), histtype=u'step')
        self.ax_hist_weight.hist(weight_data[0], bins=round(self.hist_specs['age']['max'] / self.hist_specs['weight']['delta']), histtype=u'step')
        plt.pause(1e-6)

    def map_plot(self, island_map):

        island_map = textwrap.dedent(island_map)

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]

        self.ax_map.imshow(map_rgb)

        self.ax_map.set_xticks(np.arange(1, len(map_rgb[0]), 3))
        self.ax_map.set_xticklabels(np.arange(1, len(map_rgb[0]), 3), fontsize=7)
        self.ax_map.set_yticks(np.arange(1, len(map_rgb), 3))
        self.ax_map.set_yticklabels(np.arange(1, len(map_rgb), 3), fontsize=7)

        axlg = self.fig.add_axes([0.32, 0.75, 0.05, 0.25])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes, fontsize=7)

    def dist_plot(self):
        herb_dist = [[self.island.island_map[row][col].get_num_herb() for col in range(self.island.map_columns)] for row in range(self.island.map_rows)]
        carn_dist = [[self.island.island_map[row][col].get_num_carn() for col in range(self.island.map_columns)] for row in range(self.island.map_rows)]
        self.ax_herb_dist.imshow(herb_dist, cmap='viridis')
        self.ax_carn_dist.imshow(carn_dist, cmap='viridis')
        colorbar.ColorbarBase(self.ax_herb_dist, cmap='viridis', format='%.1f')



        # def mapping(self):
    #
    #
    # def logger(self):


# if __name__ == '__main__':
#     grafikk = Graphics(ymax_animals=1, cmax_animals={'Herbivore': 50, 'Carnivore': 20})
#     grafikk.setup(100)
#     grafikk.line_plot()
