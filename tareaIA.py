import random
import matplotlib.pyplot as plt

# Función para aplicar muestreo proporcional
def proportional_resampling(particles, weights):
    num_particles = len(particles)
    new_particles = []
    cumulative_weights = [sum(weights[:i + 1]) for i in range(num_particles)]
    for _ in range(num_particles):
        rand_num = random.uniform(0, 1)
        selected_particle_index = next(i for i, weight_sum in enumerate(cumulative_weights) if weight_sum >= rand_num)
        new_particles.append(particles[selected_particle_index])
    return new_particles

# Función para aplicar muestreo estratificado
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

# Generación de datos ficticios
num_data_points = 100
true_position = [0.0, 0.0, 0.0, 1.0, 2.0]  # Posición inicial (x, y, z) y velocidad (vx, vy)
measurement_noise = 0.1  # Ruido en las medidas
data = []

for _ in range(num_data_points):
    true_position[0] += true_position[3]  # Actualizar posición en x
    true_position[1] += true_position[4]  # Actualizar posición en y
    true_position[2] += 0.0  # Mantener z constante
    noisy_measurement = [true_pos + random.uniform(-measurement_noise, measurement_noise) for true_pos in true_position]
    data.append(noisy_measurement)

# Guardar datos en un archivo de texto
with open("data.txt", "w") as data_file:
    for measurement in data:
        data_file.write("\t".join(map(str, measurement)) + "\n")

# Leer datos desde el archivo
data = []
with open("data.txt", "r") as data_file:
    for line in data_file:
        data.append(list(map(float, line.strip().split("\t"))))

# Valores de N (número de partículas) para las pruebas
num_particles_values = [50, 100, 200]

for i, num_particles in enumerate(num_particles_values):
    # Inicialización de partículas
    particles = [[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)] for _ in range(num_particles)]

    # Simulación del filtro de partículas
    estimated_positions_proporcional = []
    estimated_positions_estratificado = []

    for measurement in data:
        # Actualizar partículas con ruido
        particles = [[p[i] + random.uniform(-0.1, 0.1) for i in range(5)] for p in particles]

        # Calcular las diferencias entre las medidas y las partículas
        weights = [sum([(m - p[i]) ** 2 for i, m in enumerate(measurement)]) for p in particles]

        # Aplicar muestreo proporcional
        particles_proporcional = proportional_resampling(particles, weights)

        # Aplicar muestreo estratificado
        particles_estratificado = stratified_resampling(particles, weights)

        # Calcular la estimación promedio de la posición
        estimated_position_proporcional = [sum(p[i] for p in particles_proporcional) / num_particles for i in range(5)]
        estimated_position_estratificado = [sum(p[i] for p in particles_estratificado) / num_particles for i in range(5)]

        estimated_positions_proporcional.append(estimated_position_proporcional)
        estimated_positions_estratificado.append(estimated_position_estratificado)

    # Visualización de los resultados
    estimated_positions_proporcional = list(zip(*estimated_positions_proporcional))
    estimated_positions_estratificado = list(zip(*estimated_positions_estratificado))

    plt.figure(figsize=(12, 6))
    plt.plot(estimated_positions_proporcional[0], label=f'Proporcional (N={num_particles})', linestyle='-.', color='b')
    plt.plot(estimated_positions_estratificado[0], label=f'Estratificado (N={num_particles})', linestyle=':', color='r')
    plt.legend()
    plt.title(f'Estimación de Posición X (N={num_particles})')
    plt.show()
