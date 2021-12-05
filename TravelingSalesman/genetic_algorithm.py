import random
from typing import Callable

import numpy as np


def generate_locations(number_of_nodes: int, environment_size=10) -> list[complex]:
    return [complex(random.randint(0, environment_size), random.randint(0, environment_size))
            for _ in range(number_of_nodes)]


def construct_euclidean_distance_table(node_locations: list[complex]) -> np.ndarray:
    m, n = np.meshgrid(node_locations, node_locations)
    return abs(m-n)


def generate_random_routes(number_of_routes: int, number_of_nodes: int) -> list[np.ndarray]:
    return [np.take(np.arange(1, number_of_nodes), np.random.rand(number_of_nodes - 1).argsort(), axis=0)
            for _ in range(number_of_routes)]


def breed_generation_ranked(routes: list[np.ndarray], luck_factor: float, survival_rate: float, mutation_rate: float,
                            cost_table: np.ndarray) -> list[np.ndarray]:
    number_of_routes = len(routes)
    rank_routes(routes, luck_factor, cost_table)
    del routes[int(number_of_routes * survival_rate):]

    new_routes = []
    for _ in range(0, number_of_routes):
        new_route = ordered_crossover(routes[random.randint(0, len(routes) - 1)], routes[random.randint(0, len(routes) - 1)])
        swap_mutation(new_route, mutation_rate)
        new_routes.append(new_route)

    return new_routes


def breed_generation_elitest(routes: list[np.ndarray], luck_factor: float, survival_rate: float, mutation_rate: float,
                             crossover: Callable, cost_table: np.ndarray) -> list[np.ndarray]:
    number_of_routes = len(routes)
    number_of_elites = int(number_of_routes * survival_rate)

    rank_routes(routes, luck_factor, cost_table)
    del routes[number_of_elites:]

    for _ in range(number_of_elites, number_of_routes):
        new_route = crossover(routes[random.randint(0, number_of_elites - 1)], routes[random.randint(0, number_of_elites - 1)])
        swap_mutation(new_route, mutation_rate)
        routes.append(new_route)

    return routes


def rank_routes(routes: list[np.ndarray], luck_factor: float, cost_table: np.ndarray) -> None:
    routes.sort(key=lambda route: calculate_route_cost(route, cost_table) * (1 + random.random() * luck_factor))


def calculate_route_cost(route: np.ndarray, cost_table: np.ndarray) -> int:
    home_cost = cost_table[0][route[0]] + cost_table[route[len(route) - 1]][0]
    route_cost = sum(cost_table[route[i]][route[i + 1]] for i in range(0, len(route) - 1))
    return home_cost + route_cost


def ordered_crossover(first_route: np.ndarray, second_route: np.ndarray) -> np.ndarray:
    subset_start = random.randint(0, len(first_route) - 1)
    subset_end = random.randint(subset_start + 1, len(first_route))

    subset = first_route[subset_start:subset_end]

    child = np.array(list(filter(lambda node: node not in subset, second_route)), dtype=int)
    crossover_location = random.randint(0, len(child))
    child = np.concatenate((child[:crossover_location], subset, child[crossover_location:]), dtype=int)

    return child


def generate_smart_crossover(cluster_size: int, cost_table: np.ndarray) -> Callable:

    def smart_crossover(first_route: np.ndarray, second_route: np.ndarray) -> np.ndarray:

        subset = min([first_route[i:i+cluster_size] for i in range(len(first_route) - cluster_size)],
                     key=lambda cluster: calculate_route_cost(cluster, cost_table))

        child = np.array(list(filter(lambda node: node not in subset, second_route)), dtype=int)
        crossover_location = random.randint(0, len(child))
        child = np.concatenate((child[:crossover_location], subset, child[crossover_location:]), dtype=int)

        return child

    return smart_crossover


def swap_mutation(route: np.ndarray, mutation_rate: float):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]


def main():
    number_of_cities = 100
    number_of_generations = 100

    population_size = 300
    luck_factor = 0.4
    survival_rate = 0.05
    mutation_rate = 0.2

    print_exact_solution = False
    print_distances = False
    debug_count = 1

    locations = generate_locations(number_of_cities)
    cost_table = construct_euclidean_distance_table(locations)

    if print_exact_solution:
        from python_tsp.exact import solve_tsp_dynamic_programming

        permutation, distance = solve_tsp_dynamic_programming(cost_table)
        print("exact solution:", permutation, "  cost:", distance)

    routes = generate_random_routes(population_size, number_of_cities)
    print("locations", locations)
    if print_distances:
        print("distances:\n", cost_table)
        print("routes:\n", routes)

    rank_routes(routes, 0, cost_table)
    print("initial smallest cost:", calculate_route_cost(routes[0], cost_table))

    for i in range(number_of_generations):
        routes = breed_generation_elitest(routes, luck_factor, survival_rate, mutation_rate, ordered_crossover, cost_table)
        if i % debug_count == 0:
            rank_routes(routes, 0, cost_table)
            print("generation:", i, " smallest cost:", calculate_route_cost(routes[0], cost_table))

    rank_routes(routes, 0, cost_table)
    print("final smallest cost:", calculate_route_cost(routes[0], cost_table))
    print(routes[0])


if __name__ == "__main__":
    np.set_printoptions(precision=3)
    main()
