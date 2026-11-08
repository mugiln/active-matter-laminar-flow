from manim import *
import numpy as np

class EccentricityVsVelocity(Scene):
    def construct(self):
        # Data (your values here)
        x = np.array([
            0.1, 0.118367, 0.136735, 0.155102, 0.173469, 0.191837, 0.210204,
            0.228571, 0.246939, 0.265306, 0.283673, 0.302041, 0.320408, 0.338776,
            0.357143, 0.375510, 0.393878, 0.412245, 0.430612, 0.448980, 0.467347,
            0.485714, 0.504082, 0.522449, 0.540816, 0.559184, 0.577551, 0.595918,
            0.614286, 0.632653, 0.651020, 0.669388, 0.687755, 0.706122, 0.724490,
            0.742857, 0.761224, 0.779592, 0.797959, 0.816327, 0.834694, 0.853061,
            0.871429, 0.889796, 0.908163, 1.0
        ])

        y = np.array([
            0.249434, 0.226074, 0.214395, 0.214395, 0.214395, 0.202715, 0.214395,
            0.226074, 0.214395, 0.202715, 0.202715, 0.191035, 0.202715, 0.202715,
            0.191035, 0.191035, 0.191035, 0.191035, 0.179355, 0.179355, 0.167676,
            0.179355, 0.167676, 0.167676, 0.155996, 0.155996, 0.144316, 0.144316,
            0.144316, 0.132637, 0.132637, 0.120957, 0.120957, 0.109277, 0.109277,
            0.097598, 0.097598, 0.085918, 0.085918, 0.074238, 0.074238, 0.062559,
            0.062559, 0.062559, 0.062559, 0.050879
        ])

        # Axes
        ax = Axes(
            x_range=[0, 1.1, 0.2],
            y_range=[0, 0.3, 0.05],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [0.2, 0.4, 0.6, 0.8, 1.0]},
            y_axis_config={"numbers_to_include": [0.1, 0.2, 0.3]},
        ).to_edge(DOWN)

        labels = ax.get_axis_labels(
            x_label=MathTex(r"\alpha", color=WHITE),
            y_label=MathTex(r"v_p", color=WHITE)
        )

        self.add(ax, labels)

        # Create points and line
        points = [ax.c2p(x[i], y[i]) for i in range(len(x))]
        graph = VMobject(color="#08F7FE", stroke_width=4)
        graph.set_points_smoothly([points[0]])

        # Animate point-by-point construction
        for i in range(1, len(points)):
            new_segment = VMobject(color="#08F7FE", stroke_width=4)
            new_segment.set_points_as_corners([*points[:i+1]])
            self.play(Transform(graph, new_segment), run_time=0.05)

        self.wait(1)
