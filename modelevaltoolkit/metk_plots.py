#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import warnings
from metk_util import kcal_to_ki_df, check_dataframe
import math

def ic50_histogram(df, ax, bins=None):
    """
    Generate a histogram of the IC50 error in folds
    :param df: input dataframe
    :param ax: matplotlib axis
    :param bins:  bins to use (currently <5 kcal, 5-10 kcal, >10 kcal
    :return: None
    """
    add_ic50_error(df)
    if bins is None:
        bins = [0, 5, 10, 15]
    counts, hist_bins = np.histogram(np.clip(df['Error'], bins[0], bins[-1]), bins)
    counts = counts / float(sum(counts))
    ax.bar([1, 2, 3], counts, alpha=0.5, edgecolor="black")
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(("<5", "5-10", ">10"))
    ax.set_xlabel("Fold Error")
    ax.set_ylabel("Normalized Count")


def kcal_histogram(df, ax, bins=None):
    """
    Generate a histogram of the error in kcal/mol
    :param df: input dataframe
    :param ax: matplotlib axis
    :param bins: bins to use (currently "<1 kcal", "1-2 kcal", ">2 kcal")
    :return:
    """
    add_kcal_error(df)
    if bins is None:
        bins = [0, 1, 2, 3]
    counts, hist_bins = np.histogram(np.clip(df['Error'], bins[0], bins[-1]), bins)
    counts = counts / float(sum(counts))
    ax.bar([1, 2, 3], counts, alpha=0.5, edgecolor="black")
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(("<1", "1-2", ">2"))
    ax.set_xlabel(r'$\Delta$G Error (kcal/mol)')
    ax.set_ylabel("Normalized Count")


def add_ic50_error(df, bins=None):
    """
    Add columns to a dataframe showing absolute and binned err
    :param df: input dataframe
    :param bins: bins to use (currently <5 kcal, 5-10 kcal, >10 kcal
    :return:
    """
    if bins is None:
        bins = [5, 10]
    pt_color = ['green', 'yellow', 'red']
    df['Error'] = [10 ** x for x in np.abs(np.log10(df['Exp']) - np.log10(df['Pred']))]
    df['Error_Bin'] = [pt_color[x] for x in np.digitize(df['Error'], bins)]


def add_kcal_error(df, bins=None):
    """
    Add columns to a dataframe showing absolute and binned err
    :param df: input dataframe
    :param bins: bins to use (currently "<1 kcal", "1-2 kcal", ">2 kcal")
    :return: None
    """
    if bins is None:
        bins = [1, 2]
    pt_color = ['green', 'yellow', 'red']
    df['Error'] = np.abs(df['Exp'] - df['Pred'])
    df['Error_Bin'] = [pt_color[x] for x in np.digitize(df['Error'], bins)]


def ic50_plot(df, ax, axis_range=None, units="uM"):
    """
    Draw a scatterplot of experimental vs predicted IC50
    :param df: input dataframe
    :param ax: matplotlib axis
    :param axis_range: range for axes [minX, maxY, minY, maxY
    :param units: units for IC50 plot (currently uM or nM)
    :return: None
    """
    if axis_range is None:
        axis_range = np.array([0.001, 100, 0.0001, 100])
    if units == "nM":
        axis_range *= 1000
    min_x, max_x, min_y, max_y = axis_range
    add_ic50_error(df)

    ax.set(xscale="log", yscale="log")
    ax.axis(axis_range)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y), 0)))).format(y)))
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y), 0)))).format(y)))
    ax.set_xlabel("Experimental IC50 (%s)" % units)
    ax.set_ylabel("Predicted IC50 (%s)" % units)
    ax.scatter(df['Exp'], df['Pred'], s=100, c=df['Error_Bin'], alpha=0.5, edgecolors="black")

    ax.plot([0, max_x], [0, max_y], linewidth=2, color='black')
    # 5 fold
    ax.plot([0, max_x], [0, max_y * 5], linewidth=1, color="blue", linestyle='--')
    ax.plot([0, max_x], [0, max_y / 5], linewidth=1, color="blue", linestyle='--')
    # 10 fold
    ax.plot([0, max_x], [0, max_y * 10], linewidth=1, color="black")
    ax.plot([0, max_x], [0, max_y / 10], linewidth=1, color="black")


def kcal_plot(df, ax, axis_range=None):
    """
    Draw a scatterplot of experimental vs predicted Ki or IC50
    :param df: input dataframe
    :param ax: matplotlib axis
    :param axis_range: range for axes [minX, maxY, minY, maxY]
    :return: None
    """
    if axis_range is None:
        axis_range = [-12, -6, -12, -6]
    pt_color = ['green', 'yellow', 'red']
    df['Error'] = np.abs(df['Exp'] - df['Pred'])
    df['Error_Bin'] = [pt_color[x] for x in np.digitize(df['Error'], [1, 2])]
    ax.axis(axis_range)
    ax.set_xlabel(r'Experimental $\Delta$G (kcal/mol)')
    ax.set_ylabel(r'Predicted $\Delta$G (kcal/mol)')
    ax.scatter(df['Exp'], df['Pred'], s=100, c=df['Error_Bin'], alpha=0.5, edgecolors="black")
    # y = x
    ax.plot([0, -100], [0, -100], linewidth=2, color='black')
    # y = x+1
    ax.plot([-1, -100], [0, -100], linewidth=1, color="blue", linestyle='--')
    # y = x-1
    ax.plot([1, -100], [0, -100], linewidth=1, color="blue", linestyle='--')
    # y = x+2
    ax.plot([-2, -100], [0, -100], linewidth=1, color="black")
    # y = x-2
    ax.plot([2, -100], [0, -100], linewidth=1, color="black")


def draw_plots(df_kcal, pdf_file_name, units='uM'):
    """
    Draw scatter plots and histograms showing agreement between experimental and predicted activity
    :param df_kcal: input dataframe, data is in kcal/mol
    :param pdf_file_name: output file for plot
    :param units: units to use for the plots (currently uM or nM)
    :return:
    """
    add_kcal_error(df_kcal)
    f_kcal, ax_kcal = plt.subplots(2, figsize=(7, 7))
    ax_kcal[0].set_title("N = %d" % df_kcal.shape[0])
    
    minx = int( min(df_kcal["Exp"] ) - 1 )
    maxx = int( max(df_kcal["Exp"] ) + 1 )
    miny = int( min(df_kcal["Pred"]) - 1 )
    maxy = int( max(df_kcal["Pred"]) + 1 )
    
    kcal_plot(df_kcal, ax_kcal[0], axis_range=[minx, maxx, miny, maxy])
    kcal_histogram(df_kcal, ax_kcal[1])
    pdf_pages = PdfPages(pdf_file_name)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.tight_layout()
    pdf_pages.savefig(f_kcal.get_figure())

    df_ic50 = kcal_to_ki_df(df_kcal, units)
    add_ic50_error(df_ic50)
    f_ic50, ax_ic50 = plt.subplots(2, figsize=(7, 7))
    
    minx = 10**( math.log10(min(df_ic50["Exp"] )) - 1 )
    maxx = 10**( math.log10(max(df_ic50["Exp"] )) + 1 )
    miny = 10**( math.log10(min(df_ic50["Pred"])) - 1 )
    maxy = 10**( math.log10(max(df_ic50["Pred"])) + 1 )
    
    ic50_plot(df_ic50, ax_ic50[0], axis_range=[minx, maxx, miny, maxy], units=units)
    ic50_histogram(df_ic50, ax_ic50[1])
    pdf_pages.savefig(f_ic50.get_figure())

    pdf_pages.close()

def generate_pdf(figure_list, pdf_file_name):
    pdf_pages = PdfPages(pdf_file_name)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.tight_layout()
    for ax in figure_list:
        pdf_pages.savefig(ax.get_figure())
    pdf_pages.close()


def main():
    pdf_file_name = "/Users/pwalters/scratch/myplot.pdf"
    df_kcal = pd.read_csv(sys.argv[1])
    check_dataframe(df_kcal)
    draw_plots(df_kcal, pdf_file_name, units="nM")


if __name__ == "__main__":
    main()
