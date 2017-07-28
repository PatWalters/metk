#!/usr/bin/env python

import sys
from math import log10
import pandas as pd
from metk_util import rmse, mean_absolute_error, pearson_confidence, max_possible_correlation, kcal_to_ki
from scipy.stats import pearsonr, kendalltau, spearmanr


def metk_report(df_kcal, outfile=sys.stdout):
    """
    Generate a report
    :param df_kcal: input dataframe, activity should be in kcal/mol
    :param outfile: output file for the report
    :return: None
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
    print("N = %d" % N, file=outfile)
    print("RMSE = %.2f kcal/mol" % rms_val, file=outfile)
    print("MAE  = %.2f kcal/mol" % mae_val, file=outfile)
    print("Max possible correlation = %.2f" % max_correlation,file=outfile)
    print("Pearson R^2 = %0.2f  95%%CI = %.2f %.2f" % tuple(pearson_vals), file=outfile)
    print("Spearman rho = %0.2f" % spearman_r, file=outfile)
    print("Kendall tau = %0.2f" % kendall_t, file=outfile)


def main():
    df_kcal = pd.read_csv(sys.argv[1])
    metk_report(df_kcal)

if __name__ == "__main__":
    main()
