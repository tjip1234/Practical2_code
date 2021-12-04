import json

base_population_size = 500
base_luck_factor = 0.1
base_survival_rate = 0.05
base_mutation_rate = 0.1

if __name__ == "__main__":

    with open(".\\tests\\generations_test.json", 'r') as test_file:
        tests = json.load(test_file)

    str_hyper_parameters = list(tests.keys())
    str_hyper_parameters.sort(key=lambda x: tests[x])

    base_values = {

    }



