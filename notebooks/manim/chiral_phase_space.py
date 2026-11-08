from manim import *
import numpy as np
import os

class ThreeParticlePhaseAnimation(ThreeDScene):
    def construct(self):
        # === Load particle trajectories from files or generate dynamically ===
        folder_path = os.environ.get("TRAJ_DATA_DIR", "data/chiral_particles")
        p_i = [0, 1, 2]  # particle indices
        no_of_particles = len(p_i)
        timesteps = 500

        x = np.zeros((no_of_particles, timesteps))
        y = np.zeros((no_of_particles, timesteps))
        theta = np.zeros((no_of_particles, timesteps))

        if os.path.exists(folder_path):
            for i1, i in enumerate(range(0, 10000, 20)):
                file_path = os.path.join(folder_path, f"var{i}")
                if os.path.exists(file_path):
                    data = np.loadtxt(file_path)
                    selected = data[p_i, :]
                    x[:, i1] = selected[:, 0]
                    y[:, i1] = selected[:, 1]
                    theta[:, i1] = selected[:, 2]
        else:
            # Fallback: Generate sample trajectories dynamically
            import sys
            sys.path.insert(0, os.path.abspath("../../src"))
            from active_matter import simulate_ensemble
            X0 = np.array([[1.0, 1.0, 0.0], [1.2, 1.1, np.pi/4], [0.8, 1.2, -np.pi/4]])
            traj, _ = simulate_ensemble(X0, dt=0.01, nt=timesteps*10, nsave=10, vp=0.15, alpha=0.99, chirality=0.3)
            for i in range(no_of_particles):
                x[i, :] = traj[:timesteps, i, 0]
                y[i, :] = traj[:timesteps, i, 1]
                theta[i, :] = traj[:timesteps, i, 2]

        # === Set up 3D axes ===
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-np.pi, np.pi, np.pi/2],
            x_length=6,
            y_length=6,
            z_length=4,
        )
        x_label = axes.get_x_axis_label("X")
        y_label = axes.get_y_axis_label("Y")
        z_label = axes.get_z_axis_label(r"\theta")
        self.add(axes, x_label, y_label, z_label)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        colors = [YELLOW, GREEN, RED]
        particles = []
        traces = []

        # Create particles and their traced paths
        for i in range(no_of_particles):
            points = [axes.c2p(x[i, j], y[i, j], theta[i, j]) for j in range(timesteps)]
            path = VMobject(color=colors[i]).set_points_as_corners(points)
            dot = Dot3D(points[0], radius=0.06, color=colors[i])
            trace = TracedPath(dot.get_center, stroke_color=colors[i], stroke_width=3)
            particles.append((dot, path, points))
            traces.append(trace)
            self.add(trace, dot)

        # === Set the camera to follow the first particle (0-th) ===
        def camera_tracker(mob):
            dot = particles[0][0]
            self.camera.frame.move_to(dot.get_center())

        self.camera.frame.add_updater(camera_tracker)

        # Animate all particles along their path
        animations = [
            MoveAlongPath(particles[i][0], particles[i][1], rate_func=linear)
            for i in range(no_of_particles)
        ]

        self.play(*animations, run_time=20)  # Slower motion
        self.camera.frame.remove_updater(camera_tracker)
        self.wait()
