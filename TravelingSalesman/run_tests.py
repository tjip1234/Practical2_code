import copy
import math

import numpy as np
import json
from python_tsp.exact import solve_tsp_dynamic_programming
from genetic_algorithm import *

tests = {}


def target_generation_test():
    cost_type = "euclidean"
    number_of_cities = 14
    cost_table = np.loadtxt(f".\\cost_tables\\{cost_type}_{number_of_cities}.txt")
    print(cost_table)

    maximum_generations = 100
    skip = 1

    target_permutation, target_cost = solve_tsp_dynamic_programming(cost_table)
    print("exact solution:", target_permutation, "  cost:", target_cost)

    print(f"Starting tests...")

    for population_size in range(100, 1000, 100 * skip):
        population_routes = generate_random_routes(population_size, number_of_cities)
        rank_routes(population_routes, 0, cost_table)
        print(
            f"population: {population_size}, initial smallest cost: {calculate_route_cost(population_routes[0], cost_table)}")

        for luck_factor_10 in range(0, 10, skip):
            luck_factor = luck_factor_10 / 10

            for survival_rate_100 in range(1, 11, skip):
                survival_rate = survival_rate_100 / 100
                print(luck_factor_10 * 10 + survival_rate_100, "of 100")

                for mutation_rate_10 in range(0, 10, skip):
                    mutation_rate = mutation_rate_10 / 10

                    # print(f"\n    luck: {luck_factor}, survival: {survival_rate}, mutation: {mutation_rate}")

                    routes = copy.deepcopy(population_routes)

                    cost = math.inf
                    generation = 0
                    while cost - target_cost > 0.00004 and generation < maximum_generations:
                        routes = breed_generation_elitest(routes, luck_factor, survival_rate, mutation_rate, 3,
                                                          cost_table)
                        rank_routes(routes, 0, cost_table)
                        cost = calculate_route_cost(routes[0], cost_table)
                        generation += 1

                    tests[str((population_size, luck_factor, survival_rate, mutation_rate))] = generation

                    # print(f"    final smallest cost: {cost}, generation: {generation}\n")

    with open(".\\tests\\test.json", 'w') as test_file:
        json.dump(tests, test_file)


def linear_map(value, minimum, maximum, total_tests):
    return minimum + value * ((maximum - minimum)/(total_tests - 1))


def unbounded_cost_test():
    cost_type = "euclidean"
    number_of_cities = 100
    cost_table = np.loadtxt(f".\\cost_tables\\{cost_type}_{number_of_cities}.txt")
    print(cost_table)

    maximum_generations = 100
    tests_per_parameter = 6

    print(f"Starting unbounded tests...")

    for population_size in range(0, 2):
        population_size = int(linear_map(population_size, 100, 300, 2))

        population_routes = generate_random_routes(population_size, number_of_cities)
        rank_routes(population_routes, 0, cost_table)
        print(f"population: {population_size}, initial smallest cost: {calculate_route_cost(population_routes[0], cost_table)}")

        for luck_factor in range(0, tests_per_parameter):
            luck_factor = linear_map(luck_factor, 0, 0.5, tests_per_parameter)

            for survival_rate in range(0, tests_per_parameter):
                survival_rate = linear_map(survival_rate, 0.01, 0.99, tests_per_parameter)

                for mutation_rate in range(0, tests_per_parameter):
                    mutation_rate = linear_map(mutation_rate, 0, 0.5, tests_per_parameter)

                    # print(f"\n    luck: {luck_factor}, survival: {survival_rate}, mutation: {mutation_rate}")

                    routes = copy.deepcopy(population_routes)

                    min_cost = math.inf
                    for generation in range(maximum_generations):
                        routes = breed_generation_elitest(routes, luck_factor, survival_rate, mutation_rate, 3, cost_table)
                        rank_routes(routes, 0, cost_table)
                        cost = calculate_route_cost(routes[0], cost_table)
                        min_cost = cost if cost < min_cost else min_cost

                    tests[str((population_size, luck_factor, survival_rate, mutation_rate))] = min_cost

                    # print(f"    final smallest cost: {cost}, generation: {generation}\n")

    file_name = f".\\tests\\unbounded_cost_{number_of_cities}_{maximum_generations}.json"
    previous_tests = {}

    try:
        with open(file_name, 'r') as test_file:
            previous_tests = json.load(test_file)
    except:
        pass

    with open(file_name, 'w') as test_file:
        json.dump(previous_tests | tests, test_file)


if __name__ == "__main__":
    unbounded_cost_test()
