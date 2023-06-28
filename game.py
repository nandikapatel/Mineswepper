app.background = 'grey'

app.playGame = False

# make the 2D list  
app.rows = 13
app.cols = 14
board = makeList(app.rows, app.cols)
placedMines = []
visited = []
minesNeededtoPlace = 35

# draw the reveal the mines button
revealButton = Group(
        Rect(130, 10, 140, 40, fill = gradient('gainsboro', 'silver')),
        Label('Reveal The Mines', 200, 30, size = 15, bold = True)
        )

# make the game board
def makeBoard():
    startX = 25
    startY = 25
    
    for row in range(app.rows):
        for col in range(app.cols):
            
            # increments the x and y postions of the squares (cells)
            x = 25 + (col * startX)
            y = 65 + (row * startY)
            cell = Rect(x,y,25,25,fill = gradient('gainsboro', 'silver'), border ='silver', borderWidth = 0.5)
            
            # add the sqaures to the 2D list to create a grid 
            board[row][col] = cell
makeBoard()

def drawMine(x,y):
    
    # draws the mines depending on the location of cells (the parameters x and y)
    mine = Group (
        Circle(x, y+3,5, fill = 'black'),
        Oval(x-1, y+0.5, 4,3, fill = 'darkGray', opacity = 70, rotateAngle = 290),
        Line(x, y-2, x, y-6, fill = 'burlyWood'),
        Star(x+2, y-6, 4, 7, fill = gradient('yellow','red', 'orange'))
        )

def plantMines():
    
    # keeps track of the amount of mines that are placed on the board
    totalMines = 0
    
    # while the totalMines is less than 35 it will generate random locations on 
    # the board
    while (totalMines < minesNeededtoPlace):
        randomRow = randrange(0,app.rows)
        randomCol = randrange(0,app.cols)
        randomCell = board[randomRow][randomCol]
        
        # makes sure that no randomCell is placed over one another 
        if (randomCell not in placedMines):
            
            # uncomment the function to see the locations of the drawn mines (for testing)
            # drawMine(randomCell.centerX,randomCell.centerY)
            
            # adds the randomCell to the placedMines list to make sure no other
            # mines are drown in the same location ^. And then increments the 
            # totalMines
            placedMines.append(randomCell)
            totalMines += 1
plantMines()

def findCell(x, y):
    for row in range(len(board)):
        for col in range(len(board[row])):
            
            # finds a specific cell on the grid and only return the cell if it hits the 
            # parameters x and y 
            cell = board[row][col]
            if (cell.hits(x,y) == True):
                return cell
    return None

def checkNeighbourCells(currentCell):
    
    # creates a list to keep track of the cells surrounding the 'currentCell' on
    # all sides
    neighbourCells = []
    
    # local variable used to keep track of the number of mines surrounding the
    # 'newCell'
    mineCount = 0
    
    # the range(-1,2) check -1 or +1 of the currentCell
    for row in range(-1,2):
        for col in range(-1,2):
            
            # gets ignored when they equal 0 (when looking at currentCell itself)
            if (row == 0) and (col == 0):
                continue
            
            # gets the new x and y of a specific cell around the currentCell
            newX = int(currentCell.centerX + (col * 25))
            newY = int(currentCell.centerY + (row * 25))
            
            # calls the findCell function to get a row and col based on the newX and newY
            newCell = findCell(newX,newY)
            
            # if the newX and newY are out of bounds (beyond the grid), it gets ignored
            if (newCell == None):
                continue
            
            # adds the neighbouring cell to the neighboutCells list
            neighbourCells.append(newCell)

            # if the newCell (one of the neighbouring cells), has a mine in it,
            # it adds 1 to the mineCount
            if (newCell in placedMines):
                mineCount += 1

    # returns the count of mines around the currentCell and the list of neighbouring cells
    return neighbourCells, mineCount

def checkCell(currentCell):
    
    # calls the checkNeighbourCells function to get the list of neighours and the mineCount
    neighbourCells, mineCount = checkNeighbourCells(currentCell)

    # if the count is 0, it looks a neighnouring cell
    if (mineCount == 0):
        for cell in neighbourCells:
            
            # checks if it is not already in the visited list (so it doesnt double check 
            # the same things)
            if (cell not in visited):
                cell.fill = 'silver'
                cell.border = 'gainsboro'
                visited.append(cell)
                
                # it undergoes recursion on the checkCell function
                # it will call the function again from within itself, but the cell
                # (the neighbouring cell of the currentCell) being the new 'currentCell'
                # with each call. it finds the neighbours of that cell and then 
                # checks minecount again
                # it keeps recursing like this until all potential neighbours have 
                # a mineCount greater than 0
                checkCell(cell)
    
    # if the count isn't 0, it displays the count on its respective cell
    else:
        count = Label(str(mineCount), currentCell.centerX, currentCell.centerY)
    
    # changes the fill and border colour of the clicked on cell
    currentCell.fill = 'silver'
    currentCell.border = 'gainsboro'
    
    # add the currentCell into the visited list, if not already, so it doesn't get 
    # looked at twice
    if (currentCell not in visited):
        visited.append(currentCell)

def checkLoss(x,y):
    loss = False
    
    # loops through every mine in the placedMines list, check to see it x and y have 
    # hit it. if so, it changes the color of the mine it hit, and loss to true
    for mine in placedMines:
        if (mine.hits(x,y) == True):
            mine.fill = 'red'
            loss = True 
            break 

    # if loss is true, it draws all the placed mines on the screen
    if (loss == True):
        for cell in placedMines:
            drawMine(cell.centerX,cell.centerY)
        return True 
    return False
    
def checkWin():
    
    # there's is a win if the len of the visited list is equal to the amount of cells
    # that don't have a mine in it
    win = (app.rows * app.cols) - minesNeededtoPlace
    
    if (len(visited) == win):
        return True
    else:
        return False 
   
def revealTheMines(x,y):
    
    # if the button is pressed, all the placed mines are drawn 
    if (revealButton.hits(x,y) == True):
        for mine in placedMines:
            drawMine(mine.centerX,mine.centerY)
        return True
    return False
    
def onMousePress(mouseX, mouseY):
    if (app.playGame == True):
        
        # if the button is pressed, a game over banner is displayed and the game stops
        if (revealTheMines(mouseX,mouseY) == True):
            Rect(0,2,400,60, fill = 'red')
            Label("Game Over", 200,31, size = 35, font = 'monospace')
            app.stop()
        
        # locates the cell that was clicked on 
        cell = findCell(mouseX,mouseY) 
        
        # if clicked outside of the grid, it gets ignored
        if (cell == None):
            return
        
        # if the clicked cell isn't in the visited cell, it call the checkCell function 
        # this helps avoid clicking on already revealled cells more than once
        if (cell not in visited):
            checkCell(cell)
        
        # draws the game loss banner and stops the game
        if (checkLoss(mouseX,mouseY) == True):
            Rect(0,150,400,100, fill = 'red'),
            Label("Oh No!", 200,180, size = 35, font = 'monospace')
            Label("The Mines Blew Up!", 200,220,size = 35, font = 'monospace')
            app.stop()
        
        # draws the game won banner and stops the game
        if (checkWin() == True):
            Rect(0,150,400,100, fill = 'Green')
            Label("Phew! You revealed", 200,180, size = 35, font = 'monospace')
            Label("the safe spots!", 200,220, size = 35, font = 'monospace')
            app.stop()

# game rules
gameIntro = Group(
    Rect(0, 0, 400, 400, fill='whiteSmoke', opacity=90),
    Label("Let's Play Minesweepers!", 200, 90, fill='navy', size=30,
          bold=True),
    Label("Click on the squares in the grid to reveal", 200, 140, fill='steelBlue', size=20),
    Label("safe spots.", 200, 170, fill='steelBlue', size=20),
    Label("Be careful not to click on any of the 35", 200, 200, fill='steelBlue', size=20),
    Label("mines or else they'll blow up! Reveal all", 200, 230, fill='steelBlue', size=20),
    Label("the safe spots and win the game!", 200, 260, fill='steelBlue', size=20),      
    Label('Press space to start', 200, 320, fill='navy', size=20, bold=True),
    Label('Good Luck!', 200, 350, fill='navy', size=20, bold=True)
    )

def onKeyPress(key):
    # starts a new game when space is pressed and the game is not already 
    # being played. it makes the game rules invisible and sets playGame to true.
    if ('space' in key) and (app.playGame == False):
        gameIntro.visible = False
        app.playGame = True
      
