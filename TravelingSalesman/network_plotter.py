import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.animation import FuncAnimation


def plot_paths(file_name, length_sec=10):
    with open(file_name, 'r') as test_file:
        inp = json.load(test_file)

    hyper_parameters = inp["hyper_parameters"]
    number_of_cities = inp["number_of_cities"]
    generations = inp["generations"]
    locations = inp["locations"]
    paths = inp["paths"]

    fig, ax = plt.subplots()
    plt.suptitle("Best Path of Each Generation", fontsize=14)
    fig.patch.set_facecolor('white')

    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.axis('square')

    def update(frame):
        print(frame)
        path = paths[frame]
        ax.cla()

        ax.set_title(f"Generation {frame} of {len(paths)}")

        for i, (x, y) in enumerate(locations):
            ax.add_patch(plt.Circle((x, y), 0.1, color='b' if i != 0 else 'r'))

        path.insert(0, 0)
        path.append(0)
        for i in range(len(path) - 1):
            x1, y1 = locations[path[i]]
            x2, y2 = locations[path[i+1]]
            ax.plot((x1, x2), (y1, y2), color='black')

    anim = FuncAnimation(fig, update, frames=len(paths), interval=1)
    print("Saving")
    anim.save(file_name[:-5] + '.gif', dpi=120, writer='imagemagick')


if __name__ == "__main__":
    plot_paths("tests\\nodes_50_1000.json")
    #plot_paths("tests\\nodes_100_100.json")
    #plot_graphs([[(0, 1), (1, 2), (1, 3)]])
