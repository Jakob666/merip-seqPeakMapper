# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
import warnings


class PeakVisulizer:
    """
    visulize the peak distribution for the peak calling result.
    """
    def __init__(self, peak_location_file):
        """
        :param peak_location_file: the output result of PeakMapper
        """
        self.peak_file = peak_location_file

    def peak_location(self):
        peak_loc = pd.read_csv(self.peak_file, sep="\t", usecols=[7])
        peak_loc = peak_loc.values.flatten()
        return peak_loc

    @staticmethod
    def get_distribution(peak_loc_data, bandwidth_test_range=(0.1, 1.0), test_step=30, cv_num=10):
        """
        use guassian kernel density function to fit the peak location data and got its contiunous distribution.
        :param peak_loc_data: the peak location data from the peak location file, type numpy array
        :param bandwidth_test_range: the value range of bandwidth, type list or tuple
        :param test_step: the bandwidth range will be equally splited into pieces
        :param cv_num: the cross validation number for grid search cross validation
        :return:
        """
        bins = np.array(list(range(0, 301)))
        # use grid search to find the kernel density estimator with best "bandwidth" param
        low_limit, high_limit = bandwidth_test_range
        grid = GridSearchCV(KernelDensity(), param_grid={"bandwidth": np.linspace(low_limit, high_limit, test_step)}, cv=cv_num)
        grid.fit(peak_loc_data[:, None])
        best_banwidth = grid.best_params_
        kde = grid.best_estimator_
        pdf = np.exp(kde.score_samples(bins[:, None]))
        pdf = pdf.tolist()
        kde_plots = np.array(list(zip(bins, pdf)))

        return kde_plots, best_banwidth

    @staticmethod
    def visulize(kde_plots, kde_bandwidth, real_plots, bins_num):
        """
        :param kde_plots: plots got from kernel density function
        :param kde_bandwidth: the bandwidth parameter of KDE function
        :param real_plots: the real data
        :param bins_num: bin number for hist plot
        :return:
        """
        x = np.array([i[0] for i in kde_plots])
        y = np.array([i[1] for i in kde_plots])
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y, color="blue", alpha=0.5, label="peak distribut with bw = %s" % kde_bandwidth["bandwidth"])
        # use hist plot to judge the kde function effect
        ax.hist(real_plots, bins_num, fc="gray", histtype="stepfilled", alpha=0.3, normed=True,
                label="hist plot of real data")
        ax.set_xlim(0, 300)
        ax.set_ylim(0, 0.012)
        ax.legend(loc="upper left")
        plt.savefig("peak.png")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    pv = PeakVisulizer(r"/data/nanopore/merip_seq_data/metpeak_calling_res/peak_location/reference_files/peak_loc.tsv")
    loca_data = pv.peak_location()
    kde_data, bandwidth = pv.get_distribution(loca_data, (1.0, 6.0), test_step=500)
    pv.visulize(kde_data, bandwidth, loca_data, 300)

