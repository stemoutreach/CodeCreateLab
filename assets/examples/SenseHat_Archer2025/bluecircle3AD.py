import turtle as t
t.speed(100)
t.color("blue")
turn = 10
num = 360/turn
for i in range(0,int(num)):
    t.circle(100)
    t.left(turn)
