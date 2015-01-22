r"""
perfprof
--------

Plot a performance profile.

It is recommended to import using:
    from perfprof import *
as this module contains only one function.

More detailed help can be found in the docstring of the
function.

Samuel Relton
samuel.relton@manchester.ac.uk
www.samrelton.com

22 Jan 2015
"""
import numpy as np
import matplotlib.pyplot as plt


def perfprof(data, linespecs=None, linewidth=1.6, thmax=None,
             thlabel=r'$\theta$', plabel='$p$', tol=np.double(1e-8),
             legendnames=None, legendpos=0,
             fontsize=18, tickfontsize=14, legendfontsize=14,
             ppfix=False, ppfixmin=np.double(1e-18),
             ppfixmax=np.finfo(np.double).eps/2,
             usetex=None):
    r"""
    Plot a performance profile.

    Make a performance profile of the array *data*.
    A performance profile is an alternative to a scatter plot when
    we compare multiple series of data and are looking for the
    set of values which is smallest on average.
    Typically this would be comparing alternative algorithms for a
    problem in terms of their runtime or relative error over a set
    of test cases.

    The x-axis represents a tolerance factor, whilst the y-axis is a
    proportion. If a line passes through the point (2, 0.8) then the
    corresponding data set was within a factor 2 of the smallest
    observed value on 80% of the test cases.
    If the line first reaches y=1 at the point (10.5, 1) then this
    data set was always within a factor 10.5 of the smallest value
    observed in each case.

    See the references for additional detail.

    This code is based upon perfprof from the MATLAB Guide by
    D. J. Higham and N. J. Higham.

    The original code can be downloaded here:
    http://www.maths.man.ac.uk/~higham/mg/m/perfprof.m

    Parameters
    ----------
    data -  Array of timings/errors to plot.
            The rows of the array must be the different test cases
            whilst the columns are the different algorithms to compare.

    linespecs - List of line specifications, e.g. ['r-', 'k:']

    linewidth - Width of the lines.

    thmax - Maximum value of theta shown on the x-axis.
            If None then thmax defaults to the point where all
            algorithms reach 1 on the y-axis.

    thlabel - Rename theta on the x-axis label.

    plabel - Rename p on the y-axis label.

    tol - Tolerance on the x-coordinates to ensure plots fit on
          the graph.

    legendnames - Labels for the lines, used to create a legend.
                  If None the legend is not created.

    legendpos - Position of the legend.

    fontsize - Font size for the x and y-axis labels.

    tickfontsize - Font size for the x and y-axis tick labels.

    legendfontsize - Font size for the legend text.

    ppfix - Modify the data to avoid tiny results skewing the
            performance profile. Performs a linear interpolation
            on small data points to avoid skewing the results.
            Useful for plotting performance profiles of
            relative errors: see reference [2].

    ppfixmin - The smallest possible data point after manipulation
               by ppfix.

    ppfixmax - Data points below this value will be modified by ppfix.

    usetex - Use LaTeX for all the labels in the plot.


    References
    ----------
    [1] E.D. Dolan, and J. J. More,
        Benchmarking Optimization Software with Performance Profiles.
        Math. Programming, 91:201-213, 2002.

    [2] N. J. Dingle, and N. J. Higham,
        Reducing the Influence of Tiny Normwise Relative Errors
        on Performance Profiles. ACM Trans. Math. Software,
        39(4):24:1-24:11, 2013.
    """
    usetexorig = plt.rcParams['text.usetex']
    if usetex is not None:
        try:
            plt.rc('text', usetex=usetex)
        except e:
            print('Problem changing use of LaTeX.')

    data = np.asarray(data).astype(np.double)

    if ppfix:
        data = np.array(data >= ppfixmax, dtype=np.int) * data + \
            np.array(data < ppfixmax, dtype=np.int) * \
            (ppfixmin + data*(ppfixmax - ppfixmin)/ppfixmax)

    minvals = np.min(data, axis=1)
    if thmax is None:
        thmax = np.max(np.max(data, axis=1) / minvals)
    m, n = data.shape  # m tests cases, n alternatives

    if len(linespecs) != n:
        raise ValueError("Length of argument linespecs must equal "
                         "number of columns in the input data.")

    if legendnames is not None:
        if len(legendnames) != n:
            raise ValueError("Length of argument legendnames must "
                             "equal number of columns in input data.")

    plt.figure()

    for alt in range(n):  # for each alternative
        col = data[:, alt] / minvals  # performance ratio
        col = col[~np.isnan(col)]  # remove nans

        if len(col) == 0:
            continue

        theta = np.unique(col)
        r = len(theta)
        myarray = np.repeat(col, r).reshape(len(col), r) <= \
            np.repeat(theta, len(col)).reshape((len(col), r), order='F')
        myarray = np.array(myarray, dtype=np.double)
        prob = np.sum(myarray, axis=0) / m

        # Get points to print staircase plot
        k = np.array(np.floor(np.arange(0, r, 0.5)), dtype=np.int)
        x = theta[k[1:]]
        y = prob[k[0:-1]]

        # check endpoints
        if x[0] >= 1+tol:
            x = np.append([1, x[0]], x)
            y = np.append([0, 0], y)
        if x[-1] < thmax - tol:
            x = np.append(x, thmax)
            y = np.append(y, y[-1])

        # plot current line
        plt.hold('on')

        if legendnames is None:
            plt.plot(x, y, linespecs[alt], linewidth=linewidth)
        else:
            plt.plot(x, y, linespecs[alt], linewidth=linewidth,
                     label=legendnames[alt])

    # set labels and ticks
    plt.xlabel(thlabel, fontsize=fontsize)
    plt.ylabel(plabel, fontsize=fontsize)
    plt.tick_params(labelsize=tickfontsize)

    # create legend
    plt.legend(loc=legendpos, fontsize=legendfontsize)

    # set xlim
    plt.xlim([1, thmax])
    plt.ylim([0, 1.01])
    plt.hold('off')
    plt.draw()

    if usetex is not None:
        try:
            plt.rc('text', usetex=usetexorig)
        except e:
            print('Problem changing use of LaTeX.')
