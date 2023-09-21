import os
import json
import random

def pos_tuple_to_string(tuple):
    return f'{tuple[0]},{tuple[1]}'

def generate_random_pos(size):
    return (random.randrange(0, size), random.randrange(0, size))

def is_valid_problem(size, initial, goal, obstacles):
    # Breadth-first search algorithm to find path
    visited = []
    queue = [initial]

    actions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while len(queue) > 0:
        point = queue.pop()

        # Path has been found so return
        if point == goal:
            return True

        for dx, dy in actions:
            x, y = point[0] + dx, point[1] + dy
            next_point = (x, y)

            is_in_grid = 0 < x and x < size and 0 < y and y < size
            is_free_point = next_point not in obstacles and next_point not in visited

            if is_in_grid and is_free_point:
                visited.append(next_point)
                queue.insert(0, next_point)

    # Was unable to find path
    return False

def generate_navigation2d(size, obstacle_count):
    if (obstacle_count < 0):
        max_obstacles = size * size - 2 * size
        obstacle_count = random.randint(1, max(max_obstacles, 1))

    # Loop until a valid configuration is found
    while True:
        initial = generate_random_pos(size)
        goal = generate_random_pos(size)

        obstacles = []
        for i in range(obstacle_count):
            obstacles.append(generate_random_pos(size))

        # If valid config, we can break
        has_dup_obstacle = len(obstacles) != len(set(obstacles))
        if not (initial == goal or initial in obstacles or goal in obstacles or has_dup_obstacle):
            if (is_valid_problem(size, initial, goal, obstacles)): # Only use if there is a valid path
                break


    return {
        "size": f'{size},{size}',
        "initial": pos_tuple_to_string(initial),
        "goal": pos_tuple_to_string(goal),
        "obstacles": list(map(pos_tuple_to_string, obstacles)),
    }

def generate_cases(input_data, domain, representation, nshot, output_filename):
    data = []

    output_data = {
        "domain": domain,
        "representation": representation,
        "nshot": nshot
    }

    if (domain == "navigation-2d"):
        size = input_data.get("size", 2)
        count  = input_data.get("count", 5)
        obstacles  = input_data.get("obstacles", -1)
        for i in range(count):
            data.append(generate_navigation2d(size, obstacles))


    output_data["data"] = data

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, "w") as output_file:
        output_file.write(json.dumps(output_data, indent = 4))

    return output_data