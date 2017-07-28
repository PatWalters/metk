#!/usr/bin/env python

from __future__ import print_function
import sys
from math import log10
import pandas as pd
from metk_util import rmse, mean_absolute_error, pearson_confidence, max_possible_correlation, kcal_to_ki
from scipy.stats import pearsonr, kendalltau, spearmanr


def metk_report(df_kcal):
    """
    Generate a report
    :param df_kcal: input dataframe, activity should be in kcal/mol
    :param outfile: output file for the report
    :return: the report as a list of strings
    """
    N = df_kcal.shape[0]
    pred = df_kcal['Pred']
    expr = df_kcal['Exp']
    rms_val = rmse(pred, expr)
    mae_val = mean_absolute_error(pred, expr)
    pearson_r, pearson_p = pearsonr(pred, expr)
    pearson_vals = [x ** 2 for x in [pearson_r] + list(pearson_confidence(pearson_r, N))]
    spearman_r, spearman_p = spearmanr(pred, expr)
    kendall_t, kendall_p = kendalltau(pred, expr)
    max_correlation = max_possible_correlation([log10(kcal_to_ki(x)) for x in df_kcal['Exp']])
    report = []
    report.append("N = %d" % N)
    report.append("RMSE = %.2f kcal/mol" % rms_val)
    report.append("MAE  = %.2f kcal/mol" % mae_val)
    report.append("Max possible correlation = %.2f" % max_correlation)
    report.append("Pearson R^2 = %0.2f  95%%CI = %.2f %.2f" % tuple(pearson_vals))
    report.append("Spearman rho = %0.2f" % spearman_r)
    report.append("Kendall tau = %0.2f" % kendall_t)
    return report


def main():
    df_kcal = pd.read_csv(sys.argv[1])
    metk_report(df_kcal)

if __name__ == "__main__":
    main()
