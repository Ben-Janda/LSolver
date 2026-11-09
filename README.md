# Molecular motor simulation

This repository contains package `LSolver` and example notebooks with multiple applications and tests of this package.

## Overview

The package `LSolver` is simple collection of two algorithms for solving Langevin equation in under/over- damped regime. For overdamped regime, I have used the traditional Euler-Maruyama discretization method. For underdamped regime, I have used Verlet-type algorithm of [1].

### Supported equations

Any overdamped Langevin equation(s) of following type can be numerically solved with the method `LSolver.overdamped`:
$$\dot x(t) = \frac{1}{\gamma}F_x(x(t),y(t),t) + \sqrt{2k_B T_x(x(t),y(t),t)/\gamma}\;\xi_x(t),$$
$$\dot y(t) = \frac{1}{\gamma}F_y(x(t),y(t),t) + \sqrt{2k_B T_y(x(t),y(t),t)/\gamma}\;\xi_y(t).$$
Method `LSolver.underdamped` can be used for Langevin equation(s) of type
$$m \ddot x(t) = -\gamma \dot x(t) + F_x(x(t),y(t),t) + \sqrt{2\gamma k_B T_x(x(t),y(t),t)}\; \xi_x(t),$$
$$m \ddot y(t) = -\gamma \dot y(t) + F_y(x(t),y(t),t) + \sqrt{2\gamma k_B T_y(x(t),y(t),t)}\; \xi_y(t).$$
Lastly, the method `LSolver.mixed` is specifically for the special combination
$$\dot x(t) = \frac{1}{\gamma}F_x(x(t),y(t),t) + \sqrt{2k_B T_x(x(t),y(t),t)/\gamma}\;\xi_x(t),$$
$$m \ddot y(t) = -\gamma \dot y(t) + F_y(x(t),y(t),t) + \sqrt{2\gamma k_B T_y(x(t),y(t),t)}\; \xi_y(t).$$

### Configuration

Dataclass `LSolver.SimulationConfig` is used for specifying the parameters of the simulation, like force functions, temperature functions, friction coefficient, mass or initial conditions, as well as the RNG for reproducibility.

## Installation
*Incomplete*

## Examples
*TBA*

## Repository Structure
*TBA*

## Acknowledgements

This work was supported by SFG MFF UK (Student Faculty Grant) under the title "Termodynamické relace neurčitosti". The author is grateful to doc. V. Holubec of KMF MFF UK for supervising the project and providing invaluable guidance and consultations.

## References

[1] Grønbech-Jensen, N., & Farago, O. (2013). A simple and effective Verlet-type algorithm for simulating Langevin dynamics. Molecular Physics, 111(8), 983–991. Dostupné na: https://doi.org/10.1080/00268976.2012.760055