import pyglet

class Segment:
	'''
	represents the segments of the Snake object (other than the head)

	attributes:
	segmentSprite
	direction
	'''

	def __init__(self,x,y,direction):

		seg = pyglet.image.load('square.png')
		seg.width = 40
		seg.height = 40
		seg.anchor_x = 20
		seg.anchor_y = 20

		self.segmentSprite = pyglet.sprite.Sprite(seg)
		self.segmentSprite.x = x
		self.segmentSprite.y = y
		self.direction = direction