import math


def normal_moving_direction(my_position, position_to_attack, data, failed=False):
    distance = calc_distance(my_position, position_to_attack)
    if distance > 0:
        distance = create_distance_list(my_position, position_to_attack)
        if failed:
            if abs(distance[0]) >= abs(distance[1]):
                return [0, distance[1] / abs(distance[1])]
            else:
                return [distance[0] / abs(distance[0]), 0]
        else:
            if abs(distance[0]) >= abs(distance[1]):
                return [distance[0] / abs(distance[0]), 0]
            else:
                return [0, distance[1] / abs(distance[1])]
    else:
        return [0, 0]


def move_to_nearest_of_list(my_position, objects, data):
    nearest = None
    for i in objects:
        if nearest is None or calc_distance(my_position, nearest.pos) > calc_distance(my_position, i.pos):
            nearest = i

    if nearest is not None:
        return a_star(data, my_position, nearest.pos)
    else:
        return [0, 0]


def a_star(data, pos1, pos2, diagonal_allowed=False, above_ents=False):  # A* algorithm
    value = 1
    open_nodes = [pos1[:]]
    closed_nodes = []
    came_from = {}
    gscore = {tuple(pos1): 0}

    if diagonal_allowed:
        fscore = {tuple(pos1): __h_diagonal(pos1, pos2)}
        while open_nodes:
            lowest_node = open_nodes[0]
            for i in open_nodes:
                if i == pos2:
                    return __reconstruct_path(came_from, tuple(i))
                elif fscore[tuple(i)] < fscore[tuple(lowest_node)]:
                    lowest_node = i

            open_nodes.remove(lowest_node)
            closed_nodes.append(lowest_node)

            for i in __neighbours_diagonally(data, lowest_node, above_ents):
                if i not in closed_nodes:
                    new_score = gscore[tuple(lowest_node)] + 1

                    if i not in open_nodes or new_score < gscore[tuple(i)]:
                        came_from[tuple(i)] = tuple(lowest_node)
                        gscore[tuple(i)] = new_score
                        fscore[tuple(i)] = new_score + __h_diagonal(i, pos2)

                    if i not in open_nodes:
                        open_nodes.append(i)

    else:
        fscore = {tuple(pos1): __h_orthogonal(pos1, pos2)}
        while open_nodes:
            lowest_node = open_nodes[0]

            for i in open_nodes:
                if i == pos2:
                    return __reconstruct_path(came_from, tuple(i))
                elif fscore[tuple(i)] < fscore[tuple(lowest_node)]:
                    lowest_node = i

            open_nodes.remove(lowest_node)
            closed_nodes.append(lowest_node)

            for i in __neighbours_orthogonally(data, lowest_node, above_ents):
                if i not in closed_nodes:
                    new_score = gscore[tuple(lowest_node)] + 1

                    if i not in open_nodes or new_score < gscore[tuple(i)]:
                        came_from[tuple(i)] = tuple(lowest_node)
                        gscore[tuple(i)] = new_score
                        fscore[tuple(i)] = new_score + __h_orthogonal(i, pos2)

                    if i not in open_nodes:
                        open_nodes.append(i)

    return [0, 0]


def __neighbours_diagonally(data, pos, above_ents=False):
    xrange = [pos[1] - 1, pos[1] + 2]
    yrange = [pos[0] - 1, pos[0] + 2]
    for i in range(yrange[0], yrange[1]):
        for j in range(xrange[0], xrange[1]):
            if not (i == pos[0] and j == pos[1]) and allowed_position([i, j], data, above_ents):
                yield [i, j]


def __neighbours_orthogonally(data, pos, above_ents=False):
    if allowed_position([pos[0] + 1, pos[1]], data, above_ents):
        yield [pos[0] + 1, pos[1]]
    if allowed_position([pos[0] - 1, pos[1]], data, above_ents):
        yield [pos[0] - 1, pos[1]]
    if allowed_position([pos[0], pos[1] + 1], data, above_ents):
        yield [pos[0], pos[1] + 1]
    if allowed_position([pos[0], pos[1] - 1], data, above_ents):
        yield [pos[0], pos[1] - 1]


def __reconstruct_path(came_from, current):
    path = [current]
    while current in came_from.keys():
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def __h_diagonal(node, pos2):
    if abs(node[0] - pos2[0]) < abs(node[1] - pos2[1]):
        return abs(node[1] - pos2[1])
    else:
        return abs(node[0] - pos2[0])


def __h_orthogonal(node, pos2):
    return abs(pos2[0] - node[0]) + abs(pos2[1] - node[1])


def calc_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def create_distance_list(pos1, pos2):
    return [pos2[0] - pos1[0], pos2[1] - pos1[1]]


def genCirclePath(ent, data):
    radius = ent.radius
    path = []
    angles = []

    for i in range(radius * 8):
        angles.append(360 / float(radius * 8) * i)

    for i in angles:
        newpoint = genCirclePos(i, radius, ent.pos2)
        if data.position_in_world(newpoint):
            path.append(newpoint)

    return path


def genCirclePos(angle, rad, middle):
    relativePos = [0, 0]

    radRadians = math.radians(angle)
    relativePos[0] = int(math.cos(radRadians) * rad)
    relativePos[1] = int(math.sin(radRadians) * rad)

    Point = [middle[0] - relativePos[0], middle[1] - relativePos[1]]

    return Point


def allowed_position(pos, data, above_ents=False):
    # checks if the position is in a room and if necessary if an entity is there
    if not data.position_in_world(pos):
        return False
    if not above_ents:
        for i in data.ents:
            if pos == i.pos:
                return False
    return True

