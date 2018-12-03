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
color3 = (252,216,13,255) # orange of player 2

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

# some set positions
centerx = width//2
leftx = width//4
rightx = width*3//4
leftgridx = gridSprite.x//2
rightgridx = (gridSprite.width + 320) + ((width-(gridSprite.width + gridSprite.x))//2)

def label(l,s,x,y,c=None):
    '''
        Instead of using a label class everytime,
        a function for labels is made to define some attributes
        that will be used for all labels
    '''
    # c is optional argument, can use it to change font color, but there is a default color.
    if c != None:
        return pyglet.text.Label(l, font_name=name, font_size=s, color=c, anchor_x='center', anchor_y='center', x=x, y=y)
    else:
        return pyglet.text.Label(l, font_name=name, font_size=s, color=(color1), anchor_x='center', anchor_y='center', x=x, y=y)


def hover(x,y):
    '''
        A function for hovers is made
        to set some attributes and properties
        that will be used by all hovers
    '''
    a = pyglet.sprite.Sprite(pyglet.image.load('hover.png'), x=x, y=y)
    a.scale = 0.5
    a.opacity = 75
    return a

def oneplayermode():
    
    '''
        Start of 1 Player Mode
    '''

    # initial acceleration will be 1/7 seconds
    global a
    a = 7
    
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
        Performs an action on Player1 Snake
        when one of the W, A, S, D keys is pressed
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
        This function does nothing
        But is added in order to open the window in 1/60 seconds
        '''
        todo = 'nothing'

    def acceleration(dt):
        '''
        Increases the speed of game
        '''
        global a
        a += 0.5
        print('a=1/',a)
        
    def updatePos(dt):
        '''
        Updates the snake's segments' positions and its food
        Ends if the snake has collided somewhere
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
        Draws everything needed to be displayed for the 1 Player Game Window
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
        
    pyglet.clock.schedule_interval(updatePos, 1/a)
    pyglet.clock.schedule_interval(acceleration,5)
    pyglet.clock.schedule_once(opener,1/60)
    pyglet.app.run()

def twoplayermode():
    
    '''
        Start of 2 Player Battle Game
    '''

    # initial acceleration will be 1/7 seconds
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
        Performs an action on Player1 Snake
        when one of the W, A, S, D keys is pressed
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
                
        '''
        Performs an action on Player2 Snake
        when one of the UP, DOWN, LEFT, RIGHT keys is pressed
        '''
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
        This function does nothing
        but is added in order to open the window in 1/60 seconds
        '''
        todo = 'nothing'

    def acceleration(dt):
        '''
        Increases the speed of game
        '''
        global a
        a += 0.5
        print('a=1/',a)

    def updatePos(dt):
        '''
        Updates the snake's segments' positions and its food
        Ends if the snake has collided somewhere
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
        Draws everything needed to be displayed for the 2 Player Game Window
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
        
    pyglet.clock.schedule_interval(updatePos, 1/a)
    pyglet.clock.schedule_interval(acceleration,5)
    pyglet.clock.schedule_once(opener,1/60)
    pyglet.app.run()
    
def p1gameover(scr):
    '''
        Game Over Window for the 1 Player Game
        
        Displays GAME OVER, the Score of Player1
        And 2 Buttons that lead to Main Menu and Quit
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
        Moves the hover through the buttons
        when the LEFT or RIGHT keys are pressed
        then moves to Main Menu or Quit
        when ENTER is pressed
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
        This function does nothing
        But is added in order to open the window in 1/60 seconds
        '''
        todo = 'nothing'

    @window.event
    def on_draw():
        '''
        Draws everything needed to be displayed for the 1 Player Game Over Window
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
        Game Over Window for the 2 Player Game
        
        Displays GAME OVER, the Winner of the Game
        and 2 Buttons that lead to Main Menu and Quit
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
        Moves the hover through the buttons
        when the LEFT or RIGHT keys are pressed
        then moves to Main Menu or Quit
        when ENTER is pressed
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
        This function does nothing
        but is added in order to open the window in 1/60 seconds
        '''
        todo = 'nothing'

    @window.event
    def on_draw():
        '''
        Draws everything needed to be displayed for the 2 Player Game Over Window
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
        Saves Score to Stats file (snakescores.txt)
        Only the Top 5 Scores are saved
    '''
    try:
        file = open('snakescores.txt','r')
    except FileNotFoundError:
        file = open('snakescores.txt','w+')
        file.write(str(int(score)))
        file.close()
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
                
def highscores():
    '''
        Displays the High Scores of the 1 Player Game
        Only the Top 5 Scores are displayed
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
        This function does nothing
        But is added in order to open the window in 1/60 seconds
        '''
        todo = 'nothing'
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Moves the hover through the buttons
        when the LEFT or RIGHT keys are pressed
        then moves to Back to Main Menu or Quit
        when ENTER is pressed
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
                highscores()
            elif button == 3:
                window.close()

    @window.event
    def on_draw():
        '''
        Draws everything needed to be displayed for the High Score Window
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
        The first window to be displayed when the game is opened
        is the Main Menu
        Here, you can see the title of the game and 4 buttons:
        1 Player, 2 Player Battle, High Score, Quit
    '''

    title = label('SNAKES',60,centerx,height*0.85)
    p1label = label('1 Player',30,leftx,height*0.65)
    p2label = label('2 Player',25,rightx,height*0.663)
    p2minilabel = label('Battle',15,rightx,height*0.613)
    statlabel = label('High Score',30,centerx,height*0.5)
    statminilabel = label('For 1 Player Mode Only',10,centerx,height*0.45)
    htplabel = label('How to Play',30,centerx,height*0.35)
    qlabel = label('Quit',30,centerx,height*0.2)

    black = (0,0,0,0)
    htp101 = pyglet.text.Label('PLAY 1 Player Game\n\nYour objective, as the snake, is to eat the square and continue growing\n-----\nDo not collide with yourself nor the border of the grid',
                               font_name=name,font_size=15,color=black,
                               x=width*0.02,y=height*0.5,
                               multiline=True,width=width*0.3)
    htp201 = pyglet.text.Label('PLAY 2 Player Game\n\nYour objective, as the snake, is to survive longer than the other player\nYou can still eat the square and continue growing\n-----\nDo not collide with yourself, the border of the grid nor the other player',
                               font_name=name,font_size=15,color=black,
                               x=width*0.69,y=height*0.5,
                               multiline=True,width=width*0.3)

    hover0 = hover((width//4)-(hoverwidth//2),(height*0.65)-(hoverheight//2)-9)

    global button
    button = 1
    
    @window.event
    def on_key_press(symbol, modifiers):
        '''
        Moves the hover through the buttons
        when the UP, DOWN, LEFT, RIGHT keys are pressed
        then performs the function of the button
        where ENTER is pressed
        '''
        global button
        
        if symbol == key.LEFT or symbol == key.A:
            if button == 2:
                button = 1
                hover0.x = (width//4) - (hoverwidth//2)
                hover0.y = (height*0.65) - (hoverheight//2) - 9
        elif symbol == key.RIGHT or symbol == key.D:
            if button == 1:
                button = 2
                hover0.x = (width*3//4) - (hoverwidth//2)
                hover0.y = (height*0.65) - (hoverheight//2) - 9
        elif symbol == key.DOWN or symbol == key.S:
            if button == 1 or button == 2:
                button = 3
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.5) - (hoverheight//2) - 15
            elif button == 3:
                button = 4
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.35) - (hoverheight//2) - 9
            elif button == 4:
                button = 5
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.2) - (hoverheight//2) - 8
        elif symbol == key.UP or symbol == key.W:
            if button == 5:
                button = 4
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.35) - (hoverheight//2) - 9
            elif button == 4:
                button = 3
                hover0.x = (width//2) - (hoverwidth//2)
                hover0.y = (height*0.5) - (hoverheight//2) - 15
            elif button == 3:
                button = 1
                hover0.x = (width//4) - (hoverwidth//2)
                hover0.y = (height*0.65) - (hoverheight//2) - 9
        elif symbol == key.ENTER:
            if button == 1:
                oneplayermode()
            elif button == 2:
                twoplayermode()
            elif button == 3:
                highscores()
            elif button == 5:
                window.close()
        if button == 4:
            htp101.color = color2
            htp201.color = color2
        else:
            htp101.color = black
            htp201.color = black

    def opener(dt):
        '''
        This function does nothing
        But is added in order to open the window in 1/60 seconds
        '''
        todo = 'nothing'

    @window.event
    def on_draw():
        '''
        Draws everything needed to be displayed for the Main Menu Window
        '''
        window.clear()
        title.draw()
        p1label.draw()
        p2label.draw()
        p2minilabel.draw()
        htplabel.draw()
        statlabel.draw()
        statminilabel.draw()
        qlabel.draw()
        hover0.draw()
        htp101.draw()
        htp201.draw()

    pyglet.clock.schedule_once(opener, 1/60)
    pyglet.app.run()

mainmenu()
