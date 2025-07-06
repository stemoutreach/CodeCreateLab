import turtle
import random
wn = turtle.Screen()
elsa = turtle.Turtle()

wn.bgcolor("blue")
elsa.color("white")

elsa.penup()
elsa.backward(600)
elsa.right(90)
elsa.forward(200)
elsa.left(90)
elsa.forward(350)
elsa.pendown()

for i in range(2):
  elsa.forward(100)
  elsa.right(60)
  elsa.forward(100)
  elsa.right(120)

elsa.penup()
elsa.forward(-350)
elsa.pendown()

for i in range(3):
  for i in range(2):
    elsa.forward(100)
    elsa.right(60)
    elsa.forward(100)
    elsa.right(120)
  elsa.right(120)

elsa.penup()
elsa.right(90)
elsa.forward(-400)
elsa.left(90)
elsa.pendown()

for i in range(5):
  for i in range(2):
    elsa.forward(100)
    elsa.right(60)
    elsa.forward(100)
    elsa.right(120)
  elsa.right(72)

elsa.penup()
elsa.forward(350)
elsa.pendown()

for i in range(10):
  for i in range(2):
    elsa.forward(100)
    elsa.right(60)
    elsa.forward(100)
    elsa.right(120)
  elsa.right(36)

elsa.penup()
elsa.forward(350)
elsa.pendown()

for i in range(20):
  for i in range(2):
    elsa.forward(100)
    elsa.right(60)
    elsa.forward(100)
    elsa.right(120)
  elsa.right(18)

elsa.penup()
elsa.forward(350)
elsa.pendown()

for i in range(40):
  for i in range(2):
    elsa.forward(100)
    elsa.right(60)
    elsa.forward(100)
    elsa.right(120)
  elsa.right(9)


elsa.penup()
elsa.right(90)
elsa.forward(350)
elsa.pendown()

for i in range(120):
  for i in range(2):
    elsa.forward(100)
    elsa.right(60)
    elsa.forward(100)
    elsa.right(120)
  elsa.right(3)


elsa.penup()
elsa.right(90)
elsa.forward(445)
elsa.left(45)
elsa.pendown()

def branch():
  for i in range(3):
    for i in range(3):
      elsa.forward(30)
      elsa.backward(30)
      elsa.right(45)
    elsa.left(90)
    elsa.backward(30)
    elsa.left(45)
  elsa.right(90)
  elsa.forward(90)

for i in range(8):
  branch()
  elsa.left(45)


wn.exitonclick()
