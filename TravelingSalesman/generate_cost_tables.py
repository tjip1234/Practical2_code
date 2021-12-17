from genetic_algorithm import *

if __name__ == "__main__":
    number_of_cities = 10

    locations = generate_locations(number_of_cities)
    file_name = f"euclidean_{number_of_cities}"

    cost_table = construct_euclidean_distance_table(locations)
    print(cost_table)
    np.savetxt(f".\\cost_tables\\euclidean_{number_of_cities}.txt", cost_table)

