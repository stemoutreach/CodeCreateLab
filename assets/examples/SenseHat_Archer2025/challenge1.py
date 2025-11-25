import turtle
#import random
wn = turtle.Screen()


t = turtle.Turtle()
t.speed(0)
t.ht()
wn.tracer(0)

wn.bgcolor("blue")
t.color("white")

def shape(h,x,y):
    t.penup()
    t.goto(x,y)
    t.pendown()
    
    
    for i in range(h):
      for i in range(2):
        t.forward(100)
        t.right(60)
        t.forward(100)
        t.right(120)
        #wn.update()
      t.right(360/h)



shape(20,0,0)


#shape(1,200,-200)
#shape(3,-200,-200)
#shape(5,-200,200)
#shape(7,200,200)

wn.update()

wn.exitonclick()