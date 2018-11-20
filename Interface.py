import pyglet
from pyglet.window import key
import Snake as S
import Engine as E

window = pyglet.window.Window(1280, 720, resizable=False)

gridSprite = pyglet.sprite.Sprite(pyglet.image.load('grid.png'))
gridSprite.y = 40
gridSprite.x = 320

food = pyglet.image.load('food.png')
food.width = 40
food.height = 40
food.anchor_x = 20
food.anchor_y = 20
foodSprite = pyglet.sprite.Sprite(food)

''' Start of 1 player mode code '''
def oneplayermode():
	
	#Creates a new player1. Currently the name is hardcoded but this could
	#be altered later i.e. make player select their name. This could also be
	#used when saving high scores and names.
	player1 = S.Snake("Carlton",5,6,1)

	#Creates initial food.
	E.makeFood(player1)

	@window.event
	def on_key_press(symbol, modifiers):

		#Move queue variable of the player is used to regulate what happens
		#if multiple keys are pressed before a redraw. Keeps last 3 presses
		#and does them in the consecutive calls of updatePos

		if len(player1.moveQueue) <= 3:
			if symbol == key.RIGHT:
				player1.moveQueue.insert(0,2)
			elif symbol == key.LEFT:
				player1.moveQueue.insert(0,-2)
			elif symbol == key.UP:
				player1.moveQueue.insert(0,-1)
			elif symbol == key.DOWN:
				player1.moveQueue.insert(0,1)

		#FLIPPED DUE TO PYGLET HAVING AN UPSIDE DOWN COORDINATE SYSTEM

	def updatePos(dt):
		if len(player1.moveQueue) > 0:
			player1.setDirection(player1.moveQueue.pop())

		player1.move()
		E.checkCollision(player1)
		E.checkFood(player1)
		player1.snakeSprite.x = E.translatePositionX(player1.positionX)
		player1.snakeSprite.y = E.translatePositionY(player1.positionY)
		player1.setSegments()

	@window.event
	def on_draw():
		window.clear()
		gridSprite.draw()
		player1.segBatch.draw()
		player1.snakeSprite.draw()
		foodSprite.x = E.translatePositionX(E.food[0])
		foodSprite.y = E.translatePositionY(E.food[1])
		foodSprite.draw()

	pyglet.clock.schedule_interval(updatePos, 1/10)
''' End of 1 player mode code'''


''' Start of 2 player mode code '''
def twoplayermode():
	
	#Creates 2 players.
	player1 = S.Snake("Player 1",5,6,1)
	player2 = S.Snake("Player 2",1,4,2)

	#Creates initial food.
	E.makeFood(player1)


	@window.event
	def on_key_press(symbol, modifiers):


		#Move queue variable of the player is used to regulate what happens
		#if multiple keys are pressed before a redraw. Keeps last 3 presses
		#and does them in the consecutive calls of updatePos

		if len(player1.moveQueue) <= 3:
			if symbol == key.RIGHT:
				player1.moveQueue.insert(0,2)
			elif symbol == key.LEFT:
				player1.moveQueue.insert(0,-2)
			elif symbol == key.UP:
				player1.moveQueue.insert(0,-1)
			elif symbol == key.DOWN:
				player1.moveQueue.insert(0,1)

		if len(player2.moveQueue) <= 3:
			if symbol == key.D:
				player2.moveQueue.insert(0,2)
			elif symbol == key.A:
				player2.moveQueue.insert(0,-2)
			elif symbol == key.W:
				player2.moveQueue.insert(0,-1)
			elif symbol == key.S:
				player2.moveQueue.insert(0,1)

		#FLIPPED DUE TO PYGLET HAVING AN UPSIDE DOWN COORDINATE SYSTEM

	def updatePos(dt):
		if len(player1.moveQueue) > 0:
			player1.setDirection(player1.moveQueue.pop())

		player1.move()
		E.checkCollision(player1,player2)
		E.checkFood(player1)
		player1.snakeSprite.x = E.translatePositionX(player1.positionX)
		player1.snakeSprite.y = E.translatePositionY(player1.positionY)
		player1.setSegments()

		if len(player2.moveQueue) > 0:
			player2.setDirection(player2.moveQueue.pop())

		player2.move()
		E.checkCollision(player2,player1)
		E.checkFood(player2)
		player2.snakeSprite.x = E.translatePositionX(player2.positionX)
		player2.snakeSprite.y = E.translatePositionY(player2.positionY)
		player2.setSegments()

	@window.event
	def on_draw():
		window.clear()
		gridSprite.draw()
		player1.segBatch.draw()
		player1.snakeSprite.draw()
		player2.segBatch.draw()
		player2.snakeSprite.draw()


		foodSprite.x = E.translatePositionX(E.food[0])
		foodSprite.y = E.translatePositionY(E.food[1])
		foodSprite.draw()

	pyglet.clock.schedule_interval(updatePos, 1/10)

''' End of 2 player mode code'''

#Just call the method to run each mode. Right now it's stuck in 2 player mode
#but you can easily change this.
twoplayermode()
pyglet.app.run()