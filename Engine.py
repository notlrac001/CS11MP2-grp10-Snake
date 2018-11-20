import Snake as S
import os
import time
import random

#size of grid nxn
n = 16

grid = list()

#For now food is a tuple. Could make a spearate object for a separate sprite if there is time.
food = tuple()

def checkCollision(snakeObject,otherSnakeObject = None):
	'''
	Checks the collisions of the snake with the bounds, or itself
	'''
	if snakeObject.positionX < 0:
		print("collision")
		return True
	if snakeObject.positionY < 0:
		print("collision")
		return True
	if snakeObject.positionX >= n:
		print("collision")
		return True
	if snakeObject.positionY >= n:
		print("collision")
		return True
	if (snakeObject.positionX,snakeObject.positionY) in snakeObject.squaresoccupied:
		print("collision with self")
		return True
	if otherSnakeObject != None:
		if (snakeObject.positionX,snakeObject.positionY) in otherSnakeObject.squaresoccupied:
			print(otherSnakeObject.playerName + " wins")
			return True
	else:
		return False

def checkFood(snakeObject):
	'''
	Checks if the head of a snake passes over food, and if it does, calls the 
	eat functino and creates a new random location for the food. Note, still need
	to fix this so it doesn't make food over an occupied square.
	'''
	if snakeObject.positionX == food[0] and snakeObject.positionY == food[1]:
		#return True
		snakeObject.eat()
		makeFood(snakeObject)

def makeFood(snakeObject):
	'''
	Sets the coordinates of food.
	'''
	global food
	temp = tuple((random.randint(0,n-1),random.randint(0,n-1)))

	while temp in snakeObject.squaresoccupied:
		temp = tuple((random.randint(0,n-1),random.randint(0,n-1)))

	food = temp


def translatePositionX(x):
	'''
	Translates the x coordinate to match the coordinate system of Pyglet.
	'''
	return 340+(x*40)

def translatePositionY(y):
	'''
	Translates the y coordinate to match the coordinate system of Pyglet.
	'''
	return 60+(y*40)

	



