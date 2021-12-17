import copy
import json
from matplotlib import pyplot as plt

from genetic_algorithm import *
from run_tests import linear_map, hyper_parameter_names


def scatter_parameter_cost(parameter_name: str, n_cities: int, n_generations: int):

    with open(f".\\tests\\unbounded_cost_{n_cities}_{n_generations}.json", 'r') as test_file:
        raw_results = json.load(test_file)

    str_hyper_parameters = list(raw_results.keys())
    str_hyper_parameters.sort(key=lambda x: raw_results[x])
    results = {tuple(float(param) for param in key[1:-1].split(", ")): raw_results[key] for key in str_hyper_parameters}

    parameter_index = hyper_parameter_names.index(parameter_name)
    x = [params[parameter_index] for params in results.keys()]
    y = results.values()

    plt.suptitle("Hyper Parameter Grid Search", fontsize=14)
    plt.title(f"Shortest path through {n_cities} cities over {n_generations} generations", fontsize=12)
    plt.xlabel(parameter_name, fontsize=12)
    plt.ylabel("Euclidean Distance (lower is better)", fontsize=12)
    plt.scatter(x, y)
    plt.show()


def plot_trainings(file_name: str):

    with open(file_name, 'r') as test_file:
        inp = json.load(test_file)
        base_hyper_parameters = inp["base_hyper_parameters"]
        variable_parameter_name = inp["variable_parameter_name"]
        number_of_cities = inp["number_of_cities"]
        generations = inp["generations"]
        maximum = inp["maximum"]
        results = inp["results"]

        plt.suptitle("Training", fontsize=14)
        plt.xlabel("Generation", fontsize=12)
        plt.ylabel("Euclidean Distance (lower is better)", fontsize=12)

        variable_index = hyper_parameter_names.index(variable_parameter_name)

        for i, (x, y) in enumerate(results):
            new_value = linear_map(i, base_hyper_parameters[variable_index], maximum, len(results))

            plt.plot(x, y, label=f"{variable_parameter_name}: {new_value:.3f}")
            plt.legend()

        plt.savefig(f'{file_name[:-4]}png', dpi=1200)


def plot_graph(file_name: str):

    with open(file_name, 'r') as test_file:
        inp = json.load(test_file)
        base_hyper_parameters = inp["base_hyper_parameters"]
        variable_parameter_name = inp["variable_parameter_name"]
        number_of_cities = inp["number_of_cities"]
        generations = inp["generations"]
        maximum = inp["maximum"]
        results = inp["results"]

        plt.suptitle("Training", fontsize=14)
        plt.xlabel("Generation", fontsize=12)
        plt.ylabel("Euclidean Distance (lower is better)", fontsize=12)

        variable_index = hyper_parameter_names.index(variable_parameter_name)

        for i, (x, y) in enumerate(results):
            new_value = linear_map(i, base_hyper_parameters[variable_index], maximum, len(results))

            plt.plot(x, y, label=f"{variable_parameter_name}: {new_value:.3f}")
            plt.legend()

        plt.show()


def no_crossover(hyper_parameters: (int, float, float, float), number_of_cities, generations):
    locations = generate_locations(number_of_cities)
    cost_table = construct_euclidean_distance_table(locations)

    plt.suptitle("Training", fontsize=14)
    plt.xlabel("Generation", fontsize=12)
    plt.ylabel("Euclidean Distance (lower is better)", fontsize=12)

    population_size, luck_factor, survival_rate, mutation_rate = hyper_parameters

    routes = generate_random_routes(population_size, number_of_cities)
    rank_routes(routes, 0, cost_table)

    x = list(range(generations))
    y = []
    for generation in range(generations):
        print("generation: ", generation)
        #print([calculate_route_cost(route, cost_table) for route in routes])
        sample_size = int(population_size*survival_rate)
        routes = routes[:sample_size]
        routes.extend([copy.deepcopy(random.choice(routes)) for _ in range(population_size-sample_size)])
        #print([calculate_route_cost(route, cost_table) for route in routes])
        for route in routes[10:]:
            swap_mutation(route, mutation_rate)
        rank_routes(routes, 0, cost_table)
        #print([calculate_route_cost(route, cost_table) for route in routes])
        y.append(calculate_route_cost(routes[0], cost_table))

    print(y)
    plt.plot(x, y)

    file_name = f"tests\\no_crossover_{number_of_cities}_{generations}.png"

    plt.savefig(file_name, dpi=1200)



if __name__ == "__main__":

    #scatter_parameter_cost("Survival Rate", 100, 100)
    #plot_trainings("tests\\training_survival_rate_99.json")
    no_crossover((100, 0, 0.01, 0.1), 100, 10000)






