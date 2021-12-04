import copy
import math

import numpy as np
import json
from python_tsp.exact import solve_tsp_dynamic_programming
from genetic_algorithm import *

tests = {}

if __name__ == "__main__":

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
        print(f"population: {population_size}, initial smallest cost: {calculate_route_cost(population_routes[0], cost_table)}")

        for luck_factor_10 in range(0, 10, skip):
            luck_factor = luck_factor_10 / 10

            for survival_rate_100 in range(1, 11, skip):
                survival_rate = survival_rate_100 / 100
                print(luck_factor_10 * 10 + survival_rate_100, "of 100")

                for mutation_rate_10 in range(0, 10, skip):
                    mutation_rate = mutation_rate_10 / 10

                    #print(f"\n    luck: {luck_factor}, survival: {survival_rate}, mutation: {mutation_rate}")

                    routes = copy.deepcopy(population_routes)

                    cost = math.inf
                    generation = 0
                    while cost - target_cost > 0.00004 and generation < maximum_generations:
                        routes = breed_generation_elitest(routes, luck_factor, survival_rate, mutation_rate, 3, cost_table)
                        rank_routes(routes, 0, cost_table)
                        cost = calculate_route_cost(routes[0], cost_table)
                        generation += 1

                    tests[str((population_size, luck_factor, survival_rate, mutation_rate))] = generation

                    #print(f"    final smallest cost: {cost}, generation: {generation}\n")

    with open(".\\tests\\test.json", 'w') as test_file:
        json.dump(tests, test_file)





