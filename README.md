# Molecular motor simulation

This repository contains package `LSolver` and example notebooks with multiple applications and tests of this package.

## Overview

The package `LSolver` is lightweight package that uses two algorithms for solving Langevin equation in under/over- damped regime. For overdamped regime, we have used the traditional Euler-Maruyama discretization method. For underdamped regime, we have used Verlet-type algorithm of [1].

### Supported equations

Any overdamped Langevin equation(s) of following type can be numerically solved with the method `LSolver.overdamped`:

$$
\dot x(t) = \frac{1}{\gamma}F_x(x(t),y(t),t) + [2k_B T_x(x(t),y(t),t)/\gamma]^{1/2}\ \xi_x(t),
$$

$$
\dot y(t) = \frac{1}{\gamma}F_y(x(t),y(t),t) + [2k_B T_y(x(t),y(t),t)/\gamma]^{1/2}\ \xi_y(t).
$$

Method `LSolver.underdamped` can be used for Langevin equation(s) of type

$$
m \ddot x(t) = -\gamma \dot x(t) + F_x(x(t),y(t),t) + [2\gamma k_B T_x(x(t),y(t),t)]^{1/2}\ \xi_x(t),
$$

$$
m \ddot y(t) = -\gamma \dot y(t) + F_y(x(t),y(t),t) + [2\gamma k_B T_y(x(t),y(t),t)]^{1/2}\ \xi_y(t).
$$

Lastly, the method `LSolver.mixed` is specifically for the special combination

$$
\dot x(t) = \frac{1}{\gamma}F_x(x(t),y(t),t) + [2k_B T_x(x(t),y(t),t)/\gamma]^{1/2}\ \xi_x(t),
$$

$$
m \ddot y(t) = -\gamma \dot y(t) + F_y(x(t),y(t),t) + [2\gamma k_B T_y(x(t),y(t),t)]^{1/2}\ \xi_y(t).
$$

### Configuration

Dataclass `LSolver.SimulationConfig` is used for specifying the parameters of the simulation, like force functions, temperature functions, friction coefficient, mass or initial conditions, as well as the RNG for reproducibility.

## Installation
*Incomplete*

## Examples

There are several examples of using the `LSolver` package in jupyter notebooks. Short explanation:

1. `01_Intro` tests the implemented Euler-Maruyama algorithm (`LSolver.overdamped`) on the example of brownian particle in harmonic potential, confronting the numerical solution with analytical solution.
2. `02_Feynmans-ratchet` applies `LSolver.overdamped` on the famous Feynman's ratchet and pawl system, with(out) weight and with(out) cooling of the pawl, showing how this system could generate usable work for pulling the weight up.
3. `03_Stirling-engine` applies `LSolver.overdamped` on system of brownian particle inside optical tweezers, working in Stirling-like cycles. Contains calculation of generated work and checks the Thermodynamic Uncertainty Relations.
4. `04_Underdamped` tests the implemented Veltet-type algorithm (`LSolver.underdamped`) on several systems, namely free diffusion with friction, constant external force field and harmonic potential in stationary limit, confronting the numerical results with analytical calculations.
5. `05_TUR` uses `LSolver.mixed` for examination of special system, that was of our interest. This was the main goal of the project.

## Repository Structure

```plaintext
Molecular-Motor/
├── LSolver
|   ├── __init__.py
|   ├── config.py
|   └── engine.py
├── .gitignore
├── 01_Intro.ipynb
├── 02_Feynmans-ratchet.ipynb
├── 03_Stirling-engine.ipynb
├── 04_Underdamped.ipynb
├── 05_TUR.ipynb
└── README.md
```

## Acknowledgements

This work was supported by SFG MFF UK (Student Faculty Grant) under the title "Termodynamické relace neurčitosti". The author is grateful to doc. V. Holubec of KMF MFF UK for supervising the project and providing invaluable guidance and consultations.

## References

[1] Grønbech-Jensen, N., & Farago, O. (2013). A simple and effective Verlet-type algorithm for simulating Langevin dynamics. Molecular Physics, 111(8), 983–991. Available at: https://doi.org/10.1080/00268976.2012.760055