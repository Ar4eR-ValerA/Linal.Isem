def add(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return -1
    C = []
    for i in range(len(A)):
        t = []
        for j in range(len(A[0])):
            t.append(A[i][j] + B[i][j])
        C.append(t)
    return C

def multiConst(A, a):
    C = []
    for i in range(len(A)):
        t = []
        for j in range(len(A[0])):
            t.append(A[i][j] * a)
        C.append(t)
    return C

def multi(A, B):
    if len(A[0]) != len(B):
        return -1
    C = []
    for i in range(len(A)):
        t = []
        for j in range(len(B[0])):
            x = 0
            for k in range(len(A[0])):
                x = x + A[i][k] * B[k][j]
            t.append(x)
        C.append(t)
    return C

def tran(A):
    C = []
    for i in range(len(A[0])):
        t = []
        for j in range(len(A)):
            t.append(A[j][i])
        C.append(t)
    return C

def read(M, nM, mM):
    input = list(map(float, fin.readline().split()))
    for i in range(nM):
        buffer = []
        for j in range(mM):
            buffer.append(input[i * mM + j])
        M.append(buffer)

def func(a, b, A, B, C, D, F):
    x = tran(B)
    x = multiConst(x, b)
    y = multiConst(A, a)
    if add(x, y) == -1:
        return -1
    x = add(x, y)
    x = tran(x)
    if multi(C, x) == -1:
        return -1
    x = multi(C, x)
    if multi(x, D) == -1:
        return -1
    x = multi(x, D)
    F = multiConst(F, -1)
    if add(x, F) == 0:
        return 0
    x = add(x, F)
    return x


fin = open('input.txt')
a, b = map(float, fin.readline().split())

nA, mA = map(int, fin.readline().split())
A = []
read(A, nA, mA)

nB, mB = map(int, fin.readline().split())
B = []
read(B, nB, mB)

nC, mC = map(int, fin.readline().split())
C = []
read(C, nC, mC)

nD, mD = map(int, fin.readline().split())
D = []
read(D, nD, mD)

nF, mF = map(int, fin.readline().split())
F = []
read(F, nF, mF)
fin.close()

answer = func(a, b, A, B, C, D, F)

fout = open('output.txt', 'w')
if answer == -1:
    fout.write('0\n')
else:
    fout.write('1\n')
    fout.write(str(len(answer)) + ' ' + str(len(answer[0])) + '\n')
    for i in range(len(answer)):
        for j in range(len(answer[0])):
            fout.write(str(answer[i][j]) + ' ')
        fout.write('\n')
fout.close()
