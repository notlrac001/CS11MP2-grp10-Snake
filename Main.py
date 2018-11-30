import pyglet
from pyglet.window import key
import Snake as S
import Engine as E
import time

width, height = 1280, 720
window = pyglet.window.Window(width, height, resizable=False)

name = 'Arial Black'
color1 = (130,255,220,255) #Light blue
color2 = (0,242,255,255) # blue of player 1
color3 = (252,216,13,255) #orange of player 2

button = 1

hoverwidth = 344
hoverheight = 79

gridSprite = pyglet.sprite.Sprite(pyglet.image.load('grid.png'))
gridSprite.y = 40
gridSprite.x = 320

food = pyglet.image.load('food.png')
food.width = 40
food.height = 40
food.anchor_x = 20
food.anchor_y = 20
foodSprite = pyglet.sprite.Sprite(food)

# instead of using a label class everytime,
# a function for labels is made to define some attributes
# that will be used for all labels
def label(l,s,x,y,c=None):

    # c is optional argument, can use it to change font color, but there is a default color.

    if c != None:
        return pyglet.text.Label(l, font_name=name, font_size=s, color=c, anchor_x='center', anchor_y='center', x=x, y=y)
    else:
        return pyglet.text.Label(l, font_name=name, font_size=s, color=(color1), anchor_x='center', anchor_y='center', x=x, y=y)

# a function for hovers is made
# to set some attributes and properties
# that will be used by all hovers
def hover(x,y):
    a = pyglet.sprite.Sprite(pyglet.image.load('hover.png'), x=x, y=y)
    a.scale = 0.5
    a.opacity = 75
    return a

centerx = width//2
leftx = width//4
rightx = width*3//4
leftgridx = gridSprite.x//2
rightgridx = (gridSprite.width + 320) + ((width-(gridSprite.width + gridSprite.x))//2)

''' Start of 1 Player Mode '''
def oneplayermode():
    '''
        Insert block comment here describing this function
    '''
    
    global a
    a = 7 #initial inverse acceleration (1/7 seconds)
    
    player1 = S.Snake("Player 1",1,8,1,1)
    title = label('Player 1 Score:',20,leftgridx,height*0.8,color2)
    score = label('0',30,leftgridx,height*0.7,color2)

    #helps the player understand controls.
    controlLabel = label('Player 1 controls',15,leftgridx,height*0.3,color2)
    controlW = label('W',20,leftgridx,height*0.2,color2)
    controlS = label('S',20,leftgridx,height*0.15,color2)
    controlA = label('A',20,leftgridx - 35,height*0.15,color2)
    controlD = label('D',20,leftgridx + 35,height*0.15,color2)
    
    E.makeFood(player1)
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Insert block comment here describing this function
        '''

	#Move queue variable of the player is used to regulate what happens
	#if multiple keys are pressed before a redraw. Keeps last 3 presses
	#and does them in the consecutive calls of updatePos

        if len(player1.moveQueue) <= 3:
            if symbol == key.D:
                player1.moveQueue.insert(0,2)
            elif symbol == key.A:
                player1.moveQueue.insert(0,-2)
            elif symbol == key.W:
                player1.moveQueue.insert(0,-1)
            elif symbol == key.S:
                player1.moveQueue.insert(0,1)

		#FLIPPED DUE TO PYGLET HAVING AN UPSIDE DOWN COORDINATE SYSTEM

    def opener(dt):
        '''
        Insert block comment here describing this function
        '''

        todo = 'nothing'
        pyglet.clock.unschedule(opener)
        
    def updatePos(dt):
        '''
        Insert block comment here describing this function
        '''
        global scr1, a
        if len(player1.moveQueue) > 0:
            player1.setDirection(player1.moveQueue.pop())

        player1.move()
        player1.setSegments()
        player1.snakeSprite.x = E.translatePositionX(player1.positionX)
        player1.snakeSprite.y = E.translatePositionY(player1.positionY)
        E.checkFood(player1)
        score.text = str(player1.score)
        if E.checkCollision(player1):
            p1gameover(player1.score)

    @window.event
    def on_draw():
        '''
        Insert block comment here describing this function
        '''

        window.clear()
        gridSprite.draw()
        player1.segBatch.draw()
        player1.snakeSprite.draw()
        
        foodSprite.x = E.translatePositionX(E.food[0])
        foodSprite.y = E.translatePositionY(E.food[1])
        foodSprite.draw()
        
        title.draw()
        score.draw()
        controlLabel.draw()
        controlW.draw()
        controlS.draw()
        controlA.draw()
        controlD.draw()

    def acceleration(dt):
        '''
        Insert block comment here describing this function
        '''

        global a
        a += 0.5
        print('a=1/',a)
        
    pyglet.clock.schedule_interval(updatePos, 1/a)
    pyglet.clock.schedule_interval(acceleration,5)
    pyglet.clock.schedule_once(opener,1/60)
    pyglet.app.run()

def twoplayermode():
    '''
        Insert block comment here describing this function
    '''
    
    global a
    a = 7
    #Creates 2 players.
    player1 = S.Snake("Player 1",1,8,1,1)
    player2 = S.Snake("Player 2",14,7,-1,2)
    title1 = label('Player 1 Score:',20,leftgridx,height*0.8,color2)
    title2 = label('Player 2 Score:',20,rightgridx,height*0.8,color3)
    score1 = label('0',30,leftgridx,height*0.7,color2)
    score2 = label('0',30,rightgridx,height*0.7,color3)

    #helps player 1 understand controls.
    controlLabel1 = label('Player 1 controls',15,leftgridx,height*0.3,color2)
    controlW = label('W',20,leftgridx,height*0.2,color2)
    controlS = label('S',20,leftgridx,height*0.15,color2)
    controlA = label('A',20,leftgridx - 35,height*0.15,color2)
    controlD = label('D',20,leftgridx + 35,height*0.15,color2)

    #helps player 2 understand controls.
    #helps the player understand controls.
    controlLabel2 = label('Player 2 controls',15,rightgridx,height*0.3,color3)
    controlUp = label('↑',20,rightgridx,height*0.2,color3)
    controlDown = label('↓',20,rightgridx,height*0.15,color3)
    controlLeft = label('←',20,rightgridx - 35,height*0.15,color3)
    controlRight = label('→',20,rightgridx + 35,height*0.15,color3)

    #Creates initial food.
    E.makeFood(player1,player2)

    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Insert block comment here describing this function
        '''

        #Move queue variable of the player is used to regulate what happens
        #if multiple keys are pressed before a redraw. Keeps last 3 presses
        #and does them in the consecutive calls of updatePos

        if len(player1.moveQueue) <= 3:
            if symbol == key.D:
                player1.moveQueue.insert(0,2)
            elif symbol == key.A:
                player1.moveQueue.insert(0,-2)
            elif symbol == key.W:
                player1.moveQueue.insert(0,-1)
            elif symbol == key.S:
                player1.moveQueue.insert(0,1)

        if len(player2.moveQueue) <= 3:
            if symbol == key.RIGHT:
                player2.moveQueue.insert(0,2)
            elif symbol == key.LEFT:
                player2.moveQueue.insert(0,-2)
            elif symbol == key.UP:
                player2.moveQueue.insert(0,-1)
            elif symbol == key.DOWN:
                player2.moveQueue.insert(0,1)

        #FLIPPED DUE TO PYGLET HAVING AN UPSIDE DOWN COORDINATE SYSTEM

    def opener(dt):
        '''
        Insert block comment here describing this function
        '''
        todo = 'nothing'

    def updatePos(dt):
        '''
        Insert block comment here describing this function
        '''

        done = False
        win = 0


        if len(player1.moveQueue) > 0:
            player1.setDirection(player1.moveQueue.pop())

        player1.move()
        E.checkCollision(player1,player2)
        E.checkFood(player1,player2)
        player1.setSegments()
        player1.snakeSprite.x = E.translatePositionX(player1.positionX)
        player1.snakeSprite.y = E.translatePositionY(player1.positionY)
        score1.text = str(player1.score)


        if len(player2.moveQueue) > 0:
            player2.setDirection(player2.moveQueue.pop())

        player2.move()
        E.checkCollision(player2,player1)
        E.checkFood(player2,player1)
        player2.setSegments()
        player2.snakeSprite.x = E.translatePositionX(player2.positionX)
        player2.snakeSprite.y = E.translatePositionY(player2.positionY)
        score2.text = str(player2.score)

        # Let all moving code happen first before checking collisions to prevent
        # unwanted effects

        if E.checkCollision(player1,player2):
            win += 2
            done = True

        if E.checkCollision(player2,player1):
            win += 1
            done = True
            
        if done:

            if win == 1:
                if player2.score > 5:
                    player2.score = player2.score - 5
            if win == 2:
                if player1.score > 5:
                    player1.score = player1.score - 5
            p2gameover(win,player1.score,player2.score)

    @window.event
    def on_draw():
        '''
        Insert block comment here describing this function
        '''

        window.clear()
        gridSprite.draw()
        player1.segBatch.draw()
        player1.snakeSprite.draw()
        player2.segBatch.draw()
        player2.snakeSprite.draw()

        foodSprite.x = E.translatePositionX(E.food[0])
        foodSprite.y = E.translatePositionY(E.food[1])
        foodSprite.draw()
        
        title1.draw()
        title2.draw()
        score1.draw()
        score2.draw()

        controlLabel1.draw()
        controlW.draw()
        controlS.draw()
        controlA.draw()
        controlD.draw()

        controlLabel2.draw()
        controlUp.draw()
        controlDown.draw()
        controlLeft.draw()
        controlRight.draw()

    def acceleration(dt):
        '''
        Insert block comment here describing this function
        '''

        global a
        a += 0.5
        print('a=1/',a)
        
    pyglet.clock.schedule_interval(updatePos, 1/a)
    pyglet.clock.schedule_interval(acceleration,5)
    pyglet.clock.schedule_once(opener,1/60)
    pyglet.app.run()
    
def p1gameover(scr):
    '''
        Insert block comment here describing this function
    '''
    
    title = label('GAME OVER',60,width//2,height*0.8)
    score = label('Score:  '+str(scr),50,centerx,height*0.5,color2)
    menu = label('Main Menu',30,leftx,height*0.3)
    bye = label('Quit',30,rightx,height*0.3)
    
    hover0 = hover((width//4)-(hoverwidth//2),(height*0.3)-(hoverheight//2))

    savetostats(scr)
    button = 1
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Insert block comment here describing this function
        '''
        global button
        pyglet.clock.set_fps_limit(60)
        if symbol == key.LEFT:
            if button == 2:
                button = 1
                hover0.x = (width//4) - (hoverwidth//2)
        elif symbol == key.RIGHT:
            if button == 1:
                button = 2
                hover0.x = (width*3//4) - (hoverwidth//2)
        elif symbol == key.ENTER:
            if button == 1:
                return mainmenu()
            elif button == 2:
                window.close()

    def opener(dt):
        '''
        Insert block comment here describing this function
        '''
        todo = 'nothing'

    @window.event
    def on_draw():
        '''
        Insert block comment here describing this function
        '''
        window.clear()
        title.draw()
        score.draw()
        menu.draw()
        bye.draw()
        hover0.draw()
            
    pyglet.clock.schedule_once(opener, 1)
    pyglet.app.run()
    
def p2gameover(win,scr1,scr2):
    '''
        Insert block comment here describing this function
    '''

    if win == 1:
        title = label('GAME OVER',45,width//2,height*0.8)
        head = label('PLAYER 1 WINS',60,width//2,height*0.65,color2)
    elif win == 2:
        title = label('GAME OVER',45,width//2,height*0.8)
        head = label('PLAYER 2 WINS',60,width//2,height*0.65,color3)
    else:
        title = label('GAME OVER',45,width//2,height*0.8)
        head = label('NO ONE WINS',60,width//2,height*0.65)
    menu = label('Main Menu',30,leftx,height*0.3)
    bye = label('Quit',30,rightx,height*0.3)
    
    hover0 = hover((width//4)-(hoverwidth//2),(height*0.3)-(hoverheight//2))
    global button
    button = 1
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Insert block comment here describing this function
        '''
        global button
        pyglet.clock.set_fps_limit(60)
        if symbol == key.LEFT:
            if button == 2:
                button = 1
                hover0.x = (width//4) - (hoverwidth//2)
        elif symbol == key.RIGHT:
            if button == 1:
                button = 2
                hover0.x = (width*3//4) - (hoverwidth//2)
        elif symbol == key.ENTER:
            if button == 1:
                return mainmenu()
            elif button == 2:
                window.close()

    def opener(dt):
        '''
        Insert block comment here describing this function
        '''
        todo = 'nothing'

    @window.event
    def on_draw():
        '''
        Insert block comment here describing this function
        '''
        window.clear()
        title.draw()
        head.draw()
        menu.draw()
        bye.draw()
        hover0.draw()
            
    pyglet.clock.schedule_once(opener, 1)
    pyglet.app.run()

def savetostats(score):
    '''
        Insert block comment here describing this function
    '''
    
    try:
        file = open('snakescores.txt','r')
    except FileNotFoundError:
        file = open('snakescores.txt','w+')
        file.write(str(int(score)))
    else:
        if file.read() == '':
            file = open('snakescores.txt','w')
            file.write(str(int(score)))
            file.close()
        else:
            file = open('snakescores.txt','r')
            scores = []
            for i in file:
                scores.append(int(i.strip()))
            file.close()
            yes = True
            for i in range(0,len(scores)):
                if score > scores[i]:
                    scores.insert(i,score)
                    yes = False
                    break
            if len(scores) > 5:
                del scores[5]
            elif yes:
                scores.append(score)
            file = open('snakescores.txt','w')
            for i in range(0,len(scores)):
                scores[i] = str(scores[i])
                file.write(scores[i]+'\n')
            file.close()
                
def statistics():
    '''
        Insert block comment here describing this function
    '''

    results = ['','','','','','']
    title = label('HIGH SCORES',60,centerx,height*0.8)
    menu = label('Back',30,leftx,height*0.3)
    reset = label('Reset',30,centerx,height*0.3)
    bye = label('Quit',30,rightx,height*0.3)
    
    hover0 = hover((width//4)-(hoverwidth//2),(height*0.3)-(hoverheight//2))

    global button
    button = 1

    scores = []
    
    try:
        file = open('snakescores.txt','r')
        empty = file.read()
    except FileNotFoundError:
        file = open('snakescores.txt','w+')
        file.close()
        results[0] = label('No Results',20,centerx,height*0.6)
    else:
        if empty == '':
            results[0] = label('No Results',20,centerx,height*0.6)
        else:
            scores = []
            file = open('snakescores.txt','r')
            for i in file:
                scores.append(int(i.strip()))
            print(scores)
            for i in range(len(scores)):
                line = str(i+1)+'.     '+str(scores[i])
                print(line)
                results[i] = label(line,20,centerx,height*(0.65-(i*0.06)))
        file.close()

    def opener(dt):
        '''
        Insert block comment here describing this function
        '''
        todo = 'nothing'
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Insert block comment here describing this function
        '''

        global button
        pyglet.clock.set_fps_limit(60)
        if symbol == key.LEFT:
            if button == 2:
                button = 1
                hover0.x = (leftx) - (hoverwidth//2)
            elif button == 3:
                button = 2
                hover0.x = (centerx) - (hoverwidth//2)
        elif symbol == key.RIGHT:
            if button == 1:
                button = 2
                hover0.x = (centerx) - (hoverwidth//2)
            elif button == 2:
                button = 3
                hover0.x = (rightx) - (hoverwidth//2)
        elif symbol == key.ENTER:
            if button == 1:
                mainmenu()
            elif button == 2:
                file = open('snakescores.txt','w')
                file.write('')
                file.close()
                statistics()
            elif button == 3:
                window.close()

    @window.event
    def on_draw():
        '''
        Insert block comment here describing this function
        '''
        window.clear()
        title.draw()
        menu.draw()
        reset.draw()
        bye.draw()
        hover0.draw()
        if len(scores) != 0:
            for i in range(len(scores)):
                results[i].draw()
        else:
            results[0].draw()


    pyglet.clock.schedule_once(opener, 1/60)
    pyglet.app.run()

def mainmenu():
    '''
        Insert block comment here describing this function
    '''

    title = label('SNAKES',60,width//2,height*0.8)
    p1label = label('1 Player',30,width//4,height//2)
    p2label = label('2 Player',25,width*3//4,height*0.52)
    p2minilabel = label('Battle',15,width*3//4,height*0.47)
    statlabel = label('High Score',30,width//2,height*0.35)
    statminilabel = label('For 1 Player Mode Only',10,width//2,height*0.3)
    qlabel = label('Quit',30,width//2,height*0.2)

    hover0 = hover((width//4)-(hoverwidth//2),(height//2)-(hoverheight//2)-9)

    global button
    button = 1
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Insert block comment here describing this function
        '''
        
        global button
        
        if symbol == key.LEFT:
            if button == 2:
                button = 1
                hover0.x = (width//4) - (hoverwidth//2)
                hover0.y = (height//2) - (hoverheight//2) - 9
        elif symbol == key.RIGHT:
            if button == 1:
                button = 2
                hover0.x = (width*3//4) - (hoverwidth//2)
                hover0.y = (height//2) - (hoverheight//2) - 9
        elif symbol == key.DOWN:
            if button == 1 or button == 2:
                button = 3
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.35) - (hoverheight//2) - 15
            elif button == 3:
                button = 4
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.2) - (hoverheight//2) - 8
        elif symbol == key.UP:
            if button == 4:
                button = 3
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.35) - (hoverheight//2) - 15
            elif button == 3:
                button = 1
                hover0.x = (width//4) - (hoverwidth//2)
                hover0.y = (height//2) - (hoverheight//2) - 9
        elif symbol == key.ENTER:
            if button == 1:
                oneplayermode()
            elif button == 2:
                twoplayermode()
            elif button == 3:
                statistics()
            elif button == 4:
                window.close()

    def opener(dt):
        '''
        Insert block comment here describing this function
        '''
        todo = 'nothing'

    @window.event
    def on_draw():
        '''
        Insert block comment here describing this function
        '''
        window.clear()
        title.draw()
        p1label.draw()
        p2label.draw()
        p2minilabel.draw()
        statlabel.draw()
        statminilabel.draw()
        qlabel.draw()
        hover0.draw()

    pyglet.clock.schedule_once(opener, 1/60)
    pyglet.app.run()

mainmenu()

