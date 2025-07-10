# Import the turtle libraries
import turtle

# Create a window for turtle to draw in
wn = turtle.Screen()

# Create a turtle named 't'
t = turtle.Turtle()

# Move the turtle to the center of the screen without drawing
t.penup()        # Lift the pen so it doesn't draw while moving
t.goto(0, 0)     # Move turtle to center position (0, 0)
t.pendown()      # Put the pen down to start drawing

# Set background color to blue and turtle's drawing color to white
wn.bgcolor("blue")
t.color("white")

# This function draws one parallelogram shape
def DrawParallelogram():
    for i in range(2):           # Do this loop twice
        t.forward(100)           # Move forward 100 steps
        t.right(60)              # Turn right 60 degrees
        t.forward(100)           # Move forward again
        t.right(120)             # Turn right 120 degrees to complete the shape

# This function draws multiple parallelograms in a circular pattern
def DrawPattern(iRange):
    if iRange > 1 and iRange < 181:            # Only do pattern if number is between 2 and 180
        for i in range(iRange):                # Repeat drawing for the number entered
            DrawParallelogram()                # Draw one parallelogram
            t.right(360 / iRange)              # Turn a little before drawing the next one
    else:
        DrawParallelogram()                    # If number is not in range, draw just one shape

# Repeat the drawing process until the user wants to stop
while True:
    print("Number of parallelograms needs to be between 1 and 180")
    numberOfParallelogram = int(input("Enter number of parallelograms to draw: "))

    # Call the pattern drawing function
    DrawPattern(numberOfParallelogram)

    # Ask the user if they want to draw again
    while True:
        response = input("Draw another shape? (yes/no): ").strip().lower()

        if response == "yes":
            print("Drawing another shape...")
            t.clear()         # Clear the screen for a new drawing
            break             # Break out of this loop to ask for a new number

        elif response == "no":
            print("Exiting the drawing loop.")
            break             # Exit inner loop and then exit outer loop

        else:
            print("Please answer with 'yes' or 'no'.")  # Ask again if answer is not valid

    if response == "no":
        break     # Exit the outer loop and end the program

# Wait for a click on the window to close it
print("Click the diagram to exit")
wn.exitonclick()
