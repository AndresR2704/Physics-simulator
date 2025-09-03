import numpy as np

def apply_physics(particles, velocities, gravity, width, height, dt, damping):
    new_particles = particles.copy()
    new_velocities = velocities.copy()
    
    # Apply gravity to y velocity
    new_velocities[:, 1] += gravity
    
    return new_particles, new_velocities

def apply_boundary_collisions(particles, velocities, width, height, damping):
    new_particles = particles.copy()
    new_velocities = velocities.copy()
    
    for i in range(len(new_particles)):
        # Floor collision (bottom of screen)
        if new_particles[i, 1] > height - 10:
            new_particles[i, 1] = height - 10
            new_velocities[i, 1] *= -damping
        
        # Roof collision (top of screen)
        if new_particles[i, 1] < 10:
            new_particles[i, 1] = 10
            new_velocities[i, 1] *= -damping
        
        # Left wall collision
        if new_particles[i, 0] < 10:
            new_particles[i, 0] = 10
            new_velocities[i, 0] *= -damping
        
        # Right wall collision
        elif new_particles[i, 0] > width - 10:
            new_particles[i, 0] = width - 10
            new_velocities[i, 0] *= -damping
    
    return new_particles, new_velocities

def apply_particle_collisions_elastic(particles, velocities, radius=15, restitution=0.9):
    
    new_particles = particles.copy()
    new_velocities = velocities.copy()
    
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            # Calculate distance between particles
            dx = particles[j, 0] - particles[i, 0]
            dy = particles[j, 1] - particles[i, 1]
            distance_sq = dx**2 + dy**2
            min_distance = radius  # Collision when centers are a radius apart
            
            # Check if particles are colliding
            if distance_sq < min_distance**2 and distance_sq > 0:
                distance = np.sqrt(distance_sq)
                
                # Normalize collision direction
                nx = dx / distance
                ny = dy / distance
                
                # Calculate relative velocity
                dvx = velocities[j, 0] - velocities[i, 0]
                dvy = velocities[j, 1] - velocities[i, 1]
                
                # Calculate relative velocity in the normal direction
                velocity_along_normal = dvx * nx + dvy * ny
                
                # Do not resolve if velocities are separating
                if velocity_along_normal > 0:
                    continue
                
                # Calculate impulse scalar
                impulse_scalar = -(1.0 + restitution) * velocity_along_normal
                impulse_scalar /= 2.0  # Equal mass particles
                
                # Apply impulse
                impulse_x = impulse_scalar * nx
                impulse_y = impulse_scalar * ny
                
                new_velocities[i, 0] -= impulse_x
                new_velocities[i, 1] -= impulse_y
                new_velocities[j, 0] += impulse_x
                new_velocities[j, 1] += impulse_y
                
                # Separate particles to prevent sticking
                overlap = min_distance - distance
                if overlap > 0:
                    separation = overlap * 0.5
                    new_particles[i] -= separation * np.array([nx, ny])
                    new_particles[j] += separation * np.array([nx, ny])
    

    return new_particles, new_velocities
