import random
import pickle


def get_distances():
    with open("data.pickle", 'rb') as file:
        distances = pickle.load(file)
    return distances


distances = get_distances()


def check_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def count_path_length(path):
    dist = 0
    for i in range(len(path) - 1):
        if i % 10 == 0 and not check_prime(path[i]):
            dist += distances[path[i]][path[i + 1]] * 1.1
        else:
            dist += distances[path[i]][path[i + 1]]
    return dist


def generate_path(pheromons):
    path = [0]
    available_nodes = list(range(1, len(distances)))
    step_number = 0
    for i in range(len(distances) - 1):
        if i % 10 == 9:
            total_prob = 0
            tmp_probs = []
            for g in available_nodes:
                if check_prime(g):
                    total_prob += 1 / (distances[path[-1]][g] / 1.1) * pheromons[path[-1]][g]
                    tmp_probs.append(1 / (distances[path[-1]][g] / 1.1) * pheromons[path[-1]][g])
                else:
                    total_prob += 1 / distances[path[-1]][g] * pheromons[path[-1]][g]
                    tmp_probs.append(1 / distances[path[-1]][g] * pheromons[path[-1]][g])

            for h in range(len(tmp_probs)):
                tmp_probs[h] /= total_prob

        else:
            total_prob = 0
            for g in available_nodes:
                total_prob += 1 / distances[path[-1]][g] * pheromons[path[-1]][g]
            tmp_probs = [(1 / distances[path[-1]][g] * pheromons[path[-1]][g]) / total_prob for g in available_nodes]

        chosen_node = choose_node(tmp_probs)
        path.append(available_nodes[chosen_node])
        available_nodes.pop(chosen_node)
    path.append(0)
    return path


def choose_node(probs):
    rand = random.random()
    for i in range(len(probs)):
        rand -= probs[i]
        if rand <= 0:
            return i


pheromones_table = [[1 for j in range(len(distances))] for i in range(len(distances))]
evaporation_rate = 0.65
Q = 3
num_of_ants = 100
path = generate_path(pheromones_table)
lenpath = count_path_length(path)
print(lenpath, path)
while True:
    nodes_counts = [[0] * len(distances) for i in range(len(distances))]
    for i in range(num_of_ants):
        tpath = generate_path(pheromones_table)
        tlenpath = count_path_length(tpath)
        if tlenpath < lenpath:
            path = tpath
            lenpath = tlenpath
            print(lenpath, path)
        for j in range(len(tpath) - 1):
            nodes_counts[path[j]][path[j + 1]] += Q / tlenpath

    for i in range(len(pheromones_table)):
        for j in range(len(pheromones_table)):
            pheromones_table[i][j] = pheromones_table[i][j] * evaporation_rate + nodes_counts[i][j] + nodes_counts[j][i]
