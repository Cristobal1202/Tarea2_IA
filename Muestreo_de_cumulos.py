#Muestreo de cúmulos
import random
from sklearn.cluster import KMeans

def cluster_resampling(particles, k):
    num_particles = len(particles)
    data = [particle.feature_vector for particle in particles]
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)
    clusters = kmeans.predict(data)
    cluster_counts = {cluster: clusters.count(cluster) for cluster in set(clusters)}
    new_particles = []
    for cluster, count in cluster_counts.items():
        cluster_indices = [i for i, c in enumerate(clusters) if c == cluster]
        selected_indices = random.sample(cluster_indices, min(count, num_particles))
        new_particles.extend([particles[i] for i in selected_indices])
    return new_particles
