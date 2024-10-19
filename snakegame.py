from PIL import Image
import turtle
import time
import random

# Open the snake.gif image
snake_img = Image.open("medusa.gif")

# Rotate the image by 90 degrees
snake_rotated = snake_img.rotate(-180, expand=True)

# Save the rotated image
snake_rotated.save("snake_resized.gif")

# Function to convert mm to pixels
def mm_to_pixels(mm, dpi=96):
    return int((mm / 25.4) * dpi)

# Set the desired size in millimeters
size_in_mm = 9  # 2x2 mm

# Convert the size to pixels (assuming 96 DPI screen resolution)
size_in_pixels = mm_to_pixels(size_in_mm)

# Load and resize the snake.gif
snake_img = Image.open("snake_resized.gif")
snake_resized = snake_img.resize((size_in_pixels, size_in_pixels), Image.ANTIALIAS)
snake_resized.save("snake_resized.gif")

# Load and resize the mouse.gif
mouse_img = Image.open("mouse.gif")
mouse_resized = mouse_img.resize((size_in_pixels, size_in_pixels), Image.ANTIALIAS)
mouse_resized.save("mouse_resized.gif")

print("Images resized and saved as snake_resized.gif and mouse_resized.gif.")


delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Register the snake and mouse images
wn.register_shape("snake_resized.gif")
wn.register_shape("mouse_resized.gif")

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("snake_resized.gif")  # Use the rotated snake image
head.penup()
head.goto(0, 0)
head.direction = "up"  # Set initial direction to up
head.shapesize(stretch_wid=0.05, stretch_len=0.05)  # Scale to 5x5 mm approximately

# Snake food (mouse)
food = turtle.Turtle()
food.speed(0)
food.shape("mouse_resized.gif")  # Use the mouse image
food.penup()
food.goto(0, 100)
food.shapesize(stretch_wid=0.05, stretch_len=0.05)  # Scale to 5x5 mm approximately

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions to change the snake's direction and rotate accordingly
def go_up():
    if head.direction != "down":
        head.direction = "up"
        head.setheading(0)  # Set the snake to face up

def go_down():
    if head.direction != "up":
        head.direction = "down"
        head.setheading(180)  # Set the snake to face down

def go_left():
    if head.direction != "right":
        head.direction = "left"
        head.setheading(-90)  # Set the snake to face left

def go_right():
    if head.direction != "left":
        head.direction = "right"
        head.setheading(90)  # Set the snake to face right

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings for arrow keys
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        new_segment.color("black")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()
