import random
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

np.set_printoptions(precision=3)


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
                             cost_table: np.ndarray) -> list[np.ndarray]:
    number_of_routes = len(routes)
    number_of_elites = int(number_of_routes * survival_rate)

    rank_routes(routes, luck_factor, cost_table)
    del routes[number_of_elites:]

    for _ in range(number_of_elites, number_of_routes):
        new_route = ordered_crossover(routes[random.randint(0, number_of_elites - 1)],
                                      routes[random.randint(0, number_of_elites - 1)])
        swap_mutation(new_route, mutation_rate)
        routes.append(new_route)

    #print(len(routes), number_of_routes)

    return routes


def rank_routes(routes: list[np.ndarray], luck_factor, cost_table: np.ndarray):
    routes.sort(key=lambda route: calculate_route_cost(route, cost_table) * (1 + random.random() * luck_factor))


def calculate_route_cost(route: np.ndarray, cost_table: np.ndarray) -> int:
    home_cost = cost_table[0][route[0]] + cost_table[route[len(route) - 1]][0]
    route_cost = sum(cost_table[route[i]][route[i + 1]] for i in range(0, len(route) - 1))
    return home_cost + route_cost


# ToDo can we crossover more then 2 routes? What other crossover types are there?
def ordered_crossover(first_route: np.ndarray, second_route: np.ndarray) -> np.ndarray:
    subset_start = random.randint(0, len(first_route) - 1)
    subset_end = random.randint(subset_start + 1, len(first_route))

    subset = first_route[subset_start:subset_end]

    child = np.array(list(filter(lambda node: node not in subset, second_route)), dtype=int)
    crossover_location = random.randint(0, len(child))
    child = np.concatenate((child[:crossover_location], subset, child[crossover_location:]), dtype=int)

    return child


def swap_mutation(route: np.ndarray, mutation_rate: float):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]


def main():
    number_of_cities = 16
    number_of_generations = 1000

    population_size = 1000
    luck_factor = 0
    survival_rate = 0.05
    mutation_rate = 0.14

    print_exact_solution = True
    print_distances = False
    debug_count = 100

    locations = generate_locations(number_of_cities)
    cost_table = construct_euclidean_distance_table(locations)

    if print_exact_solution:
        permutation, distance = solve_tsp_dynamic_programming(cost_table)
        print("exact solution:", permutation, "  cost:", distance)

    routes = generate_random_routes(population_size, number_of_cities)
    print("locations", locations)
    if print_distances: print("distances:\n", cost_table)
    print("routes:\n", routes)

    rank_routes(routes, 0, cost_table)
    print("initial smallest cost:", calculate_route_cost(routes[0], cost_table))

    for i in range(number_of_generations):
        routes = breed_generation_elitest(routes, luck_factor, survival_rate, mutation_rate, cost_table)
        if i % debug_count == 0:
            rank_routes(routes, 0, cost_table)
            print("generation:", i, " smallest cost:", calculate_route_cost(routes[0], cost_table))

    rank_routes(routes, 0, cost_table)
    print("final smallest cost:", calculate_route_cost(routes[0], cost_table))
    print(routes[0])


if __name__ == "__main__":
    main()
