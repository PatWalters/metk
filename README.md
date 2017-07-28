# metk
#### Model Evaluation Toolkit


In metk, I've collected a set of routines for evaluating predictive models. 
I put a lot of this code together when I was doing the evaluation for the 
[TDT](http://www.teach-discover-treat.org/) and [D3R](https://drugdesigndata.org/)
projects.  I'm releasing this project as a way for the community to collaborate a
and (hopefully) agree on best practices for model evaluation. Most of the 
initial release is oriented toward the evaluation of free energy calculations. 

This is just a start and I plan to add a lot more.  Currently, there are 
routines to calculate 
* Root mean squared (RMS) error
* Mean absolute error (MAE)
* Pearson correlation coefficient (with confidence limits)
* Spearman rank correlation (rho) (still need to add confidence limits)
* Kendall tau (still need to add confience limits) 

The toolkit also includes code to generate a few diagnositc plots that I
find helpful when looking at model performance
* A scatter plot of experimental vs predicted ΔG.  Lines are drawn at 1 and 2 
kcal error
* A histogram of the error distribution.  
* The two plots above with ΔG converted to a binding affinity (in uM or nM).
On the scatter plot, lines are drawn at 5-fold and 10-fold error. 
I find that I mentally relate to a fold error in binding affinity better than 
I do to error expressed in kcal/mol.  However, if you like looking at error in
kcal/mol, use that plot. 

Ultimately, the plan is to implement a number of other methods for model 
evaluation including those described in papers by Anthony Nicholls.  

#### Usage

This relase of metk contains a rudimentary command-line interface. More options 
will be added in time. 

```
Usage: metk.py --in INFILE_NAME --prefix OUTFILE_PREFIX [--units UNIT_NAME] [--example]

--in INFILE_NAME         input file name
--prefix OUTFILE_PREFIX  prefix for output file names
--units UNIT_NAME        units to display (uM (default) or nM)
--example                show example command lines
```

#### Installation

The metk toolkit was written in Python 3.  Seriously people, it's been 9 years
why are you still using 2.7?  



Pat Walters - July 2017


