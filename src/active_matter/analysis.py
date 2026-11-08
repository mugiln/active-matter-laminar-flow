"""
Quantitative statistical analysis and non-linear dynamics diagnostic tools.
Computes Mean Squared Displacement (MSD), Lyapunov chaos exponents, escape ratios, and vorticity PDF ratios.
"""

import numpy as np
from scipy.stats import linregress


def compute_msd(trajectories):
    """
    Computes ensemble Mean Squared Displacement (MSD) <|r(t) - r(0)|^2> across all particles.
    Expects unwrapped trajectories of shape (n_snapshots, N, 3).
    """
    initial_positions = trajectories[0, :, :2]
    # Calculate displacement vector from t=0 origin for each particle
    displacements = trajectories[:, :, :2] - initial_positions[np.newaxis, :, :]
    squared_displacements = np.sum(displacements ** 2, axis=2)
    # Average across all particles in the ensemble
    return np.mean(squared_displacements, axis=1)


def fit_diffusion_exponent(time, msd, t_min=None, t_max=None):
    """
    Fits power-law scaling MSD ~ t^beta using linear regression on log-log data.
    beta = 2: Ballistic; beta = 1: Normal Brownian diffusion; beta < 1: Sub-diffusive / Trapped.
    """
    valid_mask = (time > 0.0) & (msd > 0.0) & np.isfinite(time) & np.isfinite(msd)
    if t_min is not None:
        valid_mask &= (time >= t_min)
    if t_max is not None:
        valid_mask &= (time <= t_max)
        
    log_t = np.log(time[valid_mask])
    log_msd = np.log(msd[valid_mask])
    
    slope, intercept, r_value, p_value, std_err = linregress(log_t, log_msd)
    return {
        "beta": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "std_err": std_err,
    }


def compute_escape_fraction(initial_coords, current_coords, vortex_size=np.pi):
    """
    Calculates the fraction of particles that have escaped their initial vortex cell.
    Vortex cells in the 2D periodic grid are indexed by quadrant boundaries at integer multiples of pi.
    """
    # Discretize domain into vortex quadrant IDs
    vortex_init = (initial_coords[:, 0] // vortex_size).astype(int) + 2 * (initial_coords[:, 1] // vortex_size).astype(int)
    vortex_curr = (current_coords[:, 0] // vortex_size).astype(int) + 2 * (current_coords[:, 1] // vortex_size).astype(int)
    
    escaped_mask = (vortex_init != vortex_curr)
    return np.mean(escaped_mask)


def compute_vorticity_pdf_ratio(vorticity_active, vorticity_uniform, nbins=30, vrange=None):
    """
    Computes ratio R(omega) = P(omega) / P0(omega) to isolate chirality-induced flow sampling bias.
    Normalizing against uniform spatial sampling cancels out geometric distribution artifacts.
    """
    if vrange is None:
        vrange = (
            min(np.min(vorticity_active), np.min(vorticity_uniform)),
            max(np.max(vorticity_active), np.max(vorticity_uniform)),
        )
        
    pdf_active, edges = np.histogram(vorticity_active, bins=nbins, density=True, range=vrange)
    pdf_uniform, _ = np.histogram(vorticity_uniform, bins=nbins, density=True, range=vrange)
    
    bin_centers = 0.5 * (edges[:-1] + edges[1:])
    # Small epsilon prevents division by zero in sparsely sampled tails
    epsilon = 1e-10
    pdf_ratio = pdf_active / (pdf_uniform + epsilon)
    
    return bin_centers, pdf_ratio, pdf_active, pdf_uniform


def compute_finite_time_lyapunov(traj_base, traj_perturbed, dt, t_max=None):
    """
    Calculates Finite-Time Lyapunov Exponent (FTLE) from exponential divergence of nearby trajectories.
    Measures sensitivity to initial conditions: delta(t) = delta(0) * exp(lambda * t).
    """
    # Euclidean distance between base and perturbed particle trajectories in phase space
    diff = traj_base - traj_perturbed
    separation = np.sqrt(np.sum(diff ** 2, axis=1))
    
    times = np.arange(len(separation)) * dt
    valid_mask = (times > 0.0) & (separation > 0.0)
    if t_max is not None:
        valid_mask &= (times <= t_max)
        
    log_sep = np.log(separation[valid_mask])
    t_clean = times[valid_mask]
    
    slope, intercept, r_value, _, std_err = linregress(t_clean, log_sep)
    return {
        "lyapunov_exponent": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "std_err": std_err,
        "times": times,
        "separation": separation,
    }
