import math
import copy


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

    @staticmethod
    def equal(a, b):
        if -0.0001 <= math.fabs(a.x - b.x) <= 0.0001 and \
                -0.0001 <= math.fabs(a.y - b.y) <= 0.0001 and \
                -0.0001 <= math.fabs(a.z - b.z) <= 0.0001:
            return 1
        else:
            return 0

    @staticmethod
    def equalPair(a1, a2, b1, b2):
        if -0.0001 <= math.fabs(a1.x - b1[0]) <= 0.0001 and \
                -0.0001 <= math.fabs(a1.y - b1[1]) <= 0.0001 and \
                -0.0001 <= math.fabs(a1.z - b1[2]) <= 0.0001 and \
                -0.0001 <= math.fabs(a2.x - b2[0]) <= 0.0001 and \
                -0.0001 <= math.fabs(a2.y - b2[1]) <= 0.0001 and \
                -0.0001 <= math.fabs(a2.z - b2[2]) <= 0.0001 or \
                -0.0001 <= math.fabs(a1.x - b2[0]) <= 0.0001 and \
                -0.0001 <= math.fabs(a1.y - b2[1]) <= 0.0001 and \
                -0.0001 <= math.fabs(a1.z - b2[2]) <= 0.0001 and \
                -0.0001 <= math.fabs(a2.x - b1[0]) <= 0.0001 and \
                -0.0001 <= math.fabs(a2.y - b1[1]) <= 0.0001 and \
                -0.0001 <= math.fabs(a2.z - b1[2]) <= 0.0001:
            return 1
        else:
            return 0


class Straight:
    def __init__(self, a, b):
        self.start = a
        self.vector = b.minus(a)


class PlaneCheck:
    def __init__(self, a, b):
        self.A = a.vector.y * b.vector.z - b.vector.y * a.vector.z
        self.B = a.vector.z * b.vector.x - a.vector.x * b.vector.z
        self.C = a.vector.x * b.vector.y - a.vector.y * b.vector.x
        self.D = -(self.A * a.start.x + self.B * a.start.y + self.C * a.start.z)

    def inside(self, a):
        if self.A * a.x + self.B * a.y + self.C * a.z + self.D == 0:
            return 1
        else:
            return 0


class Plane:
    def __init__(self):
        n1, n2, n3, r1, r2, r3 = map(float, fin.readline().split())
        self.a = n1
        self.b = n2
        self.c = n3
        self.d = -(n1 * r1 + n2 * r2 + n3 * r3)


class Polyhedron:
    size = 0
    number_of_segments = 0
    segments = []
    vertexes = []

    def __init__(self):
        self.planes = []

    def push(self, a):
        self.planes.append(a)
        self.size += 1

    def inside(self, a):
        fl = 1
        for i in self.planes:
            if i.a * a.x + i.b * a.y + i.c * a.z + i.d > 0:
                fl = 0
        return fl

    def exists(self, a):
        for q in self.vertexes:
            if Point.equal(a, q) == 1:
                return 1
        return 0

    def exists_pair(self, a, temp):
        for q in self.segments:
            if Point.equalPair(a, temp, q[0], q[1]) == 1:
                return 1
        return 0

    def to_segments(self):
        for i in range(0, self.size - 1):
            for j in range(i + 1, self.size):
                fl = 0
                temp = 0
                for k in range(0, self.size):
                    a = Matrix.cramer(self.planes[i], self.planes[j], self.planes[k])
                    if a != -1 and self.inside(a) == 1:

                        if fl == 0:
                            temp = a
                            fl = 1
                            if Polyhedron.exists(self, a) == 0:
                                self.vertexes.append(a)

                        if fl == 1:
                            if Polyhedron.exists_pair(self, a, temp) == 0 and not(temp.x == a.x and temp.y == a.y
                                                                                  and temp.z == a.z):
                                self.segments.append([[temp.x, temp.y, temp.z], [a.x, a.y, a.z]])
                                self.number_of_segments += 1
                                if Polyhedron.exists(self, a) == 0:
                                    self.vertexes.append(a)


class Matrix:
    def __init__(self, a, b, c):
        self.matrix = []
        self.matrix.append(a)
        self.matrix.append(b)
        self.matrix.append(c)

    def determinant(self):
        t1 = self.matrix[0][0] * self.matrix[1][1] * self.matrix[2][2]
        t2 = self.matrix[0][2] * self.matrix[1][0] * self.matrix[2][1]
        t3 = self.matrix[0][1] * self.matrix[1][2] * self.matrix[2][0]
        t4 = self.matrix[0][2] * self.matrix[1][1] * self.matrix[2][0]
        t5 = self.matrix[0][0] * self.matrix[1][2] * self.matrix[2][1]
        t6 = self.matrix[0][1] * self.matrix[1][0] * self.matrix[2][2]
        return t1 + t2 + t3 - t4 - t5 - t6

    @staticmethod
    def cramer(a, b, c):
        matr = Matrix([a.a, a.b, a.c], [b.a, b.b, b.c], [c.a, c.b, c.c])
        matr1 = Matrix([-a.d, a.b, a.c], [-b.d, b.b, b.c], [-c.d, c.b, c.c])
        matr2 = Matrix([a.a, -a.d, a.c], [b.a, -b.d, b.c], [c.a, -c.d, c.c])
        matr3 = Matrix([a.a, a.b, -a.d], [b.a, b.b, -b.d], [c.a, c.b, -c.d])

        dt = matr.determinant()
        if dt == 0:
            return -1
        dt1 = matr1.determinant()
        dt2 = matr2.determinant()
        dt3 = matr3.determinant()

        x = dt1 / dt
        y = dt2 / dt
        z = dt3 / dt

        return Point(x, y, z)


fin = open('input.txt')
fout = open('output.txt', 'w')

number_of_planes = int(fin.readline())
polyhedron = Polyhedron()
for i in range(number_of_planes):
    polyhedron.push(Plane())

polyhedron.to_segments()
if len(polyhedron.vertexes) >= 4:
    r1 = polyhedron.vertexes[0]
    r2 = polyhedron.vertexes[1]
    r3 = polyhedron.vertexes[2]
    r12 = Straight(r1, r2)
    r13 = Straight(r1, r3)
    test = PlaneCheck(r12, r13)

    fl = 0
    for i in polyhedron.vertexes:
        if test.inside(i) == 0:
            fl = 1
else:
    fl = 0

if fl == 0:
    fout.write('0')
else:
    fout.write(str(polyhedron.number_of_segments) + '\n')
    for i in polyhedron.segments:
        fout.write(str(i[0][0]) + ' ' + str(i[0][1]) + ' ' + str(i[0][2]) + ' ')
        fout.write(str(i[1][0]) + ' ' + str(i[1][1]) + ' ' + str(i[1][2]) + '\n')

fin.close()
fout.close()
