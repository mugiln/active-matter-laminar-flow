"""
Demonstration: Non-Linear Chaos and Finite-Time Lyapunov Exponents.
Measures exponential divergence of initially nearby trajectories to quantify sensitivity to initial conditions.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from active_matter import simulate_ensemble, compute_finite_time_lyapunov, set_visual_style


def run_chaos_quantification(timesteps=2000, dt=0.005, output_dir="output"):
    """
    Evolves pairs of trajectories with tiny initial perturbation delta_0 = 1e-5.
    Extracts the Finite-Time Lyapunov Exponent lambda from exponential separation rate.
    """
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    
    # Base starting condition and tiny initial displacement perturbation
    X_base = np.array([[1.0, 1.0, np.pi / 2.0]])
    delta_0 = 1e-5
    X_pert = X_base + np.array([[delta_0, delta_0, delta_0]])
    
    velocities = [0.1, 0.5, 1.0]
    lyapunov_results = {}
    
    for vp in velocities:
        # Evolve base and perturbed state simultaneously
        X_combined = np.vstack((X_base, X_pert))
        traj, times = simulate_ensemble(
            X_combined, dt=dt, nt=timesteps, nsave=1, U0=1.0, vp=vp, alpha=0.0, wrap_pbc=False
        )
        
        traj_b = traj[:, 0, :]
        traj_p = traj[:, 1, :]
        
        # Calculate separation growth and fit exponential slope
        result = compute_finite_time_lyapunov(traj_b, traj_p, dt=dt, t_max=4.0)
        lyapunov_results[vp] = result
        print(f"  Propulsion vp = {vp:.1f} -> Lyapunov Exponent lambda = {result['lyapunov_exponent']:.3f}")
        
    # Plot log of perturbation separation over time
    set_visual_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    palette = ["#1d3557", "#457b9d", "#e63946"]
    
    for (vp, res), color in zip(lyapunov_results.items(), palette):
        times = res["times"]
        sep = res["separation"]
        mask = times <= 4.0
        ax.plot(times[mask], np.log(sep[mask] / delta_0), label=rf"$v_p = {vp:.1f}$ ($\lambda = {res['lyapunov_exponent']:.2f}$)", color=color, linewidth=2.0)
        
    ax.set_xlabel("Time (t)")
    ax.set_ylabel(r"Log Divergence $\ln(|\delta(t)| / |\delta(0)|)$")
    ax.set_title("Trajectory Divergence & Lyapunov Exponents", fontsize=12)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, "lyapunov_divergence.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Chaos analysis complete! Saved to '{save_path}'.")


if __name__ == "__main__":
    run_chaos_quantification()
