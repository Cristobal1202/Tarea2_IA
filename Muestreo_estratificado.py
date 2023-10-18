#Muestreo estratificado
import random

def stratified_resampling(particles, weights):
    num_particles = len(particles)
    indices = range(num_particles)
    new_particles = []
    step = 1.0 / num_particles
    offset = random.uniform(0, step)
    cumulative_weights = [sum(weights[:i + 1]) for i in range(num_particles)]
    for i in range(num_particles):
        rand_num = (i * step) + offset
        selected_particle_index = next(j for j, weight_sum in enumerate(cumulative_weights) if weight_sum >= rand_num)
        new_particles.append(particles[selected_particle_index])
    return new_particles
