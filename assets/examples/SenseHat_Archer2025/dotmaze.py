from sense_hat import SenseHat
import time
import math
import random as r

s = SenseHat()
green = (0, 255, 0)
yellow = (255, 180, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
pink = (255,105, 180)

ws = 20
def make_world1():

    global world
    world = [[1 for _ in range(ws)] for _ in range(ws)]  # fill with walls

    def carve_passages_from(cx, cy):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        r.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < ws-1 and 1 <= ny < ws-1:
                if world[ny][nx] == 1:
                    world[cy + dy//2][cx + dx//2] = 0  # remove wall between
                    world[ny][nx] = 0  # carve new cell
                    carve_passages_from(nx, ny)

    # Start carving from (1,1)
    world[1][1] = 0
    carve_passages_from(1, 1)

    # Optional: print the maze
    for row in world:
        print(row)


def make_world():
    global world
    # Step 1: Create a 20x20 grid filled with 0s
    world = [[r.randint(1, 3)   for wx in range(ws)] for wy in range(ws)]

    # Step 2: Add border walls
    for wy in range(ws):
        for wx in range(ws):
            if wx == 0 or wy == 0 or wx == ws - 1 or wy == ws - 1:
                world[wy][wx] = 1  # border wall
    
    world[1][1] = 0


    # Optional: Print the world for debugging
    for row in world:
        print(row)

        

def round_g(g):
    orientation = s.get_orientation_degrees()
    return round(float(orientation[g]))



def angle_difference(a, b):
    return (a - b + 180) % 360 - 180

def get_orientation_change():
    global yaw_c, pitch_c, roll_c
    orientation = s.get_orientation_degrees()
    yaw_c = angle_difference(orientation['yaw'], base_gyro[0])
    pitch_c = angle_difference(orientation['pitch'], base_gyro[1])
    roll_c = angle_difference(orientation['roll'], base_gyro[2])


def controls():
    global speed_x, speed_y, x, y, prev_x, prev_y
    
    prev_x = x
    prev_y = y
    get_orientation_change()
    speed_y = roll_c/80
    
    speed_x = pitch_c/80
   
    # print(speed_x, speed_y)
    
    x = x + speed_x
    y = y + speed_y
    #print(math.floor(x),math.floor(y))
    
def draw():
    global x, y, camx, camy

    s.clear()

    # Calculate camera top-left position (clamp so viewport stays in world)
    if x > 4 and x < ws - 4:
        camx = int(x) - 4
    elif x <= 4:
        camx = 0
    else:
        camx = ws - 8

    if y > 4 and y < ws - 4:
        camy = int(y) - 4
    elif y <= 4:
        camy = 0
    else:
        camy = ws - 8
   # print(camx,camy)
    # Draw the 8x8 viewport
    for wy in range(8):
        for wx in range(8):
            world_x = camx + wx
            world_y = camy + wy
            

            if world[world_x][world_y] == 1:
                s.set_pixel(wx, wy, red)
            
            
            
              

    player_x = int(x) - camx
    player_y = int(y) - camy
    s.set_pixel(player_x, player_y, blue)

    

def collisions():
    global x,y,itm
   
    
    if world[math.floor(x)][math.floor(y)] == 1:
        x = prev_x
        y = prev_y

s.clear()
orientation = s.get_orientation_degrees()


base_gyro = [round_g('yaw'), round_g('pitch'), round_g('roll')]

print(base_gyro)

world = []


prev_x = 0
prev_y = 0


yaw_c = 0
pitch_c = 0 
roll_c = 0

speed_x = 0
speed_y = 0

x = 1
y = 1
camy = 0
camx = 0


make_world()
#print(world)
while(True):
    
    controls()
    collisions()
    draw()
    #print(round(x),round(y))
    