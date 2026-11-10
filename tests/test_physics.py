import numpy as np
import pytest
from LSolver import SimulationConfig, overdamped

def dummy_force(t, x, y):
    return 0.0

def dummy_temp(t, x, y):
    return 1.0

def test_overdamped_free_diffusion_symmetry():
    config = SimulationConfig(
        gamma = 1.0,
        Fx_func = dummy_force,
        Fy_func = dummy_force,
        Tx_func = dummy_temp,
        Ty_func = dummy_temp,
        t_max = 5.0,
        dt = 0.01,
        x0 = 0.0
    )
    
    n_sim = 100
    final_positions_x = np.empty(n_sim)
    final_positions_y = np.empty(n_sim)
    
    master_rng = np.random.default_rng(42)
    
    for i in range(n_sim):
        sub_rng = np.random.default_rng(master_rng.integers(0, 1000000))
        x, y = overdamped(config, rng = sub_rng)
        
        final_positions_x[i] = x[-1]
        final_positions_y[i] = y[-1]
    
    mean_final_x = np.mean(final_positions_x)
    mean_final_y = np.mean(final_positions_y)
    
    assert mean_final_x == pytest.approx(0.0, abs = 0.5)
    assert mean_final_y == pytest.approx(0.0, abs = 0.5)