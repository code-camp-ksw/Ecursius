import math


def normalMoveDir(myPos, entPos, data, failed=False):
    distance = [entPos[0] - myPos[0], entPos[1] - myPos[1]]
    if distance != [0, 0]:
        if math.fabs(distance[0]) >= math.fabs(distance[1]):
            return [distance[0] / int(math.fabs(distance[0])), 0]
        else:
            return [0, distance[1] / int(math.fabs(distance[1]))]
    else:
        return [0, 0]


def moveToNearestOfList(myPos, objects, data):
    nearest = None
    for i in objects:
        if nearest is None or calc_distance(myPos, nearest.pos) > calc_distance(myPos, i.pos):
            nearest = i

    if nearest is not None:
        return normalMoveDir(myPos, nearest.pos, data)
    else:
        return [0, 0]


def calc_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


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


def allowed_position(pos, data, above_ents = False):
    if not data.position_in_world(pos):
        return False
    if above_ents:
        for i in data.ents:
            if pos == i.pos:
                return False
    return True
