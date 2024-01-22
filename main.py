import cv2 as cv
import mediapipe as mp
import turtle

# window creation
sc = turtle.Screen()
sc.title("Ping Pong game")
sc.bgcolor("grey")
sc.setup(width=1000, height=600)

# pad creation
Pad = turtle.Turtle()
Pad.speed(0)
Pad.shape("square")
Pad.color("blue")
Pad.shapesize(stretch_wid=2, stretch_len=6)
Pad.penup()
Pad.goto(0, -280)

# ball creation
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("green")
ball.penup()
ball.goto(0, 300)
ball.dx = 10
ball.dy = -10

# for displaying score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("score : 0", align="center", font=("Courier", 24, "normal"))

# initial score is 0
player = 0

video = cv.VideoCapture(0)
video.set(3, 1000)
video.set(4, 600)

# hand tracking solution
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)

while True:

    success, frame = video.read()
    frame = cv.flip(frame, 1)
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        move = int(results.multi_hand_landmarks[0].landmark[8].x * 1000)
        Pad.setx(move - 500)
    cv.imshow("video", frame)
    if cv.waitKey(1) != -1:
        break

    # moving ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # if ball hits top of window then change direction
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    # if ball hits right wall of window then change direction
    if ball.xcor() > 490:
        ball.setx(490)
        ball.dx *= -1

    # if ball hits left wall of window then change direction
    if ball.xcor() < -490:
        ball.setx(-495)
        ball.dx *= -1

    # if ball crosses the pad indication player is out
    if ball.ycor() < -280:
        sketch.goto(0, 100)
        sketch.write("    GAME OVER \n your score is : {}".format(player), align="center",
                     font=("Courier", 24, "normal"))
        sc.mainloop()
        break

    # maintaining the pad not moving out of  the right and left walls
    x_pad, y_pad = Pad.xcor(), Pad.ycor()
    if x_pad > 440:
        Pad.setx(440)
    if x_pad < -440:
        Pad.setx(-440)

    # checking  whether the ball is aligning in pads length range and hitting the pad
    # if this happens score is increased and ball changes its direction.
    x_ball, y_ball = ball.xcor(), ball.ycor()
    if x_pad + 60 >= x_ball >= x_pad - 60 and y_ball <= -252:
        player += 1
        sketch.clear()
        sketch.write("score : {} ".format(player), align="center", font=("Courier", 24, "normal"))
        ball.sety(-252)
        ball.dy *= -1
        ## sjdhbf sd bfis difus
