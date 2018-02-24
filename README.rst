metk
====

Model Evaluation Toolkit
^^^^^^^^^^^^^^^^^^^^^^^^

| In metk, I've collected a set of routines for evaluating predictive
  models.
| I put a lot of this code together when I was doing the evaluation for
  the
| `TDT <http://www.teach-discover-treat.org/>`__ and
  `D3R <https://drugdesigndata.org/>`__
| projects, as well as
| `a book chapter I wrote in
  2013 <http://onlinelibrary.wiley.com/doi/10.1002/9781118742785.ch1/summary>`__.
| I'm releasing this project as a way for the community to collaborate
| and (hopefully) agree on best practices for model evaluation. Most of
  the
| initial release is oriented toward the evaluation of free energy
  calculations.

| This is just a start and I plan to add a lot more. Currently, there
  are
| routines to calculate

-  Root mean squared (RMS) error
-  Mean absolute error (MAE)
-  Pearson correlation coefficient (with confidence limits)
-  Spearman rank correlation (rho) (still need to add confidence limits)
-  Kendall tau (still need to add confience limits)
-  Maximum possible correlation given a specific experimental error.
   This is
   based on on a 2009 paper by
   `Brown, Muchmore and
   Hajduk <http://www.sciencedirect.com/science/article/pii/S1359644609000403>`__

| Most of the statistics is done with routines from
  `scikitlearn <http://scikit-learn.org/stable/>`__
| and `scipy <https://www.scipy.org/>`__.

| The toolkit also includes code to generate a few diagnositc plots that
  I
| find helpful when looking at model performance. Examples of these
  plots can be found
| `here <https://figshare.com/articles/metk_out_pdf/5258080>`__

-  A scatter plot of experimental vs predicted ΔG. Lines are drawn at 1
   and 2
   kcal error
-  A histogram of the error distribution.
-  The two plots above with ΔG converted to a binding affinity (in uM or
   nM).
   On the scatter plot, lines are drawn at 5-fold and 10-fold error.
   I find that I mentally relate to a fold error in binding affinity
   better than
   I do to error expressed in kcal/mol. However, if you like looking at
   error in
   kcal/mol, use that plot.

| Ultimately, the plan is to implement a number of other methods for
  model
| evaluation including those described in papers by Anthony Nicholls.

Usage
^^^^^

| This relase of metk contains a rudimentary command-line interface.
  More options
| will be added in time.

::

    Usage: metk.py --in INFILE_NAME --prefix OUTFILE_PREFIX [--units UNIT_NAME] [--example]

    --in INFILE_NAME         input file name
    --prefix OUTFILE_PREFIX  prefix for output file names
    --units UNIT_NAME        units to display (uM (default) or nM)
    --example                show example command lines

Installation
^^^^^^^^^^^^

The toolkit works under both Python 2.7 and Python 3.6. Installation is
relatively painless.

#. Install the dependencies, you can do this with pip

   ::

       pip install numpy pandas matplotlib scipy docopt

#. | Get the code from github. You can either download and unpack the
     zip file
   | or just clone the repository.

   ::

       git clone https://github.com/PatWalters/metk.git

#. | There's one more trick to make the plots work with matplotlib. When
     pip installed
   | matplotlib, it created a directory under your home directory called
     .matplotlib. Create
   | a file in this directory called matplotlibrc and put this line in
     that file.

::

    backend: TkAgg

#. | At this point you should be all set. The main script is metk.py.
     The other Python
   | files need to either be in the same directory or in your
     PYTHONPATH. You can
   | then run the script with this command.

   ::

       python metk.py

   | If you're running under Linux or OS-X and you hate typing "python"
     all the time
   | (I know I do) you can do

   ::

       chmod +x metk.py
       ./metk.py

A Few Notes
^^^^^^^^^^^

`I use tabs <https://www.youtube.com/watch?v=SsoOG6ZeyUI>`__

Please don't hesitate to let me know if you run into problems or have
additions or improvements.

Pat Walters - July 2017
