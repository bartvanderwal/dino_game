from processing import *

x = 0
speed = 1

def setup():
    size(800,500)

def draw():
    global x

    background(255)
    circle(x,250,50)

    x += speed

    request_input("Nieuwe snelheid: ")

def input_received(text_line):
    global speed
    try:
        speed = int(text_line)
    except ValueError:
        print("Ongeldige invoer: " + text_line)
        
run()
