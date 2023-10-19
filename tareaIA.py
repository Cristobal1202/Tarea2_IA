import random
import matplotlib.pyplot as plt

# Función para simular el movimiento del submarino
def move_submarine(particles):
    new_particles = []
    for particle in particles:
        # Simular el movimiento del submarino en cada dimensión
        particle[0] += random.gauss(0, 0.1)  # Movimiento en x
        particle[1] += random.gauss(0, 0.1)  # Movimiento en y
        particle[2] += random.gauss(0, 0.1)  # Movimiento en z
        particle[3] += random.gauss(0, 0.01)  # Cambio de aceleración
        particle[4] += random.gauss(0, 0.1)  # Cambio de velocidad
        new_particles.append(particle)
    return new_particles

# Función para calcular los pesos de las partículas (simulación simple)
def calculate_weights(particles, measurements):
    weights = []
    for particle in particles:
        weight = 1.0
        for i in range(5):
            weight *= 1.0 / (1.0 + abs(particle[i] - measurements[i]))
        weights.append(weight)
    return weights

# Resampling proporcional
def proportional_resampling(particles, weights):
    num_particles = len(particles)
    new_particles = []
    cumulative_weights = [sum(weights[:i + 1]) for i in range(num_particles)]
    for _ in range(num_particles):
        rand_num = random.uniform(0, 1)
        selected_particle_index = next(i for i, weight_sum in enumerate(cumulative_weights) if weight_sum >= rand_num)
        new_particles.append(particles[selected_particle_index])
    return new_particles

# Resampling estratificado
def stratified_resampling(particles, weights):
    num_particles = len(particles)
    new_particles = []
    step = 1.0 / num_particles
    offset = random.uniform(0, step)
    cumulative_weights = [sum(weights[:i + 1]) for i in range(num_particles)]
    for i in range(num_particles):
        rand_num = (i * step) + offset
        selected_particle_index = next(j for j, weight_sum in enumerate(cumulative_weights) if weight_sum >= rand_num)
        new_particles.append(particles[selected_particle_index])
    return new_particles

# Número de partículas
N_values = [50, 100, 200]  # Cambio en la cantidad de partículas

# Inicialización de partículas (simulación simple)
initial_particles = [[0.0, 0.0, 0.0, 0.0, 0.0] for _ in range(max(N_values))]

# Mediciones simuladas (simulación simple)
measurements = [1.0, 1.0, 1.0, 0.0, 0.0]

# Listas para almacenar los resultados
results_proportional = []
results_stratified = []

# Iteraciones del filtro de partículas
for N in N_values:
    # Inicialización de N partículas
    particles = initial_particles[:N]

    # Movimiento del submarino
    particles = move_submarine(particles)

    # Cálculo de pesos
    weights = calculate_weights(particles, measurements)

    # Resampling proporcional
    particles_proportional = proportional_resampling(particles, weights)

    # Resampling estratificado
    particles_stratified = stratified_resampling(particles, weights)

    # Almacenar las partículas después del resampling
    results_proportional.append(particles_proportional)
    results_stratified.append(particles_stratified)

# Graficar la dispersión de partículas en cada dimensión
for i, N in enumerate(N_values):
    plt.figure(figsize=(12, 6))
    plt.suptitle(f'Resampling con N = {N}', fontsize=16)

    for j, dimension in enumerate(["X", "Y", "Z", "Aceleración", "Velocidad"]):
        plt.subplot(2, 3, j+1)
        plt.title(f"{dimension} Dimensión")
        
        particles_proportional = [particle[j] for particle in results_proportional[i]]
        particles_stratified = [particle[j] for particle in results_stratified[i]]
        
        plt.scatter(range(N), particles_proportional, c='b', label='Proporcional', s=15)
        plt.scatter(range(N), particles_stratified, c='r', label='Estratificado', s=15)
        
        plt.xlabel("Partícula")
        plt.ylabel(f"{dimension}")
        plt.legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()
