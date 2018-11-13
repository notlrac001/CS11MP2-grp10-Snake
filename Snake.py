class Snake:
	''' Snake class represents the snake for the game. Contains essential information
		about the snake such as position information, name of player (useful for 
		multiplayer/saving names of highscorers)
		
		Attributes: 
		playerName:str
		position:tuple
		length:int
		squaresoccupied:list of tuples
		score:int
		direction:int (1=up, -1=down, 2=right, -2=left)
	'''

	

	def __init__(self,name,x,y):
		self.playerName = name
		self.length = 10
		self.direction = 1
		self.positionX = x
		self.positionY = y
		self.squaresoccupied = list()
		self.score = int()

		for i in range(self.length):
			self.squaresoccupied.append(tuple((x,y+i)))

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

	def setDirection(self,direction):
		'''
		Set the direction that the snake is facing. 
		'''
		if self.direction != -direction:
			self.direction = direction

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


		



