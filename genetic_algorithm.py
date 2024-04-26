import math
import random
import time
import pygame
import collections


class GeneticAlgorithm:
    def __init__(self):
        # self.visuals = True
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

    def start(self):
        self.stamp = time.time()
        # if self.visuals:
        # pygame.init()
        # pygame.font.init()
        # self.font = pygame.font.SysFont('Arial', 30)
        # self.screen = pygame.display.set_mode((800, 850))
        # size = (400, 800)
        # self.surface = pygame.Surface(size)

        # waint until user quits
        # running = True
        # while running:
        # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        # running = False
        #
        # pygame.quit()

        # else:
        while True:
            self.gen_count += 1
            self.calculate_fitness()
            self.generate_new_population()

    def calculate_distance(self, path: []) -> float:
        total = 0
        for i in range(len(path) - 1):  # runs on all the items except the last one
            x = pow((path[i + 1][0] - path[i][0]), 2)
            y = pow((path[i + 1][1] - path[i][1]), 2)
            total += math.sqrt(x + y)

        # calculate the last item
        x = pow((path[-1][0] - path[-1][0]), 2)
        y = pow((path[-1][0] - path[-1][0]), 2)
        total += math.sqrt(x + y)
        return total

    def calculate_fitness(self) -> None:
        total_fitness = 0
        # calculate length of path for each route
        # Invert length to give shorter routes a higher fitness
        for i in range(len(self.fitness)):
            self.fitness[i] = self.calculate_distance(self.population[i])
            if self.fitness[i] < self.current_best["length"]:
                print("New best path found: {0} after {1} generations and {2:5.2f} seconds."
                      .format(self.fitness[i], self.gen_count, time.time() - self.stamp))
                self.current_best["path"] = self.population[i]
                self.current_best["length"] = self.fitness[i]
            self.fitness[i] = 1 / self.fitness[i]
            total_fitness += self.fitness[i]

    def generate_new_population(self) -> None:
        new_population = [None] * len(self.population)
        for i in range(len(self.population)):
            parent_a = None
            parent_b = None
            iter_limit = 0
            while parent_a == parent_b:
                iter_limit += 1
                parent_a = self.accept_reject()
                parent_b = self.accept_reject()
                if iter_limit > 5000:
                    break
            new_population[i] = self.crossover(parent_a, parent_b)  # generate new child
            new_population[i] = self.mutate(new_population[i])  # mutate the child

        self.population = new_population

    def accept_reject(self) -> []:
        max_fitness = max(self.fitness)
        # Choose a random element from the population
        index = random.randint(0, len(self.population) - 1)

        # Generate a random number between 0 and max_fitness
        # if the fitness of the current element is lower than the random number,
        # Choose another element and try again. otherwise return the current element
        # population memnbers with higher fittness values have a better chance of being selected
        # not eliminating the chance of the lower fittness members to be selected
        while self.fitness[index] < random.uniform(0, max_fitness):
            index = random.randint(0, len(self.population) - 1)
        return self.population[index]

    def crossover(self, parent_a: [], parent_b: []) -> []:
        # add an order set of points from parentA
        # then fill the remaining spots with points from parentB in the order they appear
        # ignoring any elements already inserted from the first parent
        # correct number of unique cities - according to both of the parents
        rand = random.randint(0, len(parent_a) - 1)
        child = parent_a[:rand]
        #  Counter is a built-in class that allows you to count the occurrences of elements in an iterable object
        # creates a dictionary that maps each element in the iterable to its count or frequency in the collection.

        # only elements with positive count are returned
        # intersection min(c1[x], c2[x])
        intersect = collections.Counter(child) & collections.Counter(parent_b)

        # keeps only +ve count elements
        # keeps the cities that aren't in child's list
        parent_b = list((collections.Counter(parent_b) - intersect).elements())
        child += parent_b[:]
        return child

    def mutate(self, child: []) -> []:
        # Generate a random number. if it is lower than the mutation rate,
        # swap the current element with a random element from the population
        for i in range(len(child)):
            if random.random() < self.mutation_rate:
                index = random.randint(0, len(self.cities) - 1)
                # swap between the cities
                child[i], child[index] = child[index], child[i]
        return child


GeneticAlgorithm().start()
