"""
Vectorized numerical integrators for multi-particle active matter simulations.
Implements 2nd-order Runge-Kutta (RK2 / Heun's method) for deterministic and stochastic ensembles.
"""

import numpy as np
from .dynamics import particle_derivatives


def rk2_step(X, t, dt, U0=1.0, vp=0.1, alpha=0.0, B=0.0, nu=2.0 * np.pi, chirality=0.0, Dr=0.0):
    """
    Advances particle state [x, y, theta] by one timestep using 2nd-order Runge-Kutta (RK2).
    Predictor-corrector scheme maintains second-order numerical accuracy.
    """
    # Predictor step: estimate slope at beginning of interval
    k1 = dt * particle_derivatives(X, t, U0=U0, vp=vp, alpha=alpha, B=B, nu=nu, chirality=chirality, Dr=Dr, dt=dt)
    
    # Corrector step: evaluate slope at estimated midpoint
    k2 = dt * particle_derivatives(X + 0.5 * k1, t + 0.5 * dt, U0=U0, vp=vp, alpha=alpha, B=B, nu=nu, chirality=chirality, Dr=Dr, dt=dt)
    
    return X + k2


def simulate_ensemble(
    X0,
    dt=0.01,
    nt=10000,
    nsave=100,
    U0=1.0,
    vp=0.1,
    alpha=0.0,
    B=0.0,
    nu=2.0 * np.pi,
    chirality=0.0,
    Dr=0.0,
    wrap_pbc=False,
    L=2.0 * np.pi,
):
    """
    Evolves an ensemble of N particles over nt timesteps, logging trajectories at every nsave interval.
    Returns array of recorded states with shape (n_snapshots, N, 3) and corresponding time array.
    """
    X = np.copy(X0)
    t = 0.0
    
    recorded_states = [np.copy(X)]
    recorded_times = [t]
    
    for it in range(1, nt + 1):
        X = rk2_step(X, t, dt, U0=U0, vp=vp, alpha=alpha, B=B, nu=nu, chirality=chirality, Dr=Dr)
        t += dt
        
        # Periodic boundary condition wrapping on positions if requested
        if wrap_pbc:
            X[:, 0] = np.mod(X[:, 0], L)
            X[:, 1] = np.mod(X[:, 1], L)
            X[:, 2] = np.mod(X[:, 2] + np.pi, 2.0 * np.pi) - np.pi
            
        if it % nsave == 0:
            recorded_states.append(np.copy(X))
            recorded_times.append(t)
            
    return np.array(recorded_states), np.array(recorded_times)
