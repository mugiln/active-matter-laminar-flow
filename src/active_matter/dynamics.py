"""
Non-linear equations of motion for self-propelled ellipsoidal microswimmers.
Integrates Jeffrey's equation for shape alignment, intrinsic chirality, and rotational Brownian noise.
"""

import numpy as np
from .flow import cellular_velocity


def eccentricity_from_aspect_ratio(gamma):
    """
    Computes Bretherton/Jeffrey alignment parameter alpha = (gamma^2 - 1) / (gamma^2 + 1).
    alpha = 0 for spheres (gamma = 1); alpha -> 1 for slender rods (gamma >> 1).
    """
    gamma_sq = gamma ** 2
    return (gamma_sq - 1.0) / (gamma_sq + 1.0)


def particle_derivatives(X, t, U0=1.0, vp=0.1, alpha=0.0, B=0.0, nu=2.0 * np.pi, chirality=0.0, Dr=0.0, dt=0.01):
    """
    Computes time derivatives [dx/dt, dy/dt, dtheta/dt] for an ensemble of N particles.
    X has shape (N, 3) where columns correspond to [x, y, theta].
    """
    N = len(X)
    rhs = np.zeros_like(X)
    
    # Hydrodynamic advection velocity evaluated at each particle position
    v_flow = cellular_velocity(X[:, 0], X[:, 1], t=t, U0=U0, B=B, nu=nu)
    
    # Translational motion: flow advection plus autonomous self-propulsion along orientation theta
    rhs[:, 0] = v_flow[:, 0] + vp * np.cos(X[:, 2])
    rhs[:, 1] = v_flow[:, 1] + vp * np.sin(X[:, 2])
    
    # Vorticity-induced background rotation (fluid shear turning the particle)
    vorticity_torque = U0 * np.sin(X[:, 0]) * np.sin(X[:, 1])
    
    # Jeffrey alignment torque: couples elongated particle shape (alpha) to local fluid strain
    shape_alignment = -alpha * np.cos(X[:, 0]) * np.cos(X[:, 1]) * np.sin(2.0 * X[:, 2])
    
    # Rotational Brownian motion: Gaussian white noise simulating thermal solvent collisions
    stochastic_noise = np.sqrt(2.0 * Dr / dt) * np.random.normal(0.0, 1.0, size=N) if Dr > 0.0 else 0.0
    
    # Total orientation rate of change: vorticity + shape torque + intrinsic chirality + noise
    rhs[:, 2] = vorticity_torque + shape_alignment + chirality + stochastic_noise
    
    return rhs


def phase_space_divergence(x, y, theta, alpha=0.0):
    """
    Calculates phase space divergence div(V) = d(x_dot)/dx + d(y_dot)/dy + d(theta_dot)/dtheta.
    Zero for spheres (Liouville volume-preserving); non-zero for ellipsoids (phase space contraction).
    """
    return -2.0 * alpha * np.cos(x) * np.cos(y) * np.cos(2.0 * theta)
