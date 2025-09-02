import numpy as np

# Simulation Parameters
def get_simulation_parameters():
    params = {
        'num_particles': 50,
        'width': 1535,
        'height': 800,
        'dt': 0.1,
        'gravity': 2.0,
        'particle_radius': 20,
        'min_radius': 2,
        'max_radius': 25,
        'collision_scale': 2,
        'damping': 1.0,
        'min_damping': 0.1,
        'max_damping': 1.0,
        'restitution': 1.0,
        'min_restitution': 0.1,
        'max_restitution': 1.0
    }
    return params

# Initialize Particles
def initialize_particles(num_particles, width, height):
    particles = np.random.rand(num_particles, 2) * np.array([width, height // 2])
    velocities = np.zeros((num_particles, 2))
    return particles, velocities