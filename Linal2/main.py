import math

def side(x1, y1, x2, y2):
    x1, y1 = y1, x1
    x1 = -x1
    angle = (x1 * x2 + y1 * y2) / (math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2))
    angle = math.acos(angle) * 180 / math.pi
    if 0 <= angle <= 60:
        return 1
    elif 120 <= angle <= 180:
        return -1
    elif 60 <= angle <= 90:
        return 2
    else:
        return -2

def rotate(x1, y1, x2, y2):
    angle = (x1 * x2 + y1 * y2) / (math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2))
    angle = math.acos(angle) * 180 / math.pi
    if angle < 0:
        angle += 90
    else:
        angle = 90 - angle
    return angle

def pitch(x1, y1, x2, y2):
    x1, y1 = y1, x1
    x1 = -x1
    if x1 * x2 + y1 * y2 == 0:
        return 0
    angle = (x1 * x2 + y1 * y2) / (math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2 + 1))
    angle = math.acos(angle) * 180 / math.pi
    if angle < 0:
        angle += 90
    else:
        angle = 90 - angle
    return angle


fin = open('input.txt')
mineX, mineY = map(float, fin.readline().split())
directX, directY = map(float, fin.readline().split())
rollX, rollY = map(float, fin.readline().split())
enemyX, enemyY = map(float, fin.readline().split())
fin.close()
fout = open('output.txt', 'w')

side = side(directX, directY, enemyX - mineX, enemyY - mineY)
if not(-1 <= side <= 1):
    fout.write('0\n')
else:
    fout.write(str(side) + '\n')
fout.write(str(rotate(directX, directY, enemyX - mineX, enemyY - mineY)) + '\n')
fout.write(str(pitch(directX, directY, rollX, rollY)) + '\nBye')

fout.close()
