import pytest
import numpy as np
from LSolver.config import SimulationConfig

def zeros(t: float, x: float, y: float) -> float:
    return 0.0

def test_SimulationConfig_initialization():
    cfg = SimulationConfig(
        gamma = 1.5,
        Fx_func = zeros,
        Tx_func = zeros,
        t_max = 1.0,
        dt = 0.1
    )
    
    assert cfg.num_steps == 11
    
    assert isinstance(cfg.t_array, np.ndarray)
    assert len(cfg.t_array) == 11
    
    assert cfg.t_array[0] == pytest.approx(0.0)
    assert cfg.t_array[-1] == pytest.approx(1.0)
    
def test_invalid_gamma_raises_error():
    with pytest.raises(ValueError, match = "Friction coefficient gamma has to be positive."):
        SimulationConfig(
            gamma = -0.5,
            Fx_func = zeros,
            Tx_func = zeros,
            t_max = 1.0,
            dt = 0.1
        )

    with pytest.raises(ValueError):
        SimulationConfig(
            gamma = 0.0,
            Fx_func = zeros,
            Tx_func = zeros,
            t_max = 1.0,
            dt = 0.1
        )
        
def test_invalid_dt_raises_error():
    with pytest.raises(ValueError, match = "Timestep dt has to be positive."):
        SimulationConfig(
            gamma = 1.0,
            Fx_func = zeros,
            Tx_func = zeros,
            t_max = 1.0,
            dt = -0.01
        )
        
    with pytest.raises(ValueError):
        SimulationConfig(
            gamma = 1.0,
            Fx_func = zeros,
            Tx_func = zeros,
            t_max = 1.0,
            dt = 0.0
        )
            
def test_default_values():
    cfg = SimulationConfig(
        gamma = 1.0,
        Fx_func = zeros,
        Tx_func = zeros,
        t_max = 1.0,
        dt = 0.1
    )
    
    assert cfg.x0 == 0.0
    assert cfg.vx0 == 0.0
    assert cfg.y0 == 0.0
    assert cfg.vy0 == 0.0
    assert cfg.m is None
    
def test_invalid_mass_raises_error():
    with pytest.raises(ValueError, match = "Mass m has to be positive."):
        SimulationConfig(
            gamma = 1.0,
            Fx_func = zeros,
            Tx_func = zeros,
            t_max = 1.0,
            dt = 0.1,
            m = -1.0
        )
        
    with pytest.raises(ValueError, match = "Mass m has to be positive."):
        SimulationConfig(
            gamma = 1.0,
            Fx_func = zeros,
            Tx_func = zeros,
            t_max = 1.0,
            dt = 0.1,
            m = 0.0
        )

def test_explicit_none_mass():
    cfg = SimulationConfig(
        gamma=1.0,
        Fx_func=zeros,
        Tx_func=zeros,
        t_max=1.0,
        dt=0.1,
        m=None
    )
    assert cfg.m is None
    
def test_negative_t_max_raises_error():
    with pytest.raises(ValueError, match = "End time of simulation t_max has to be greater than zero."):
        SimulationConfig(
            gamma=1.0,
            Fx_func=zeros,
            Tx_func=zeros,
            t_max=-1.0,
            dt=0.1
        )
    