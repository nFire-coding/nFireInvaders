import turtle
import random
import time

win = turtle.Screen()
win.title("nFire Invaders")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

punteggio = 0
powerups = []

def genera_powerup():
    powerup = turtle.Turtle()
    powerup.shape("square")
    powerup.color("blue")
    powerup.penup()
    powerup.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(100, 250)
    powerup.goto(x, y)
    return powerup

def muovi_powerup(powerup):
    y = powerup.ycor()
    y -= invader_speed + 10
    powerup.sety(y)

def muovi_aliena(aliena):
    x = aliena.xcor()
    x += aliena.direction * 5
    aliena.setx(x)

    # Cambia la direzione e abbassa la navicella quando tocca i bordi
    if x > 290 or x < -290:
        aliena.direction *= -1
        y = aliena.ycor()
        y -= 40
        aliena.sety(y)

def aggiorna_punteggio():
    score_display.clear()
    score_display.write("PUNTEGGIO : {}".format(punteggio), align="left", font=("Courier", 12, "normal"))

def aggiorna_barra_vita(barra_vita, vita):
    barra_vita.clear()
    barra_vita.write("VITA : {}".format(vita), align="right", font=("Courier", 12, "normal"))

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-290, 260)
aggiorna_punteggio()

# Barra della vita della navicella aliena
barra_vita = turtle.Turtle()
barra_vita.speed(0)
barra_vita.color("white")
barra_vita.penup()
barra_vita.hideturtle()
barra_vita.goto(280, 260)
vita_aliena = 100
aggiorna_barra_vita(barra_vita, vita_aliena)

player = turtle.Turtle()
player.shape("turtle")
player.color("white")
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

player_speed = 30
bullet_speed = 3

def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -290:
        x = -290
    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x > 290:
        x = 290
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

win.listen()
win.onkey(move_left, "Left")
win.onkey(move_right, "Right")
win.onkey(fire_bullet, "space")

num_invaders = 7
invaders = []

for _ in range(num_invaders):
    invader = turtle.Turtle()
    invader.shape("circle")
    invader.color("red")
    invader.penup()
    invader.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(100, 250)
    invader.goto(x, y)
    invaders.append(invader)

aliena = turtle.Turtle()
aliena.shape("square")
aliena.color("green")
aliena.penup()
aliena.speed(0)
aliena.goto(0, 200)
aliena.direction = 1

invader_speed = 2
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.speed(10)
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)  # Rendi il proiettile della navicella aliena più sottile
bullet.hideturtle()
bullet_state = "ready"

def move_invaders():
    for invader in invaders:
        y = invader.ycor()
        y -= invader_speed
        invader.sety(y)

        if player.distance(invader) < 20:
            player.hideturtle()
            invader.hideturtle()
            print("GAME OVER!!!")
            win.bye()

        if y < -290:
            player.hideturtle()
            invader.hideturtle()
            print("GAME OVER!!!")
            win.bye()
    
    muovi_aliena(aliena)

    for powerup in powerups:
        muovi_powerup(powerup)

    win.update()
    win.ontimer(move_invaders, 100)

move_invaders()

start_time = time.time()
while True:
    if random.randint(1, 10000) == 1:
        powerup = genera_powerup()
        powerups.append(powerup)

    for powerup in powerups:
        if player.distance(powerup) < 20:
            powerup.hideturtle()
            powerups.remove(powerup)
            player_speed = 60
            invader_speed = 1

    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

        for invader in invaders:
            if bullet.distance(invader) < 15:
                bullet.hideturtle()
                bullet_state = "ready"
                #x = random.randint(-290, 290)
                #y = random.randint(100, 250)
                invader.hideturtle()
                punteggio += 10
                aggiorna_punteggio()

        if y > 290:
            bullet.hideturtle()
            bullet_state = "ready"

    if time.time() - start_time > 1000000:
        if aliena.isvisible():
            muovi_aliena(aliena)

    # Verifica se il proiettile del giocatore colpisce la navicella aliena
    if bullet_state == "fire" and bullet.distance(aliena) < 15:
        bullet.hideturtle()
        bullet_state = "ready"
        vita_aliena -= 10
        aggiorna_barra_vita(barra_vita, vita_aliena)

        if vita_aliena <= 0:
            aliena.hideturtle()
            print("HAI VINTO!!!")
            win.bye()

    win.update()