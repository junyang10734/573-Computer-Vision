list = [[1, 2, 3, 4], [2, 2, 2, 2], [3, 5, 6, 7]]
gl = []
g_c = 0
g_t = 0
g_mean = 0
xn = len(list)
yn = len(list[0])
for x1 in range(xn):
    for y1 in range(yn):
        g_t = g_t + list[x1][y1]
        g_c = g_c + 1
g_mean = g_t / g_c
for x in range(xn):
    for y in range(yn):
        gl.append(list[x][y] - g_mean)

print(g_mean)
print(gl)

fl = []
f_c = 0
f_t = 0
f_mean = 0
for x in range(xn):
    f_t += sum(list[x])
    f_c += yn
f_mean = f_t/f_c
print(list)

for x in range(xn):
    for y in range(yn):
        fl.append(list[x][y] - f_mean)

print(f_mean)
print(fl)
