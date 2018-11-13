import Snake as S
import os
import time
import random

#size of grid nxn
n = 13

grid = list()
food = tuple()

for i in range(n):
	grid.append(list())
	for j in range(n):
		grid[i].append(".")

def checkCollision(snakeObject,otherSnakeObject = None):
	'''
	Checks the collisions of the snake with the bounds, or itself
	'''
	if snakeObject.positionX < 0:
		quit()
		return True
	if snakeObject.positionY < 0:
		quit()
		return True
	if snakeObject.positionX >= n:
		quit()
		return True
	if snakeObject.positionY >= n:
		quit()
		return True
	if (snakeObject.positionX,snakeObject.positionY) in snakeObject.squaresoccupied:
		quit()
		return True
	if otherSnakeObject != None:
		if (snakeObject.positionX,snakeObject.positionY) in otherSnakeObject.squaresoccupied:
			print(otherSnakeObject.playerName + " wins")
			quit()
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
		snakeObject.eat()
		makeFood(random.randint(0,n-1),random.randint(0,n-1))

def makeFood(x,y):
	'''
	Sets the coordinates of food.
	'''
	global food
	food = (x,y)

	



