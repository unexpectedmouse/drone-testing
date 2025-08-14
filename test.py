x = 0
y = 0.5
flip_x = -1
flip_y = 1

for i in range(6):
    print(x * flip_x, ';', y * flip_y)
    x = y
    y = 0
    print(x * flip_x, ';', y * flip_y)
    y = x + 0.5
    x = 0
