import pygame
from config import get_simulation_parameters, initialize_particles
from physics_engine import apply_physics, apply_boundary_collisions, apply_particle_collisions_elastic
from visualizer import Slider, draw_particles, draw_ui, BACKGROUND

def main():
    # Initialize Pygame
    pygame.init()
    
    # Get configuration
    params = get_simulation_parameters()
    width, height = params['width'], params['height']
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fluid Simulator with Interactive Controls")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    
    # Initialize particles
    particles, velocities = initialize_particles(params['num_particles'], width, height)
    
    # Create UI elements
    gravity_slider = Slider(
        x=50, 
        y=height - 50, 
        width=120, 
        height=20, 
        initial_value=params['gravity'],
        min_val=0.0,
        max_val=2.0,
        label="Gravity"
    )
    
    radius_slider = Slider(
        x=190,
        y=height - 50,
        width=120,
        height=20,
        initial_value=params['particle_radius'],
        min_val=params['min_radius'],
        max_val=params['max_radius'],
        label="Particle Size"
    )
    
    damping_slider = Slider(
        x=330,
        y=height - 50,
        width=120,
        height=20,
        initial_value=params['damping'],
        min_val=params['min_damping'],
        max_val=params['max_damping'],
        label="Damping"
    )
    
    restitution_slider = Slider(
        x=470,
        y=height - 50,
        width=120,
        height=20,
        initial_value=params['restitution'],
        min_val=params['min_restitution'],
        max_val=params['max_restitution'],
        label="Bounciness"
    )
    
    sliders = [gravity_slider, radius_slider, damping_slider, restitution_slider]
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to UI elements
            for slider in sliders:
                slider.handle_event(event)
        
        # Update physics with current values from sliders
        particles, velocities = apply_physics(
            particles, 
            velocities, 
            gravity_slider.value, 
            width, 
            height, 
            params['dt'],
            damping_slider.value
        )
        
        # Apply particle collisions with current parameters
        particles, velocities = apply_particle_collisions_elastic(
            particles, 
            velocities, 
            radius=radius_slider.value * params['collision_scale'],  # Simple scaling
            restitution=restitution_slider.value
        )
        
        # Update positions after collisions
        particles += velocities * params['dt']
        
        # Apply boundary collisions with current damping
        particles, velocities = apply_boundary_collisions(
            particles,
            velocities,
            width,
            height,
            damping_slider.value
        )
        
        # Drawing
        screen.fill(BACKGROUND)
        draw_particles(screen, particles, radius_slider.value)
        draw_ui(screen, font, sliders)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()