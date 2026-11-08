"""
Demonstration: Minimum Swimming Velocity for Vortex Escape vs Particle Shape.
Shows how elongated particles (high alpha) leverage shear alignment to escape vortex traps at lower propulsion speeds.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from active_matter import simulate_ensemble, compute_escape_fraction, set_visual_style


def find_minimum_escape_velocity(
    alpha_values=np.linspace(0.1, 0.95, 6),
    num_particles=500,
    timesteps=2000,
    dt=0.01,
    escape_threshold=0.8,
    output_dir="output",
):
    """
    Computes critical propulsion speed v_p required for >= 80% of particles to cross vortex boundaries.
    Iteratively sweeps velocities to determine the escape barrier for each particle eccentricity.
    """
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    
    # Confine initial particles within the central region of the lower-left vortex [0, pi]
    X0 = np.random.uniform(0.2 * np.pi, 0.8 * np.pi, size=(num_particles, 3))
    
    critical_velocities = []
    test_velocities = np.linspace(0.02, 0.35, 12)
    
    print(f"Sweeping escape threshold across alpha values: {np.round(alpha_values, 2)}...")
    for alpha in alpha_values:
        v_crit = test_velocities[-1]
        for vp in test_velocities:
            # Evolve particles under current shape and propulsion speed without PBC wrapping
            traj, _ = simulate_ensemble(
                X0, dt=dt, nt=timesteps, nsave=timesteps, U0=1.0, vp=vp, alpha=alpha, wrap_pbc=False
            )
            # Check what percentage crossed the vortex border at x = pi or y = pi
            escaped_frac = compute_escape_fraction(X0, traj[-1], vortex_size=np.pi)
            if escaped_frac >= escape_threshold:
                v_crit = vp
                break
        critical_velocities.append(v_crit)
        print(f"  alpha = {alpha:.2f} -> Minimum escape speed v_p = {v_crit:.3f}")
        
    # Plot critical velocity as a function of particle shape eccentricity
    set_visual_style()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot(alpha_values, critical_velocities, "o-", color="#e63946", linewidth=2.0, markersize=6)
    ax.set_xlabel(r"Particle Eccentricity $\alpha$ (Shape Anisotropy)")
    ax.set_ylabel(r"Critical Escape Velocity $v_p^{crit}$")
    ax.set_title("Vortex Escape Threshold vs Particle Shape", fontsize=12)
    ax.grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, "escape_velocity_vs_eccentricity.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Results saved to '{save_path}'.")


if __name__ == "__main__":
    find_minimum_escape_velocity()
