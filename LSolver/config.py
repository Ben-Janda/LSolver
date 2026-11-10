from dataclasses import dataclass, field
from typing import Callable
import numpy as np

TimeDependentFunc = Callable[[float, float, float],float]
            
@dataclass(frozen=True)
class SimulationConfig:
    """Configuration of physical paramaters and discretization"""
    # Physical parameters
    gamma: float
    Fx_func: TimeDependentFunc
    Tx_func: TimeDependentFunc
    
    # Discretization
    t_max: float
    dt: float
    m: float = None
    x0: float = 0.0
    vx0: float = 0.0
    y0: float = 0.0
    vy0: float = 0.0
    
    # Physical parameters of y (optional)
    Fy_func: TimeDependentFunc = lambda t,x,y : 0.0
    Ty_func: TimeDependentFunc = lambda t,x,y : 0.0
    
    
    # For evaluation
    t_array: np.ndarray = field(init=False, repr=False)
    num_steps: int = field(init=False, repr=False)
    
    def __post_init__(self):
        if self.gamma <= 0:
            raise ValueError("Friction coefficient gamma has to be positive.")
        if self.dt <= 0:
            raise ValueError("Timestep dt has to be positive.")
        if self.m is not None and self.m <= 0:
            raise ValueError("Mass m has to be positive.")
        if self.t_max <= 0:
            raise ValueError("End time of simulation t_max has to be greater than zero.")
        
        n_steps = int(np.ceil(self.t_max / self.dt)) + 1
        t_arr = np.arange(n_steps) * self.dt
        
        object.__setattr__(self, 'num_steps', n_steps)
        object.__setattr__(self, 't_array', t_arr)