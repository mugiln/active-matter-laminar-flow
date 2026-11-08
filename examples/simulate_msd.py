"""
Demonstration: Mean Squared Displacement (MSD) and Transport Scaling.
Quantifies spreading dynamics <|r(t) - r(0)|^2> ~ t^beta from ballistic expansion to vortex-confined saturation.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from active_matter import simulate_ensemble, compute_msd, fit_diffusion_exponent, set_visual_style


def run_msd_simulation(num_particles=1000, timesteps=10000, nsave=50, dt=0.01, output_dir="output"):
    """
    Computes ensemble MSD curves for passive tracers (vp = 0.0) up to active swimmers (vp = 0.30).
    Fits power-law exponent beta to classify anomalous transport regimes.
    """
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    
    velocities = [0.0, 0.05, 0.15, 0.30]
    msd_results = {}
    time_array = None
    
    X0 = np.random.uniform(0.0, 2.0 * np.pi, size=(num_particles, 3))
    
    for vp in velocities:
        print(f"Simulating MSD for self-propulsion speed vp = {vp:.2f}...")
        # Unwrapped coordinate simulation preserves absolute spatial dispersion
        trajectories, times = simulate_ensemble(
            X0, dt=dt, nt=timesteps, nsave=nsave, U0=1.0, vp=vp, alpha=0.95, wrap_pbc=False
        )
        time_array = times
        msd = compute_msd(trajectories)
        msd_results[f"$v_p = {vp:.2f}$"] = msd
        
        # Fit power-law exponent beta during the initial unconfined regime
        fit = fit_diffusion_exponent(times, msd, t_min=0.5, t_max=10.0)
        print(f"  Early-time scaling exponent beta = {fit['beta']:.2f} (R^2 = {fit['r_squared']:.3f})")
        
    # Render log-log plot
    set_visual_style(dark_mode=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#ff595e", "#1982c4", "#6a4c93", "#ffca3a"]
    
    for (label, msd), c in zip(msd_results.items(), colors):
        ax.loglog(time_array, msd, label=label, color=c, linewidth=2.0)
        
    ax.set_xlabel("Time (t)", color="white", fontsize=11)
    ax.set_ylabel(r"MSD $\langle |\mathbf{r}(t) - \mathbf{r}(0)|^2 \rangle$", color="white", fontsize=11)
    ax.set_title(r"Mean Squared Displacement vs Time ($\alpha = 0.95$)", color="white", fontsize=12)
    ax.grid(True, linestyle=":", alpha=0.4, color="gray")
    ax.legend(facecolor="black", edgecolor="white")
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, "msd_scaling_loglog.png")
    plt.savefig(save_path, dpi=300, facecolor="black")
    plt.close()
    print(f"MSD analysis complete! Saved to '{save_path}'.")


if __name__ == "__main__":
    run_msd_simulation()
