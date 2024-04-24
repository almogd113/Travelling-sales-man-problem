import random


class GeneticAlgorithm:
    def __init__(self):
        self.visuals = True
        self.mutation_rate = 0.01
        population_size = 100

        # init cities coordinates
        self.cities = []

        # check if the list is empty
        if not self.cities:
            cities_count = 10
            for i in range(cities_count):
                x = random.randint(0, 399)
                y = random.randint(0, 399)
                self.cities.append((x, y))
        print(self.cities)

        #     fill population with random permutations

        #  initializing an empty list of tuples - all the chromosomes
        self.population = [None] * population_size
        for i in range(len(self.population)):
            random.shuffle(self.cities)  # create a random sequence of the cities
            self.population[i] = self.cities[:]  # refers to all the references that the list has

        self.fitness = [0] * population_size

        self.current_best = {"path": self.population[0], "length": float('inf')}

        self.gen_count = 0