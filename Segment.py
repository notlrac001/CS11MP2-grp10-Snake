import pyglet

class Segment:
	'''
	represents the segments of the Snake object (other than the head)

	attributes:
	segmentSprite
	direction
	'''

	#note: direction not yet used but could be used if we decide to draw the snake nicer
	def __init__(self,x,y,direction,playerType):

		if playerType == 1:
			seg = pyglet.image.load('segmentp1.png')
		elif playerType == 2:
			seg = pyglet.image.load('segmentp2.png')

		seg.width = 40
		seg.height = 40
		seg.anchor_x = 20
		seg.anchor_y = 20

		self.segmentSprite = pyglet.sprite.Sprite(seg)
		self.segmentSprite.x = x
		self.segmentSprite.y = y
		self.direction = direction