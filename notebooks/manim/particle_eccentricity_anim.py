from manim import *

class AlphaToOneAnimation(Scene):
    def construct(self):
        # Value tracker for gamma (start at 1, a perfect circle)
        gamma = ValueTracker(1.0)

        # Ellipse shape — linked to gamma
        ellipse = always_redraw(
            lambda: Ellipse(
                width=2 * gamma.get_value(),
                height=2 / gamma.get_value(),
                color=BLUE
            )
        )

        # Alpha formula display — linked to gamma
        alpha_label = always_redraw(
            lambda: MathTex(
                r"\alpha = \frac{\gamma^2 - 1}{\gamma^2 + 1}",
                r"\quad = \quad",
                f"{(gamma.get_value()**2 - 1) / (gamma.get_value()**2 + 1):.4f}"
            ).to_edge(DOWN)
        )

        self.play(FadeIn(ellipse), Write(alpha_label))

        # Animate gamma from 1 (circle) to 1000 (approaching alpha = 1)
        self.play(
            gamma.animate.set_value(1000),
            run_time=8,
            rate_func=smooth
        )

        self.wait(1)
