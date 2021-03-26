import numpy as np
import pickle


cities = np.genfromtxt("cities.csv", delimiter=",")

def calculate_and_safe_distances():
    distances = []
    for i in range(len(cities)):
        tmp_array = []
        for j in range(len(cities)):
            tmp = ((cities[i][1] - cities[j][1]) ** 2 + (
                    cities[i][2] - cities[j][2]) ** 2) ** 0.5
            tmp_array.append(tmp)
        distances.append(tmp_array)
        print(len(distances))
    with open("data.pickle", "wb") as fil:
        pickle.dump(distances, fil)

    return distances


calculate_and_safe_distances()
