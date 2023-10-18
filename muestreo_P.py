#muestreo proporcional
import random

def proportional_resampling(particles, weights):
    num_particles = len(particles)
    indices = range(num_particles)
    new_particles = []
    cumulative_weights = [sum(weights[:i + 1]) for i in range(num_particles)]
    for _ in range(num_particles):
        rand_num = random.uniform(0, 1)
        selected_particle_index = next(i for i, weight_sum in enumerate(cumulative_weights) if weight_sum >= rand_num)
        new_particles.append(particles[selected_particle_index])
    return new_particles
