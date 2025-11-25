from sense_hat import SenseHat
import time

s = SenseHat()
s.low_light = True


green = (0, 255, 0)
yellow = (255, 180, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
pink = (255,105, 180)


def blank():
    G = green
    Y = yellow
    B = blue
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo



def sky():
    G = green
    Y = yellow
    B = blue
    O = nothing
    logo = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def a1():
    G = green
    Y = yellow
    B = blue
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, Y, O, O, O,
    O, O, O, Y, Y, O, O, O,
    O, O, O, O, Y, O, O, O,
    O, O, O, O, Y, O, O, O,
    O, O, O, O, Y, O, O, O,
    O, O, O, O, Y, O, O, O,
    O, O, O, Y, Y, Y, O, O,
    ]
    return logo




def aX():
    G = green
    Y = yellow
    B = blue
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    B, O, O, O, O, O, B, O,
    O, B, O, O, O, B, O, O,
    O, O, B, O, B, O, O, O,
    O, O, O, B, O, O, O, O,
    O, O, B, O, B, O, O, O,
    O, B, O, O, O, B, O, O,
    B, O, O, O, O, O, B, O,
    ]
    return logo

def SUPER():
    R = red
    G = green
    Y = yellow
    B = blue
    O = nothing
    logo = [
    O, O, R, R, R, O, O, O,
    O, R, Y, R, Y, R, O, O,
    R, Y, R, Y, R, Y, R, O,
    O, R, Y, R, Y, R, O, O,
    O, O, R, Y, R, O, O, O,
    O, O, O, R, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo


#s.set_pixels(SUPER())
colors = [red,blue,yellow,green]
c = 0
while(True):
    
    for y in range(0,8):
        for i in range(0,8):
            s.set_pixel(y,i,colors[c % 4])
            time.sleep(0.1)
    time.sleep(1)
    c = c+1
