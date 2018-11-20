import pyglet

class Segment:
	'''
	represents the segments of the Snake object (other than the head)

	attributes:
	segmentSprite
	direction
	'''

	def __init__(self,x,y,direction):

		red = pyglet.image.load('square.png')
		red.width = 40
		red.height = 40
		red.anchor_x = 20
		red.anchor_y = 20

		self.segmentSprite = pyglet.sprite.Sprite(red)
		self.segmentSprite.x = x
		self.segmentSprite.y = y
		self.direction = direction