import numpy as np
from .config import SimulationConfig

def overdamped(config: SimulationConfig, rng: np.random.Generator = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate single trajectory x(t) and stochastic time y(t)

    Parameters
    ----------
    config : SimulationConfig
        Configuration of the simulation.
    rng : np.random.Generator
        Optional rng for reproducibility.

    Returns
    -------
    Tuple (x(t), y(t)).
    """
    if rng is None:
        rng = np.random.default_rng()
    
    N = config.num_steps
    dt = config.dt
    gamma = config.gamma
    t_arr = config.t_array
    
    x = np.empty(N)
    y = np.empty(N)
    x[0] = config.x0
    y[0] = config.y0
    eta_x = rng.normal(0, 1, N-1)
    eta_y = rng.normal(0, 1, N-1)
    
    for i in range(N-1):
        t = t_arr[i]
        Fxt = config.Fx_func(t, x[i], y[i])
        Fyt = config.Fy_func(t, x[i], y[i])
        Txt = config.Tx_func(t, x[i], y[i])
        Tyt = config.Ty_func(t, x[i], y[i])
        
        dx = Fxt * dt / gamma + np.sqrt(2*Txt*dt / gamma) * eta_x[i]
        dy = Fyt * dt / gamma + np.sqrt(2*Tyt*dt / gamma) * eta_y[i]
        
        x[i+1] = x[i] + dx
        y[i+1] = y[i] + dy
        
    return x, y

def underdamped(config: SimulationConfig, rng: np.random.Generator = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    

    Parameters
    ----------
    config : SimulationConfig
        DESCRIPTION.
    rng : np.random.Generator, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    x : TYPE
        DESCRIPTION.
    vx : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    vy : TYPE
        DESCRIPTION.

    """
    if rng is None:
        rng = np.random.default_rng()
        
    if config.m is None:
        raise ValueError("Mass of the particle not specified.")
    
    N = config.num_steps
    dt = config.dt
    gamma = config.gamma
    t_arr = config.t_array
    m = config.m
    
    b = 1/(1 + gamma * dt / (2*m))
    a = b*(1 - gamma * dt / (2*m))
    
    x = np.empty(N)
    y = np.empty(N)
    vx = np.empty(N)
    vy = np.empty(N)
    x[0] = config.x0
    y[0] = config.y0
    vx[0] = config.vx0
    vy[0] = config.vy0
    eta_x = rng.normal(0, 1, N-1)
    eta_y = rng.normal(0, 1, N-1)
    
    for i in range(N-1):
        t = t_arr[i]
        Fxt = config.Fx_func(t, x[i], y[i])
        Fyt = config.Fy_func(t, x[i], y[i])
        Txt = config.Tx_func(t, x[i], y[i])
        Tyt = config.Ty_func(t, x[i], y[i])
        
        dx = b * vx[i] * dt + b * dt**2 * Fxt / (2*m) + b * dt * np.sqrt(2*Txt*dt * gamma) * eta_x[i] / (2*m)
        x[i+1] = x[i] + dx
        dy = b * vy[i] * dt + b * dt**2 * Fyt / (2*m) + b * dt * np.sqrt(2*Tyt*dt * gamma) * eta_y[i] / (2*m)
        y[i+1] = y[i] + dy
        Fxtp = config.Fx_func(t+dt, x[i+1], y[i+1])
        Fytp = config.Fy_func(t+dt, x[i+1], y[i+1])
        
        vx[i+1] = a * vx[i] + dt * (a * Fxt + Fxtp) / (2*m) + b * np.sqrt(2*Txt*dt * gamma) * eta_x[i]/m
        vy[i+1] = a * vy[i] + dt * (a * Fyt + Fytp) / (2*m) + b * np.sqrt(2*Tyt*dt * gamma) * eta_y[i]/m
        
    return x, vx, y, vy

def mixed(config: SimulationConfig, rng: np.random.Generator = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    

    Parameters
    ----------
    config : SimulationConfig
        DESCRIPTION.
    rng : np.random.Generator, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    vy : TYPE
        DESCRIPTION.

    """
    if rng is None:
        rng = np.random.default_rng()
        
    if config.m is None:
        raise ValueError("Mass of the particle not specified.")
    
    N = config.num_steps
    dt = config.dt
    gamma = config.gamma
    t_arr = config.t_array
    m = config.m
    
    b = 1/(1 + gamma * dt / (2*m))
    a = b*(1 - gamma * dt / (2*m))
    
    x = np.empty(N)
    y = np.empty(N)
    vy = np.empty(N)
    x[0] = config.x0
    y[0] = config.y0
    vy[0] = config.vy0
    eta_x = rng.normal(0, 1, N-1)
    eta_y = rng.normal(0, 1, N-1)

    for i in range(N-1):
        t = t_arr[i]
        Fxt = config.Fx_func(t, x[i], y[i])
        Fyt = config.Fy_func(t, x[i], y[i])
        Txt = config.Tx_func(t, x[i], y[i])
        Tyt = config.Ty_func(t, x[i], y[i])
        
        dx = Fxt * dt / gamma + np.sqrt(2*Txt*dt / gamma) * eta_x[i]
        x[i+1] = x[i] + dx
        dy = b * vy[i] * dt + b * dt**2 * Fyt / (2*m) + b * dt * np.sqrt(2*Tyt*dt * gamma) * eta_y[i] / (2*m)
        y[i+1] = y[i] + dy
        Fytp = config.Fy_func(t+dt, x[i+1], y[i+1])
        
        vy[i+1] = a * vy[i] + dt * (a * Fyt + Fytp) / (2*m) + b * np.sqrt(2*Tyt*dt * gamma) * eta_y[i]/m
        
    return x, y, vy