import copy
import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def minus(self, b):
        a = copy.copy(self)
        a.x = a.x - b.x
        a.y = a.y - b.y
        a.z = a.z - b.z
        return a

    def distance(self, b):
        t = math.sqrt((self.x - b.x) ** 2 + (self.y - b.y) ** 2 + (self.z - b.z) ** 2)
        return t


class Straight:
    def __init__(self, a, b):
        self.start = a
        self.vector = b.minus(a)


class Plane:
    def __init__(self, a, b):
        self.A = a.vector.y * b.vector.z - b.vector.y * a.vector.z
        self.B = a.vector.z * b.vector.x - a.vector.x * b.vector.z
        self.C = a.vector.x * b.vector.y - a.vector.y * b.vector.x
        self.D = -(self.A * a.start.x + self.B * a.start.y + self.C * a.start.z)

    def move(self, dot):
        a = copy.copy(self)
        a.D = -(self.A * dot.x + self.B * dot.y + self.C * dot.z)
        return a

    def cross(self, str):
        if self.A * str.vector.x + self.B * str.vector.y + self.C * str.vector.z == 0:
            return Point(str.start.x, str.start.y, str.start.z)
        t = -(self.A * str.start.x + self.B * str.start.y + self.C * str.start.z + self.D) / \
            (self.A * str.vector.x + self.B * str.vector.y + self.C * str.vector.z)

        x = str.start.x + str.vector.x * t
        y = str.start.y + str.vector.y * t
        z = str.start.z + str.vector.z * t
        return Point(x, y, z)

    def normal(self, a):
        n = copy.copy(self)
        t = -(self.A * a.x + self.B * a.y + self.C * a.z + self.D) / \
            (self.A * n.A + self.B * n.B + self.C * n.C)
        x = a.x + n.A * t
        y = a.y + n.B * t
        z = a.z + n.C * t
        return Point(x, y, z)


class Light:
    def __init__(self, vector, start, energy):
        self.vector = vector
        self.start = start
        self.energy = energy


def read():
    x, y, z = map(float, fin.readline().split())
    return Point(x, y, z)


def planes_of_cube(A, B, C, D):
    cube = []
    cube.append(Plane(Straight(B, A), Straight(B, C)))
    cube.append(Plane(Straight(C, B), Straight(C, D)))

    cube.append(cube[1].move(A))
    cube.append(cube[0].move(D))

    BC = Straight(B, C)
    temp = copy.copy(cube[0])
    temp.A = BC.vector.x
    temp.B = BC.vector.y
    temp.C = BC.vector.z
    cube.append(temp.move(B))
    cube.append(temp.move(C))
    return cube


def cube_dots(A, B, C, D):
    cube = []

    E = dot_4th(A, B, C)
    abce = [A, B, C, E]

    G = dot_4th(C, B, D)
    cbdg = [C, B, D, G]

    F = dot_4th(C, D, E)
    cdef = [C, D, E, F]

    H = dot_4th(B, A, G)
    bagh = [B, A, G, H]

    aefh = [A, E, F, H]

    hfdg = [H, F, D, G]

    cube.append(abce)
    cube.append(cbdg)
    cube.append(aefh)
    cube.append(hfdg)
    cube.append(bagh)
    cube.append(cdef)
    return cube


def mirror(a, b, c):
    return Plane(Straight(b, a), Straight(b, c))


def dot_4th(a, b, c):
    if (b.x - a.x) * (c.x - b.x) + (b.y - a.y) * (c.y - b.y) + (b.z - a.z) * (c.z - b.z) == 0:
        dx = a.x + c.x - b.x
        dy = a.y + c.y - b.y
        dz = a.z + c.z - b.z
    else:
        dx = c.x + b.x - a.x
        dy = c.y + b.y - a.y
        dz = c.z + b.z - a.z
    return Point(dx, dy, dz)


def belong(a, cros):
    b = Straight(a.start, cros)
    if a.vector.x * b.vector.x >= 0 and a.vector.y * b.vector.y >= 0 and a.vector.z * b.vector.z >= 0:
        return 1
    else:
        return 0


fin = open('input.txt')
fout = open('output.txt', 'w')

a = read()
b = read()
c = read()
d = read()
cubePlanes = planes_of_cube(a, b, c, d)
cube = cube_dots(a, b, c, d)

light = Light(read(), read(), int(fin.readline()))

n = int(fin.readline().split()[0])
mirrorsPlanes = []
mirrors = []
for i in range(n):
    a = read()
    b = read()
    c = read()
    d = dot_4th(a, b, c)
    mirrorsPlanes.append(mirror(a, b, c))

    temp = [a, b, c, d]
    mirrors.append(temp)
fin.close()


while light.energy != 0:
    minimum = 99999999.9
    j = 0
    for i in mirrorsPlanes:
        crossPoint = i.cross(light)
        if crossPoint.x != light.start.x or crossPoint.y != light.start.y or crossPoint.z != light.start.z:
            dist = light.start.distance(crossPoint)
            if dist < minimum and belong(light, crossPoint) == 1:
                minimum = dist
                plane = i
        j += 1
    j = 0
    for i in cubePlanes:
        crossPoint = i.cross(light)
        if crossPoint.x != light.start.x or crossPoint.y != light.start.y or crossPoint.z != light.start.z:
            dist = light.start.distance(crossPoint)
            if dist < minimum and belong(light, crossPoint) == 1:
                fout.write(str(1) + '\n')
                fout.write(str(light.energy) + '\n')
                fout.write(str(crossPoint.x) + ' ' + str(crossPoint.y) + ' ' + str(crossPoint.z) + '\n')
                fout.write(str(light.vector.x) + ' ' + str(light.vector.y) + ' ' + str(light.vector.z) + '\n')
                exit(0)
        j += 1

    light.energy -= 1
    crossPoint = plane.cross(light)
    point1 = plane.normal(light.start)
    point2 = Point(2 * crossPoint.x - point1.x, 2 * crossPoint.y - point1.y, 2 * crossPoint.z - point1.z)
    v = Straight(point1, light.start)

    point2.x = point2.x + v.vector.x
    point2.y = point2.y + v.vector.y
    point2.z = point2.z + v.vector.z

    point2.x = point2.x - crossPoint.x
    point2.y = point2.y - crossPoint.y
    point2.z = point2.z - crossPoint.z


    light.start = crossPoint
    light.vector = point2

fout.write(str(0) + '\n')
fout.write(str(crossPoint.x) + ' ' + str(crossPoint.y) + ' ' + str(crossPoint.z))

fout.close()
