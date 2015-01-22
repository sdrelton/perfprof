# perfprof
A convenience function for plotting performance profiles in Python.

In scientific computing, one commonly compares multiple algorithms over a set of test problems in terms of
their runtime or relative error.
The best algorithm is the one with the smallest values and, typically,
these are plotted using a scatter plot.

Performance profiles can be a great alternative to scatter plots when comparing multiple sets of data.
Some potential disadvantages of scatter plots are as follows:
- When scatter plots are very crowded it can be hard to tell which algorithm is best overall.
- Small differences between algorithms can be missed.
- If one algorithm is always just slightly worse than another it can be hard to quanitify what _"slightly worse"_ means.

A performance profile makes these sorts of question easy to see at a glance. 
Of course the best practice is to use a scatter plot in conjunction with a performance profile.

**Note:** This implementation is based upon **perfprof** from the MATLAB Guide by D. J. Higham and N. J. Higham.
The original code can be downloaded here:
http://www.maths.man.ac.uk/~higham/mg/m/perfprof.m

## How They Work
Roughly speaking: the x-axis represents a tolerance factor, whilst the y-axis is a
proportion. 
If a line passes through the point (2, 0.8) then the
corresponding data set was within a factor 2 of the smallest
observed value on 80% of the test cases.
If the line first reaches y=1 at the point (10.5, 1) then this
data set was always within a factor 10.5 of the smallest value
observed in each case.

For a more detailed understanding of how performance profiles work please see the references at the bottom
of this document.

## Importing
Since the module only contains one function you might want to import it as follows.
```python
from perfprof import *
```

## Examples
Here are some fabricated examples to help show the difference between
the information that is readily interpreted from scatter plots and performance profiles.

### Example 1: Timings
Suppose we have two algorithms and we would like to see which is faster.
If we have a set of 20 test problems to try them on we can measure the time taken by both
algorithms on each of the problems.

```python
alg1times = 10 + 0.8*np.random.randn(20)
alg2times = 9.9 + 1.2*np.random.randn(20)
```

Now let's generate a scatter plot and performance profile of the data.
```python
markerspecs = ['r^', 'bo']
linespecs = ['r-', 'b-']
labels = ['alg1', 'alg2']

plt.figure()
plt.rc('text', usetex=True)
plt.plot(range(20), alg1times, markerspecs[0])
plt.hold('on')
plt.plot(range(20), alg2times, markerspecs[1])
plt.legend(labels, loc=0, fontsize=14)
plt.hold('off')
plt.savefig(r'fig/timings.png')
plt.tick_params(labelsize=14)
plt.ylim((8.5, 12.8))

data = np.vstack((alg1times, alg2times)).T
perfprof(data, linespecs=linespecs, legendnames=labels, usetex=True)
plt.savefig(r'fig/timings_pp.png')
```

![Scatter plot of timings](fig/timings.png?raw=true "Scatter Plot")
![Performance profile of timings](fig/timings_pp.png?raw=true "Performance Profile")

From the scatter plot alone it would be difficult to see which algorithm is best overall.
Looking at the performance profile we can clearly see that **alg2** was fastest on around 55% of the test cases
and that it was always within a factor 1.22 of the best time.

### Example 2: Relative Errors
For our second example suppose we have two competing algorithms and we want to see which is
the most accurate over a set of 100 test problems.
First let's generate some fake data: the two sets of relative errors and the condition number of each problem.

```python
cond = np.exp(np.sort(3e1*np.random.rand(100))[::-1])
condu = np.finfo(np.double).eps/2 * cond

rerr1 = 1e-3 * (condu + 100 * np.random.randn(100) * condu)
rerr2 = 1e-3 * (condu + 200 * np.random.randn(100) * condu)
```

Plotting the data we get the following.

```python
plt.figure()
plt.rc('text', usetex=True)
plt.hold('on')
plt.semilogy(range(100), condu, 'b-')
plt.semilogy(range(100), rerr1, 'r^')
plt.semilogy(range(100), rerr2, 'bo')
plt.legend(['cond u', 'alg1', 'alg2'], loc=0, fontsize=14)
plt.tick_params(labelsize=14)
plt.savefig(r'fig/relerr.png')

labels = ['alg1', 'alg2']
linespecs = ['r-', 'b-']
data = np.vstack((rerr1, rerr2)).T
perfprof(data, linespecs=linespecs, legendnames=labels, thmax=10, usetex=True)
plt.ylim((0.6, 1))
plt.savefig(r'fig/relerr_pp.png')
```

![Scatter plot of timings](fig/relerr.png?raw=true "Scatter Plot")
![Performance profile of timings](fig/relerr_pp.png?raw=true "Performance Profile")

We can see from the scatter plot that **alg1** is generally better but it is harder to see
how far behind **alg2** is.
The performance profile answers this question.
For example, we see that on 90% of the test problems **alg2** is within a factor 4 of **alg1**
so that, whilst **alg1** is more accurate, the difference between the two is not enormous.

## References
[1] 
    E. D. Dolan, and J. J. More,
    **Benchmarking Optimization Software with Performance Profiles.**
    _Math. Programming_, 91:201-213, 2002.

[2] 
   N. J. Dingle, and N. J. Higham,
   **Reducing the Influence of Tiny Normwise Relative Errors
    on Performance Profiles.** _ACM Trans. Math. Software_,
    39(4):24:1-24:11, 2013.

[3]
   D. J. Higham, and N. J. Higham,
   **MATLAB Guide, Second Edition.**
   _SIAM_, 2005. xxiii+382 pages, ISBN 0-89871-578-4.
