# API Reference

This document provides detailed reference for the core components and methods of the package `LSolver`.

---

## `LSolver.SimulationConfig`

A configuration dataclass used to set up the physical parameters, time steps, and reproducibility for the simulation.

### Required Attributes

- `gamma` (*float*): Friction coefficient ($\gamma$).
- `Fx_func` (*callable*): Force component in the $x$-DoF, $F_x(x(t),y(t),t)$, signature `lambda t,x,y`.
- `Tx_func` (*callable*): Temperature in the $x$-DoF, $T_x(x(t),y(t),t)$, signature `lambda t,x,y`.
- `t_max` (*float*): end time of the simulation.
- `dt` (*float*): timestep of the discretization.

### Optional Attributes

- `m` (*float*): mass of the particle, default `None`. Raises `ValueError` if left unspecified when using `LSolver.underdamped` and `LSolver.mixed`.
- `x0` (*float*): initial value of $x$, default `0.0`.
- `vx0` (*float*): initial velocity in the $x$-DoF, default `0.0`.
- `y0` (*float*): initial value of $y$, default `0.0`.
- `vy0` (*float*): initial velocity in the $y$-DoF, default `0.0`.
- `Fy_func` (*callable*): Force component in the $y$-DoF, $F_y(x(t),y(t),t)$. Default is `lambda t,x,y: 0.0`.
- `Ty_func` (*callable*): Temperature in the $y$-DoF, $T_y(x(t),y(t),t)$. Default is `lambda t,x,y: 0.0`.

---

## Integration Methods

### `LSolver.overdamped`

```python
LSolver.overdamped(config: SimulationConfig, rng: numpy.random.Generator = None) -> tuple[numpy.ndarray, numpy.ndarray]
```
Simulates overdamped Langevin equation with 2 DoF using the standard Euler-Maruyama discretization scheme.

**Parameters:**
- `config` (`SimulationConfig`): The configuration object of simulation.
- `rng` (`np.random.Generator`): RNG with specified seed for reproducibility. If not specified, new instance with unspecified seed will be initiated.

**Returns:**
- `x` (`numpy.ndarray`): Position array of $x$-coordinate, of shape `(num_steps,)`.
- `y` (`numpy.ndarray`): Position array of $y$-coordinate, of shape `(num_steps,)`.

### `LSolver.underdamped`

```python
LSolver.underdamped(config: SimulationConfig, rng: numpy.random.Generator = None) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]
```
Simulates underdamped Langevin equation with 2 DoF using the Verlet-type algorithm [1].

**Parameters:**
- `config` (`SimulationConfig`): The configuration object of simulation.
- `rng` (`np.random.Generator`): RNG with specified seed for reproducibility. If not specified, new instance with unspecified seed will be initiated.

**Returns:**
- `x` (`numpy.ndarray`): Position array of $x$-coordinate, of shape `(num_steps,)`.
- `vx` (`numpy.ndarray`): Velocity array of $x$-coordinate, of shape `(num_steps,)`.
- `y` (`numpy.ndarray`): Position array of $y$-coordinate, of shape `(num_steps,)`.
- `vy` (`numpy.ndarray`): Velocity array of $y$-coordinate, of shape `(num_steps,)`.

### `LSolver.mixed`

```python
LSolver.underdamped(config: SimulationConfig, rng: numpy.random.Generator = None) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]
```
Simulates Langevin equation, overdamped in $x$-coordinate and underdamped in $y$-coordinate, using Euler-Maruyama and Verlet-type [1] algorithms.

**Parameters:**
- `config` (`SimulationConfig`): The configuration object of simulation.
- `rng` (`np.random.Generator`): RNG with specified seed for reproducibility. If not specified, new instance with unspecified seed will be initiated.

**Returns:**
- `x` (`numpy.ndarray`): Position array of $x$-coordinate, of shape `(num_steps,)`.
- `y` (`numpy.ndarray`): Position array of $y$-coordinate, of shape `(num_steps,)`.
- `vy` (`numpy.ndarray`): Velocity array of $y$-coordinate, of shape `(num_steps,)`.

---

## References

[1] Grønbech-Jensen, N., & Farago, O. (2013). A simple and effective Verlet-type algorithm for simulating Langevin dynamics. Molecular Physics, 111(8), 983–991. Available at: https://doi.org/10.1080/00268976.2012.760055