#Muestreo por importancia residual
import random

def residual_resampling(particles, weights):
    num_particles = len(particles)
    indices = range(num_particles)
    new_particles = []
    num_copies = [int(weight * num_particles) for weight in weights]
    for i, num_copy in enumerate(num_copies):
        new_particles.extend([particles[i]] * num_copy)
    while len(new_particles) < num_particles:
        i = random.choice(indices)
        new_particles.append(particles[i])
    return new_particles
