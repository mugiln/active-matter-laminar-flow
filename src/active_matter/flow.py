"""
Cellular flow field definitions and hydrodynamic field computations.
Models 2D vortex arrays derived from streamfunctions with optional time-dependent lateral oscillations.
"""

import numpy as np


def cellular_velocity(x, y, t=0.0, U0=1.0, B=0.0, nu=2.0 * np.pi, L=2.0 * np.pi):
    """
    Computes velocity components (vx, vy) for a 2D cellular vortex array.
    Derived from streamfunction psi = (U0 * L / 2pi) * sin(2pi(x - B sin(nu t))/L) * sin(2pi y / L).
    """
    k = 2.0 * np.pi / L
    # Lateral oscillation shifts the separatrix boundaries periodically in time
    x_shift = B * np.sin(nu * t)
    
    vx = U0 * np.sin(k * (x - x_shift)) * np.cos(k * y)
    vy = -U0 * np.cos(k * (x - x_shift)) * np.sin(k * y)
    
    if np.isscalar(x) and np.isscalar(y):
        return np.array([vx, vy])
    return np.column_stack((vx, vy))


def compute_vorticity(x, y, U0=1.0, L=2.0 * np.pi):
    """
    Computes the scalar fluid vorticity omega = d(vy)/dx - d(vx)/dy.
    Measures local fluid rotation in the 2D plane (alternating checkerboard pattern).
    """
    k = 2.0 * np.pi / L
    return 2.0 * k * U0 * np.sin(k * x) * np.sin(k * y)


def compute_strain_tensor(x, y, U0=1.0, L=2.0 * np.pi):
    """
    Calculates rate-of-strain tensor components E_xx, E_yy, E_xy = 0.5 * (dv_i/dx_j + dv_j/dx_i).
    Governs shape alignment and hydrodynamic torque acting on elongated particles.
    """
    k = 2.0 * np.pi / L
    # Diagonal strain components (pure extension / compression)
    E_xx = k * U0 * np.cos(k * x) * np.cos(k * y)
    E_yy = -E_xx  # Incompressibility enforces div(v) = 0
    # Off-diagonal shear strain component
    E_xy = 0.5 * (-k * U0 * np.sin(k * x) * np.sin(k * y) - k * U0 * np.sin(k * x) * np.sin(k * y))
    return E_xx, E_yy, E_xy
