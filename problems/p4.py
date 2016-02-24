#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import corner
import numpy as np

from plot_setup import setup

setup()  # initialize the plotting styles
np.random.seed(42)


def log_p_gauss(x):
    V = np.array([[2.0, 1.2], [1.2, 2.0]])
    alpha = np.linalg.solve(V, x)
    return -0.5 * np.dot(x, alpha)


def log_p_uniform(x):
    if 3 <= x[0] <= 7 and 1 <= x[1] <= 9:
        return 0.0
    return -np.inf


def run_mcmc(log_p, x, prop_sigma=1.0, nsteps=2e4):
    lp = log_p(x)
    chain = np.empty((nsteps, len(x)))
    for step in range(len(chain)):
        x_prime = np.array(x)
        x_prime[np.random.randint(len(x))] += prop_sigma * np.random.randn()
        lp_prime = log_p(x_prime)
        if np.random.rand() <= np.exp(lp_prime - lp):
            x[:] = x_prime
            lp = lp_prime
        chain[step] = x
    return chain


chain = run_mcmc(log_p_gauss, np.array([0.0, 0.0]))
fig = corner.corner(chain, labels=["$x$", "$y$"],
                    range=[(-4.5, 4.5), (-4.5, 4.5)],
                    plot_density=False, plot_contours=False)
fig.savefig("p4a.pdf", dpi=300)

chain = run_mcmc(log_p_uniform, np.array([5.0, 5.0]), nsteps=1e5)
fig = corner.corner(chain, labels=["$x$", "$y$"],
                    range=[(2.5, 7.5), (0.5, 9.5)],
                    plot_density=False, plot_contours=False)
fig.savefig("p4b.pdf", dpi=300)
