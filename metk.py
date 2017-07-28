#!/usr/bin/env python

"""Usage: metk.py --in INFILE_NAME --prefix OUTFILE_PREFIX [--units UNIT_NAME] [--example]

--in INFILE_NAME         input file name
--prefix OUTFILE_PREFIX  prefix for output file names
--units UNIT_NAME        units to display (uM (default) or nM)
--example                show example command lines
"""

from docopt import docopt
from metk_report import metk_report
from metk_plots import draw_plots
import pandas as pd
from io import StringIO

of_string = StringIO()

do_input = docopt(__doc__)
infile_name = do_input.get("--in")
prefix = do_input.get("--prefix")
units = do_input.get("--units") or 'uM'

pdf_file_name = prefix + ".pdf"
report_file_name = prefix + ".txt"

df = pd.read_csv(infile_name)
metk_report(df, of_string)
draw_plots(df, pdf_file_name, units)
report_str = of_string.getvalue()
print(report_str)
of_string.close()
report_file = open(report_file_name, "w")
print(report_str, file=report_file)
report_file.close()
print("Report written to %s" % report_file_name)
print("Plots written to %s" % pdf_file_name)
