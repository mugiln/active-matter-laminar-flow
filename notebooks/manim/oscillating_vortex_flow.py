from manim import *
import numpy as np


class ImprovedVortexFlowAnimation(Scene):
    def construct(self):
        # Parameters
        U = 1.0  # Flow velocity magnitude
        L = 2*PI  # Spatial scaling factor (L = 2π)
        num_particles = 400  # More particles for better coverage
        particle_speed_factor = 0.02  # Control particle movement speed
        animation_time = 0.05  # Shorter time for smoother animation
        trace_length = 15  # How many positions to store for each particle's trail
        
        # Create coordinate axes
        axes = Axes(
            x_range=[-PI, PI, PI/2],
            y_range=[-PI, PI, PI/2],
            axis_config={"color": BLUE},
        )
        
        # No axes labels or title
        
        # Function to compute velocity at a point
        def compute_velocity(x, y):
            # Apply spatial scaling (L = 2π)
            x_scaled = x
            y_scaled = y
            
            vx = U * np.sin(x_scaled) * np.cos(y_scaled)
            vy = -U * np.cos(x_scaled) * np.sin(y_scaled)
            
            return vx, vy, np.sqrt(vx**2 + vy**2)
        
        # Initialize flow particles with arrows
        flow_arrows = []
        arrow_positions = []
        arrow_trails = []
        arrow_colors = []
        
        # Create a uniform grid of particles
        grid_size = int(np.sqrt(num_particles))
        for i in range(grid_size):
            for j in range(grid_size):
                # Uniform distribution across domain
                x = -PI + 2*PI * i / (grid_size - 1)
                y = -PI + 2*PI * j / (grid_size - 1)
                
                # Skip particles too close to vortex centers
                if ((abs(x - PI/2) < 0.2 and abs(y - PI/2) < 0.2) or
                    (abs(x + PI/2) < 0.2 and abs(y - PI/2) < 0.2) or
                    (abs(x - PI/2) < 0.2 and abs(y + PI/2) < 0.2) or
                    (abs(x + PI/2) < 0.2 and abs(y + PI/2) < 0.2)):
                    continue
                
                # Get velocity at this point
                vx, vy, magnitude = compute_velocity(x, y)
                
                # Scale arrow length based on velocity magnitude
                arrow_scale = 0.2 + 0.3 * magnitude
                
                # Determine color based on which quadrant (to show vortex direction)
                if (x > 0 and y > 0) or (x < 0 and y < 0):  # Quadrants 1 and 3 (CW)
                    color = BLUE_B
                else:  # Quadrants 2 and 4 (CCW)
                    color = RED_B
                
                # Create arrow pointing in flow direction
                start_point = axes.c2p(x, y)
                end_point = axes.c2p(x + vx * arrow_scale, y + vy * arrow_scale)
                
                # Create arrow with consistent length based on velocity
                arrow = Arrow(
                    start_point, 
                    end_point,
                    buff=0, 
                    max_tip_length_to_length_ratio=0.2,
                    stroke_width=2,
                    color=color
                )
                
                flow_arrows.append(arrow)
                arrow_positions.append([x, y])
                arrow_trails.append([[x, y]])  # Start with current position
                arrow_colors.append(color)
        
        # Create group for arrows
        arrow_group = VGroup(*flow_arrows)
        
        # Create trail objects for each arrow
        trails = []
        for i, history in enumerate(arrow_trails):
            trail = VMobject()
            trail.set_points_as_corners([axes.c2p(*pos) for pos in history])
            trail.set_stroke(arrow_colors[i], opacity=0.6, width=2)
            trails.append(trail)
        
        # Group all trails
        trail_group = VGroup(*trails)
        
        # Add axes to scene
        self.play(
            Create(axes)
        )
        
        # Create dots at vortex centers
        vortex_centers = [
            [PI/2, PI/2],
            [-PI/2, PI/2],
            [PI/2, -PI/2],
            [-PI/2, -PI/2]
        ]
        
        vortex_dots = VGroup(*[
            Dot(axes.c2p(*center), color=WHITE, radius=0.08)
            for center in vortex_centers
        ])
        
        # Add arrows, vortex dots, and trails to scene
        self.play(Create(arrow_group))
        self.play(Create(vortex_dots))
        self.add(trail_group)  # Add trails but don't animate creation
        
        # Wait a moment before animation
        self.wait(1)
        
        # Animation parameters
        num_frames = 300  # More frames for smoother animation
        
        # Animate particles and their trails
        for i in range(num_frames):
            arrow_moves = []
            new_trails = []
            
            for j, (arrow, position, history, color) in enumerate(zip(flow_arrows, arrow_positions, arrow_trails, arrow_colors)):
                x, y = position
                
                # Get velocity at current position
                vx, vy, magnitude = compute_velocity(x, y)
                
                # Update position based on velocity field
                new_x = x + vx * particle_speed_factor
                new_y = y + vy * particle_speed_factor
                
                # Check if particle is out of bounds, if so reset to opposite side
                if abs(new_x) > PI or abs(new_y) > PI:
                    # Reset to a new position along the edge
                    angle = np.random.uniform(0, 2 * PI)
                    r = PI * 0.95  # Slightly inside the visible area
                    new_x = r * np.cos(angle)
                    new_y = r * np.sin(angle)
                    
                    # Update color based on new quadrant
                    if (new_x > 0 and new_y > 0) or (new_x < 0 and new_y < 0):
                        arrow_colors[j] = BLUE_B
                    else:
                        arrow_colors[j] = RED_B
                    
                    # Reset history for this particle
                    arrow_trails[j] = [[new_x, new_y]]
                else:
                    # Add new position to history
                    history.append([new_x, new_y])
                    
                    # Limit history length
                    if len(history) > trace_length:
                        history = history[-trace_length:]
                        arrow_trails[j] = history
                
                # Save new position
                arrow_positions[j] = [new_x, new_y]
                
                # Get velocity at new position for arrow orientation
                new_vx, new_vy, new_magnitude = compute_velocity(new_x, new_y)
                
                # Scale arrow length based on new velocity magnitude
                arrow_scale = 0.2 + 0.3 * new_magnitude
                
                # Create new arrow pointing in flow direction
                start_point = axes.c2p(new_x, new_y)
                end_point = axes.c2p(new_x + new_vx * arrow_scale, new_y + new_vy * arrow_scale)
                
                # Create animation to move and rotate arrow
                new_arrow = Arrow(
                    start_point, 
                    end_point,
                    buff=0, 
                    max_tip_length_to_length_ratio=0.2,
                    stroke_width=2,
                    color=arrow_colors[j]
                )
                
                arrow_moves.append(Transform(arrow, new_arrow))
                
                # Update trail
                new_trail = VMobject()
                new_trail.set_points_as_corners([axes.c2p(*pos) for pos in history])
                new_trail.set_stroke(arrow_colors[j], opacity=0.6, width=2)
                new_trails.append(new_trail)
            
            # Update trails
            self.remove(trail_group)
            trail_group = VGroup(*new_trails)
            self.add(trail_group)
            trails = new_trails
            
            # Play all arrow animations at once
            self.play(
                *arrow_moves,
                run_time=animation_time,
                rate_func=linear
            )
        
        self.wait(2)


class StreamlineFlowVisualization(Scene):
    """An alternative visualization that shows streamlines of the flow."""
    def construct(self):
        # Initialize time variable
        self.current_time = 0
        
        # Parameters
        U = 1.0  # Flow velocity magnitude
        L = 2*PI  # Spatial scaling factor (L = 2π)
        streamline_count = 16  # Number of streamlines to draw
        animation_time = 5.0  # Total animation duration
        
        # Create coordinate axes
        axes = Axes(
            x_range=[-PI, PI, PI/2],
            y_range=[-PI, PI, PI/2],
            axis_config={"color": BLUE},
        )
        
        # No axes labels or title
        
        # Function to compute velocity at a point
        def compute_velocity(x, y):
            # Apply spatial scaling (L = 2π)
            x_scaled = x
            y_scaled = y
            
            vx = U * np.sin(x_scaled) * np.cos(y_scaled)
            vy = -U * np.cos(x_scaled) * np.sin(y_scaled)
            
            return vx, vy, np.sqrt(vx**2 + vy**2)
        
        # Add axes to scene
        self.play(
            Create(axes)
        )
        
        # Create vortex center markers
        vortex_centers = [
            [PI/2, PI/2],
            [-PI/2, PI/2],
            [PI/2, -PI/2],
            [-PI/2, -PI/2]
        ]
        
        vortex_dots = VGroup(*[
            Dot(axes.c2p(*center), color=YELLOW, radius=0.05)
            for center in vortex_centers
        ])
        
        self.play(
            Create(vortex_dots)
        )
        
        # Create streamlines
        streamlines = []
        
        # Starting positions for streamlines
        for i in range(streamline_count):
            # Start points along the axes and domain boundaries
            if i < streamline_count/4:
                # Top edge
                x = -PI + 2*PI * i / (streamline_count/4 - 1)
                y = PI * 0.9
            elif i < streamline_count/2:
                # Right edge
                x = PI * 0.9
                y = PI - 2*PI * (i - streamline_count/4) / (streamline_count/4 - 1)
            elif i < 3*streamline_count/4:
                # Bottom edge
                x = PI - 2*PI * (i - streamline_count/2) / (streamline_count/4 - 1)
                y = -PI * 0.9
            else:
                # Left edge
                x = -PI * 0.9
                y = -PI + 2*PI * (i - 3*streamline_count/4) / (streamline_count/4 - 1)
            
            # Determine color based on which quadrant the streamline starts in
            if (x > 0 and y > 0) or (x < 0 and y < 0):
                color = BLUE_B
            else:
                color = RED_B
            
            # Create streamline path with closure to capture initial position
            initial_pos = (x, y)
            streamline = TracedPath(
                lambda: axes.c2p(*self.get_particle_position(initial_pos[0], initial_pos[1], self.current_time)),
                stroke_color=color,
                stroke_width=2,
                stroke_opacity=0.8
            )
            
            streamlines.append(streamline)
        
        # Add all streamlines to scene
        for streamline in streamlines:
            self.add(streamline)
        
        # Animate time using a ValueTracker
        time_tracker = ValueTracker(0)
        
        # Update function to set current_time from the tracker
        def update_time(m):
            self.current_time = time_tracker.get_value()
        
        # Add a dummy mobject for the updater
        dummy = VMobject()
        dummy.add_updater(update_time)
        self.add(dummy)
        
        # Animate the time tracker
        self.play(
            time_tracker.animate.set_value(animation_time),
            rate_func=linear,
            run_time=animation_time
        )
        
        self.wait(2)
    
    def get_particle_position(self, x_start, y_start, t):
        """
        Compute particle position at time t, starting from (x_start, y_start)
        using 4th order Runge-Kutta integration
        """
        dt = 0.01  # Small time step for integration
        steps = int(t / dt)
        x, y = x_start, y_start
        
        # Implement RK4 integration for the flow
        for _ in range(min(steps, 1000)):  # Limit max steps
            # Get velocity at current position
            vx, vy, _ = self.compute_velocity(x, y)
            
            if abs(vx) < 1e-10 and abs(vy) < 1e-10:
                break  # Stop if velocity is near zero
                
            # RK4 integration
            k1_x, k1_y, _ = self.compute_velocity(x, y)
            k2_x, k2_y, _ = self.compute_velocity(x + 0.5*dt*k1_x, y + 0.5*dt*k1_y)
            k3_x, k3_y, _ = self.compute_velocity(x + 0.5*dt*k2_x, y + 0.5*dt*k2_y)
            k4_x, k4_y, _ = self.compute_velocity(x + dt*k3_x, y + dt*k3_y)
            
            x += (dt/6) * (k1_x + 2*k2_x + 2*k3_x + k4_x)
            y += (dt/6) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
            
            # Check if out of bounds or too close to a vortex center
            if abs(x) > PI or abs(y) > PI:
                break
            
            # Check if too close to vortex centers
            if ((abs(x - PI/2) < 0.1 and abs(y - PI/2) < 0.1) or
                (abs(x + PI/2) < 0.1 and abs(y - PI/2) < 0.1) or
                (abs(x - PI/2) < 0.1 and abs(y + PI/2) < 0.1) or
                (abs(x + PI/2) < 0.1 and abs(y + PI/2) < 0.1)):
                break
        
        return x, y
    
    def compute_velocity(self, x, y):
        """Compute velocity at point (x, y)"""
        U = 1.0
        
        vx = U * np.sin(x) * np.cos(y)
        vy = -U * np.cos(x) * np.sin(y)
        magnitude = np.sqrt(vx**2 + vy**2)
        
        return vx, vy, magnitude
    
    # Removed the time_increase_animation method as we're using ValueTracker instead