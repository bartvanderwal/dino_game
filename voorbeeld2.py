from processing import *

xPos = 0

def setup(): 
  size(800, 600)


def draw(): 
  background(255)
  global xPos  
  xPos = xPos + 1
  circle(xPos, 550, 100)
    
run()