import numpy as np
import sys
from string import ascii_lowercase
from copy import deepcopy
import matplotlib.pyplot as plt

from utilities.utils import get_puzzle

letters = list(ascii_lowercase)


def get_moves(start, arr, move_store, route_id, previous_position=None):
    possible_moves = []
    for m in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
        pm = deepcopy(start)
        pm[0] += m[0]
        pm[1] += m[1]
        if pm[0] >= 0 and pm[0] < arr.shape[0] and pm[1] >= 0 and pm[1] < arr.shape[1]:
            if pm in move_store[route_id]:
                pass
                # print(f"Discarding {pm} as previously visited")
            else:
                # print(f"Route = {move_store[route_id]}")
                start_height = arr[start[0], start[1]]
                dst_height = arr[pm[0], pm[1]]
                start_height = "a" if start_height == "S" else start_height
                dst_height = "z" if dst_height == "E" else dst_height
                if letters.index(dst_height) - letters.index(start_height) < 2:
                    possible_moves.append(pm)
    return possible_moves


def make_move(current_position, move):
    previous_position = deepcopy(current_position)
    current_position[0] = move[0]
    current_position[1] = move[1]
    return current_position, previous_position


def draw_route(route, shape):
    z = np.zeros(shape)
    for j, i in enumerate(route):
        z[i[0], i[1]] = j + 1
    plt.imshow(z)


def play_turn(current_position, arr, move_store, route_id=0, previous_position=None):
    if arr[current_position[0], current_position[1]] == "E":
        return True, current_position, previous_position, move_store
    moves = get_moves(current_position, arr, move_store, route_id, previous_position)
    if len(moves) == 0:
        return False, current_position, previous_position, move_store
    route = deepcopy(move_store[route_id])
    for i, move in enumerate(moves):
        if i > 0: # need to make a new route
            new_route = deepcopy(route)
            new_route.append(move)
            new_route_id = max(move_store.keys()) + 1
            print(f"exploring new route -> {new_route_id}")
            move_store[new_route_id] = new_route
            cp, pp = make_move(current_position, move)
            _, cp, pp, move_store = play_turn(cp, arr, move_store, new_route_id, pp)
        else:
            move_store[route_id].append(move)
            cp, pp = make_move(current_position, move)
            _, cp, pp, move_store = play_turn(cp, arr, move_store, route_id, pp)
    return False, cp, pp, move_store


def solve(arr: np.ndarray):
    start_point = np.where(arr=="S")
    start_point = [int(start_point[0]), int(start_point[1])]
    finished, cp, pp, moves = play_turn(deepcopy(start_point), arr, {0: [start_point]})
    # finished, cp, pp, moves = play_turn([0, 0], arr, {0: [start_point]})
    print(f"Paths sampled = {len(moves.keys())}")
    successful_routes = [k for k in moves.keys() if arr[moves[k][-1][0], moves[k][-1][1]] == "E"]
    print(f"Successful paths = {len(successful_routes)}")
    shortest_route = min([len(moves[k]) - 1 for k in successful_routes])
    i = [k for k in successful_routes if len(moves[k]) - 1 == shortest_route]
    print(f"{len(i)} routes where found with path length of {shortest_route}")
    return moves[i[0]]


if __name__ == "__main__":
    data = get_puzzle(year=2022, day=12)
    data = data.split("\n")

    # path = "../data/sample_12.txt"
    # with open(path, 'r') as file:
    #     # Read the contents of the file into a list
    #     data = file.readlines()
    # data = [x.replace("\n", "") for x in data]
    arr = np.array([list(d) for d in data])
    route = solve(arr)
    draw_route(route)