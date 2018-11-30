import pyglet
import Segment as Seg

class Snake:
	''' Snake class represents the snake for the game. Contains essential information
		about the snake such as position information, name of player (useful for 
		multiplayer/saving names of highscorers)
		
		Attributes:
		type (1=player1, 2=player2)
		playerName
		positionX
		positionY
		length
		squaresoccupied
		score
		direction (1=up, -1=down, 2=right, -2=left)


		pyglet related:
		snakeSprite
		segments
		segBatch
	'''

	def __init__(self,name,x,y,direction,playerType):


		head = pyglet.image.load('head.png')
		head.width = 36
		head.height = 36
		head.anchor_x = 18
		head.anchor_y = 18

		self.playerType = playerType
		self.playerName = name
		self.length = 7
		self.direction = direction
		self.positionX = x
		self.positionY = y
		self.squaresoccupied = list()
		self.score = 0
		self.moveQueue = list()

		self.segments = list()
		self.segBatch = pyglet.graphics.Batch()
		self.snakeSprite = pyglet.sprite.Sprite(head)

		for i in range(self.length):
			self.squaresoccupied.append(tuple((x,y+(i*self.direction))))
			self.segments.append(Seg.Segment(340+(x*40),60+(y*40)+(i*40*self.direction),self.direction,self.playerType))

		for element in self.segments:
			element.segmentSprite.batch = self.segBatch

	def setSquares(self):
		'''
		Inserts the current coordinates as a tuple to the front of the list so that
		the newest element is always the first in the list. Also, if the length of the
		squares occupied is greater than the supposed length of the snake, pop the last
		(oldest) element in the list
		'''
		self.squaresoccupied.insert(0,tuple((self.positionX,self.positionY)))

		if len(self.squaresoccupied) > self.length:
			self.squaresoccupied.pop()

	def setSegments(self):
		'''
		See the documentation for setSquares(). It works similarly, except handles the segments
		of the snake for drawing in pyglet. Also specifies the batches of the snake.
		'''
		self.segments.insert(0,Seg.Segment(340+(self.positionX*40),(60+(self.positionY*40)),self.direction,self.playerType))

		if len(self.segments) > self.length:
			self.segments.pop()

		for element in self.segments:
			element.segmentSprite.batch = self.segBatch

	def setDirection(self,direction):
		'''
		Set the direction that the snake is facing. 
		'''

		if self.direction != -direction:
			self.direction = direction
			if self.direction == 1:
				self.snakeSprite.rotation = 180
			elif self.direction == -1:
				self.snakeSprite.rotation = 0
			elif self.direction == 2:
				self.snakeSprite.rotation = 90
			elif self.direction == -2:
				self.snakeSprite.rotation = 270


	def eat(self):
		'''
		Increase the length of the snake by 1 and increase the score by 1
		'''
		self.length += 1
		self.score += 1
	
	def move(self):
		'''
		Depending on the current direction of the snake, the move function moves the
		snake 1 position in the required direction. Sets the squares occupied first,
		before moving the snake so that the head of the snake is not included in squares
		occupied (This is useful for checking if a snake collides with itself)
		'''
		if self.direction == 1:
			self.setSquares()
			self.positionY -= 1
		if self.direction == -1:
			self.setSquares()
			self.positionY += 1
		if self.direction == 2:
			self.setSquares()
			self.positionX += 1
		if self.direction == -2:
			self.setSquares()
			self.positionX -= 1

		#Mostly a debug function
		print(str(self.positionX) + " " + str(self.positionY))




		



