import turtle as t

#setup
t.shape('turtle')
t.speed('slow')
t.bgcolor('Dodger blue')

def rectangle(width, height, color):
    t.pendown()
    t.pensize(1)
    t.color(color)
    t.begin_fill()
    for c in range(0,2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    t.penup()

while True:
    #feet
    t.goto(-100, -150)
    rectangle(50, 20, 'blue')
    t.goto(-30, -150)
    rectangle(50, 20, 'blue')

    #legs
    t.goto(-25, -50)
    rectangle(15, 100,'grey')
    t.goto(-55, -50)
    rectangle(10, 100,'grey')

    #body
    t.goto(-90, 100)
    rectangle(100, 150, 'red')

    #arms
    t.goto(-150, 70)
    rectangle(60, 15,'grey')
    t.goto(-150, 110)
    rectangle(15, 40,'grey')

    t.goto(10, 70)
    rectangle(60, 15,'grey')
    t.goto(55, 110)
    rectangle(15, 40,'grey')

    #neck
    t.goto(-50, 120)
    rectangle(15, 20, 'grey')

    #head
    t.goto(-85, 170)
    rectangle(80, 50, 'red')

    #eyes
    t.goto(-60, 160)
    rectangle(30, 10, 'white')
    t.goto(-55, 155)
    rectangle(5, 5, 'black')
    t.goto(-40, 155)
    rectangle(5, 5, 'black')

    #mouth
    t.goto(-65, 135)
    rectangle(40, 5, 'black')

    t.hideturtle()


