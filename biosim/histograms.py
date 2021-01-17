# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

class Histograms:
    def __init__(self, data):
        self.data = data


    def plot_hist(self):

        data_herb = [1, 45, 3, 54, 23, 2, 0, 2, 43, 45, 4, 4, 12, 32, 32]
        data_1 = [1, 45, 45, 54, 23, 3, 2, 2, 2, 45, 4, 4, 12, 32, 32]

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.hist(ages, bins=10, histtype=u'step')
        ax.hist(ages_1, bins=10, histtype=u'step')

        plt.show()



class Age_hist(Histograms):
    def __init__(self, data):
        super().__init__(data)


class Weight_hist(Histograms):
    def __init__(self, data):
        super().__init__(data)


class Fitness_hist(Histograms):
    def __init__(self, data:
        super().__init__(data)


if __name__ == '__main__':
    age_hist =

