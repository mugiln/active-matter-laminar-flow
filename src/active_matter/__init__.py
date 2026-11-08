"""
active_matter: Simulation and non-linear dynamics of self-propelled particles in fluid flows.

Provides flow fields, particle dynamics (Jeffrey's equation for ellipsoids),
Runge-Kutta integrators, and statistical analysis tools (MSD, Lyapunov exponents, vorticity ratios).
"""

from .flow import cellular_velocity, compute_vorticity, compute_strain_tensor
from .dynamics import particle_derivatives, eccentricity_from_aspect_ratio
from .integrator import rk2_step, simulate_ensemble
from .analysis import (
    compute_msd,
    fit_diffusion_exponent,
    compute_vorticity_pdf_ratio,
    compute_escape_fraction,
    compute_finite_time_lyapunov,
)
from .visualization import (
    plot_particles_2d,
    plot_quiver_field,
    plot_msd_scaling,
    set_visual_style,
)

__all__ = [
    "cellular_velocity",
    "compute_vorticity",
    "compute_strain_tensor",
    "particle_derivatives",
    "eccentricity_from_aspect_ratio",
    "rk2_step",
    "simulate_ensemble",
    "compute_msd",
    "fit_diffusion_exponent",
    "compute_vorticity_pdf_ratio",
    "compute_escape_fraction",
    "compute_finite_time_lyapunov",
    "plot_particles_2d",
    "plot_quiver_field",
    "plot_msd_scaling",
    "set_visual_style",
]
