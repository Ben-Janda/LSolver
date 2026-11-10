import numpy as np
import pytest
from LSolver import SimulationConfig, overdamped, underdamped, mixed

def dummy_force(t, x, y):
    return 0.0

def dummy_temp(t, x, y):
    return 1.0

@pytest.fixture
def config_for_shapes():
    return SimulationConfig(
        gamma = 1.0,
        Fx_func = dummy_force,
        Fy_func = dummy_force,
        Tx_func = dummy_temp,
        Ty_func = dummy_temp,
        t_max = 5.0,
        dt = 0.1,
        m = 1.0
    )

@pytest.mark.parametrize("solver_func", [overdamped, underdamped, mixed])
def test_output_shapes_and_types(config_for_shapes, solver_func):
    result = solver_func(config_for_shapes)
    
    assert isinstance(result, tuple)
    
    expected_length = config_for_shapes.num_steps
    for arr in result:
        assert isinstance(arr, np.ndarray)
        assert len(arr) == expected_length
        
@pytest.mark.parametrize("solver_func", [overdamped, underdamped, mixed])
def test_no_nans_or_infs(config_for_shapes, solver_func):
    result = solver_func(config_for_shapes)
    
    for arr in result:
        assert not np.isnan(arr).any()
        assert not np.isinf(arr).any()