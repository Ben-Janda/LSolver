import numpy as np
import pytest
from LSolver import SimulationConfig, overdamped, underdamped, mixed

def dummy_force(t, x, y):
    return -1.0 * x

def dummy_temp(t, x, y):
    return 1.0

@pytest.fixture
def basic_config():
    return SimulationConfig(
        gamma = 1.0,
        Fx_func = dummy_force,
        Fy_func = dummy_force,
        Tx_func = dummy_temp,
        Ty_func = dummy_temp,
        t_max = 1.0,
        dt = 0.1,
        m = 1.0
    )

def test_overdamped_reproducibility(basic_config):
    rng_1 = np.random.default_rng(123)
    out1 = overdamped(basic_config, rng=rng_1)
    
    rng_2 = np.random.default_rng(123)
    out2 = overdamped(basic_config, rng=rng_2)
    
    for arr1, arr2 in zip(out1, out2):
        np.testing.assert_array_equal(arr1, arr2)
    
def test_underdamped_reproducibility(basic_config):
    rng_1 = np.random.default_rng(42)
    out1 = underdamped(basic_config, rng=rng_1)
    
    rng_2 = np.random.default_rng(42)
    out2 = underdamped(basic_config, rng=rng_2)
    
    for arr1, arr2 in zip(out1, out2):
        np.testing.assert_array_equal(arr1, arr2)
        
def test_mixed_reproducibility(basic_config):
    rng_1 = np.random.default_rng(2048)
    out1 = mixed(basic_config, rng=rng_1)
    
    rng_2 = np.random.default_rng(2048)
    out2 = mixed(basic_config, rng=rng_2)
    
    for arr1, arr2 in zip(out1, out2):
        np.testing.assert_array_equal(arr1, arr2)

@pytest.mark.parametrize("solver_func", [overdamped, underdamped, mixed])
def test_differents_seeds_produce_different_results(basic_config, solver_func):
    rng_a = np.random.default_rng(123)
    out_a = solver_func(basic_config, rng = rng_a)
    
    rng_b = np.random.default_rng(456)
    out_b = solver_func(basic_config, rng=rng_b)
    
    for arr1, arr2 in zip(out_a, out_b):
        with pytest.raises(AssertionError):
            np.testing.assert_array_equal(arr1, arr2)

@pytest.mark.parametrize("solver_func", [overdamped, underdamped, mixed])
def test_simulation_invariance_on_t_max(solver_func):
    dt_val = 0.05
    seed_val = 42
    
    cfg_short = SimulationConfig(
        gamma = 1.0,
        Fx_func = dummy_force,
        Fy_func = dummy_force,
        Tx_func = dummy_temp,
        Ty_func = dummy_temp,
        t_max = 1.0,
        dt = dt_val,
        m = 1.0
    )
    
    cfg_long = SimulationConfig(
        gamma = 1.0,
        Fx_func = dummy_force,
        Fy_func = dummy_force,
        Tx_func = dummy_temp,
        Ty_func = dummy_temp,
        t_max = 2.0,
        dt = dt_val,
        m = 1.0
    )
    
    rng_1 = np.random.default_rng(seed_val)
    res_short = solver_func(cfg_short, rng=rng_1)
    
    rng_2 = np.random.default_rng(seed_val)
    res_long = solver_func(cfg_long, rng=rng_2)
    
    n_short_steps = cfg_short.num_steps
    
    for arr_short, arr_long in zip(res_short, res_long):
        arr_long_trunc = arr_long[:n_short_steps]
        np.testing.assert_array_equal(arr_short, arr_long_trunc)