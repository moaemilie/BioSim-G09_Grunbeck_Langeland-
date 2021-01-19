# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import matplotlib.pyplot as plt
import numpy as np
import textwrap


class Graphics:
    def __init__(self, ymax_animals=None, cmax_animals=None, hist_specs=None, sim_island=None,
                 img_base=None, img_fmt=None):
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        if self.cmax_animals is None:
            self.cmax_animals = {'Herbivore': 250, 'Carnivore': 150}
        self.hist_specs = hist_specs
        self.island = sim_island
        self.img_no = 0
        self.img_base = img_base
        if self.img_base is None:
            self.img_base = '..data'
        self.img_fmt = img_fmt

        self.fig = plt.figure(figsize=(8, 6))
        self.plot_map = self.fig.add_subplot(3, 3, 1)
        self.plot_line = self.fig.add_subplot(3, 3, 3)
        self.plot_herb_dist = self.fig.add_subplot(3, 3, 4)
        self.plot_carn_dist = self.fig.add_subplot(3, 3, 6)
        self.plot_hist_fit = self.fig.add_subplot(3, 3, 7)
        self.plot_hist_age = self.fig.add_subplot(3, 3, 8)
        self.plot_hist_weight = self.fig.add_subplot(3, 3, 9)
        self.add_col_bar = False
        self.plot_count = self.fig.add_axes([0.4, 0.56, 0.2, 0.2])
        self.count_template = 'Year: {:5d}'
        self.count_format = self.plot_count.text(0.5, 0.5, self.count_template.format(0),
                                                 horizontalalignment='center',
                                                 verticalalignment='center',
                                                 transform=self.plot_count.transAxes,
                                                 fontsize=14)

    def setup(self, num_years):

        font = 9
        self.plot_count.axis('off')
        self.fig.tight_layout()
        self.plot_line.set_xlim(0, num_years)
        if self.ymax_animals is None:
            self.ymax_animals = True
        else:
            self.plot_line.set_ylim(0, self.ymax_animals)

        self.plot_line.set_title('Animal count', fontsize=font)
        self.plot_map.set_title('Island', fontsize=font)

        title_fit = self.fig.add_axes([0.16, 0.34, 0.05, 0.25])
        title_fit.axis('off')
        title_fit.text(0, 0., 'Fitness', fontsize=9)

        title_age = self.fig.add_axes([0.5, 0.34, 0.05, 0.25])
        title_age.axis('off')
        title_age.text(0, 0, 'Age', fontsize=9)

        title_weight = self.fig.add_axes([0.815, 0.34, 0.05, 0.25])
        title_weight.axis('off')
        title_weight.text(0, 0, 'Weight', fontsize=9)

        self.plot_herb_dist.set_title('Herbivore distribution', fontsize=font)
        self.plot_herb_dist.axis('off')
        self.plot_carn_dist.set_title('Carnivore distribution', fontsize=font)
        self.plot_carn_dist.axis('off')

        self.line_herb = self.plot_line.plot(np.arange(num_years),
                                             np.full(num_years, np.nan), 'b-')[0]
        self.line_carn = self.plot_line.plot(np.arange(num_years),
                                             np.full(num_years, np.nan), 'r-')[0]

        if self.hist_specs is None:
            self.hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05}, 'age': {'max': 60.0, 'delta': 2},
                               'weight': {'max': 60, 'delta': 2}}

    def counter(self, year):

        self.count_format.set_text(self.count_template.format(year))
        plt.pause(0.1)

    def line_plot(self, year, num_herb, num_carn):

        if self.ymax_animals == True:
            self.plot_line.set_ylim(0, max(num_herb + 1000, num_carn + 1000))
        ydata_h = self.line_herb.get_ydata()
        ydata_c = self.line_carn.get_ydata()
        ydata_h[year - 1] = num_herb
        ydata_c[year - 1] = num_carn
        self.line_herb.set_ydata(ydata_h)
        self.line_carn.set_ydata(ydata_c)
        self.fig.canvas.flush_events()
        plt.pause(1e-6)

    def hist_plot(self, fitness_data, age_data, weight_data):

        self.plot_hist_fit.cla()
        self.plot_hist_age.cla()
        self.plot_hist_weight.cla()

        self.plot_hist_fit.hist(fitness_data[0],
                                bins=round(self.hist_specs['fitness']['max'] / self.hist_specs['fitness']['delta']),
                                histtype=u'step')
        self.plot_hist_age.hist(age_data[0],
                                bins=round(self.hist_specs['age']['max'] / self.hist_specs['age']['delta']),
                                histtype=u'step')
        self.plot_hist_weight.hist(weight_data[0],
                                   bins=round(self.hist_specs['age']['max'] / self.hist_specs['weight']['delta']),
                                   histtype=u'step')
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

        self.plot_map.imshow(map_rgb)

        self.plot_map.set_xticks(np.arange(1, len(map_rgb[0]), 3))
        self.plot_map.set_xticklabels(np.arange(1, len(map_rgb[0]), 3), fontsize=7)
        self.plot_map.set_yticks(np.arange(1, len(map_rgb), 3))
        self.plot_map.set_yticklabels(np.arange(1, len(map_rgb), 3), fontsize=7)

        ax_land_type = self.fig.add_axes([0.32, 0.75, 0.05, 0.25])
        ax_land_type.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            ax_land_type.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                                 edgecolor='none',
                                                 facecolor=rgb_value[name[0]]))
            ax_land_type.text(0.35, ix * 0.2, name, transform=ax_land_type.transAxes, fontsize=7)

    def dist_plot(self):

        herb_dist = [[self.island.island_map[row][col].get_num_herb_landscape()
                      for col in range(self.island.map_columns)] for row in range(self.island.map_rows)]

        carn_dist = [[self.island.island_map[row][col].get_num_carn_landscape()
                      for col in range(self.island.map_columns)] for row in range(self.island.map_rows)]

        if not self.add_col_bar:
            herb_colb = self.plot_herb_dist.imshow(herb_dist, cmap='viridis',
                                                   vmin=0, vmax=self.cmax_animals['Herbivore'])

            carn_colb = self.plot_carn_dist.imshow(carn_dist, cmap='viridis',
                                                   vmin=0, vmax=self.cmax_animals['Carnivore'])

            c_bar_herb = self.fig.colorbar(herb_colb, ax=self.plot_herb_dist, orientation='vertical', shrink=0.7,
                                           ticks=[0, self.cmax_animals['Herbivore'] / 2,
                                                  self.cmax_animals['Herbivore']])
            c_bar_herb.ax.set_yticklabels(['Low', 'Middle', 'High'], fontsize=7)

            c_bar_carn = self.fig.colorbar(carn_colb, ax=self.plot_carn_dist, orientation='vertical', shrink=0.7,
                                           ticks=[0, self.cmax_animals['Carnivore'] / 2,
                                                  self.cmax_animals['Carnivore']])
            c_bar_carn.ax.set_yticklabels(['Low', 'Middle', 'High'], fontsize=7)

            self.add_col_bar = True

        self.plot_herb_dist.imshow(herb_dist, cmap='viridis', vmin=0, vmax=self.cmax_animals['Herbivore'])
        self.plot_carn_dist.imshow(carn_dist, cmap='viridis', vmin=0, vmax=self.cmax_animals['Carnivore'])

    def save_graphics(self):
        """
        Saves graphics to file if file name given.
        """

        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_no,
                                                     type=self.img_fmt))
        self.img_no += 1
