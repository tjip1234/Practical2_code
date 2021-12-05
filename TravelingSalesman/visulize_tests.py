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

        plt.show()


if __name__ == "__main__":

    #scatter_parameter_cost("Survival Rate", 100, 100)
    plot_trainings("tests\\training_survival_rate.json")





