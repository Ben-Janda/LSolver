import numpy as np
import pytest
from LSolver import SimulationConfig, overdamped, underdamped

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
        x0 = 0.0,
        y0 = 0.0
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
    
def test_underdamped_free_diffusion_with_friction_symmetry():
    config = SimulationConfig(
        gamma = 1.0,
        Fx_func = dummy_force,
        Fy_func = dummy_force,
        Tx_func = dummy_temp,
        Ty_func = dummy_temp,
        t_max = 5.0,
        dt = 0.01,
        x0 = 0.0,
        vx0 = 0.0,
        y0 = 0.0,
        vy0 = 0.0,
        m = 1.0
    )
    
    n_sim = 100
    final_velocities_x = np.empty(n_sim)
    final_velocities_y = np.empty(n_sim)
    
    master_rng = np.random.default_rng(42)
    child_rng = master_rng.spawn(n_sim)
    
    for i in range(n_sim):
        sub_rng = child_rng[i]
        x, vx, y, vy = underdamped(config, rng = sub_rng)
        
        final_velocities_x[i] = vx[-1]
        final_velocities_y[i] = vy[-1]
    
    mean_final_x = np.mean(final_velocities_x)
    mean_final_y = np.mean(final_velocities_y)
    
    assert mean_final_x == pytest.approx(0.0, abs = 0.1)
    assert mean_final_y == pytest.approx(0.0, abs = 0.1)