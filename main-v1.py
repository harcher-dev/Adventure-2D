import tkinter as tk

# debug
coordsActive = True
overrideLevelData = False
newLevelData = None # you data goes here instead of none

# main
window = tk.Tk()
window.title('2D Game')
window.geometry('720x720')

# plr attributes
playerX = tk.DoubleVar(value = 0.5)
playerY = tk.DoubleVar(value = 0.5)
playerCoins = tk.IntVar(value = 0)

# level data
currentLevel = tk.IntVar(value = 0)

levelData = {
    0 : {'wallPositions' : [[0.4,0.4], [0.3,0.4], [0.4,0.3]],
         'coinPositions' : [[0.2,0.4], [0.6,0.4]],
         'killPositions' : [[0.1,0.4]],
         'endPos' : [0.2,0.3],
         'startPos' : [0.5,0.5]},
    
    1 : {'wallPositions' : [[0.4,0.3], [0.3,0.1], [0.2,0.7]],
         'coinPositions' : [[0.5,0.5]],
         'killPositions' : [[0.2,0.4]],
         'endPos' : [0.2,0.3],
         'startPos' : [0.5,0.7]}
}

# override level data mode
if overrideLevelData:
    levelData = newLevelData

#global collisionObjectPositions, coinObjectsPositions, killObjectsPositions, endPos, startPos
try:
    collisionObjectPositions = levelData[currentLevel.get()]["wallPositions"]
except: raise 'Error reading level data... have you left a debug setting on?'
coinObjectsPositions = levelData[currentLevel.get()]["coinPositions"]
killObjectsPositions = levelData[currentLevel.get()]["killPositions"]

try:
    endPos = levelData[currentLevel.get()]["endPos"]
except: raise 'Error reading level data... have you forgot to add an end position to your level?'
startPos = levelData[currentLevel.get()]["startPos"]

coinObjects = []
killObjects = []
collisionObjects = []
otherObjects = []


# events
def playerKilled():
    playerY.set(startPos[0])
    playerX.set(startPos[1])

def loadLevel():
    # destroy previous level
    for x in collisionObjects:
        x.destroy()
    for x in killObjects:
        x.destroy()
    for x in coinObjects:
        x.destroy()
    for x in otherObjects:
        x.destroy()
        
    collisionObjects.clear()
    coinObjects.clear()
    killObjects.clear()
    otherObjects.clear()
        
    
    # load next level
    currentLevel.set(currentLevel.get()+1)
    if len(levelData)-1 >= currentLevel.get():
        global collisionObjectPositions, coinObjectsPositions, killObjectsPositions, endPos, startPos
        collisionObjectPositions = levelData[currentLevel.get()]["wallPositions"]
        coinObjectsPositions = levelData[currentLevel.get()]["coinPositions"]
        killObjectsPositions = levelData[currentLevel.get()]["killPositions"]

        endPos = levelData[currentLevel.get()]["endPos"]
        startPos = levelData[currentLevel.get()]["startPos"]
        
        playerKilled()
    
        drawLevel()
    else:
        # all levels complete
        # add victory code here
        pass

# hit detections
def checkForObject():
    currentPlrY = round(playerY.get(), 3)
    currentPlrX = round(playerX.get(), 3)
    
    for pos in collisionObjectPositions:
        if pos[0] == currentPlrX:
            if pos[1] == currentPlrY:
                # wall hit
                return 'wall'
    
    for index, pos in enumerate(coinObjectsPositions):
        if pos[0] == currentPlrX:
            if pos[1] == currentPlrY:
                # coin hit - dodgy code not sure if it works
                coinObjects[index].destroy()
                coinObjectsPositions.pop(index)
                playerCoins.set(playerCoins.get()+1)
                #print('coin hit', str(currentPlrX), str(currentPlrY))
                return 'coin'
    
    for index, pos in enumerate(killObjectsPositions):
        if pos[0] == currentPlrX:
            if pos[1] == currentPlrY:
                # kill obj hit
                playerKilled()
                return 'killObj'
    
    if [currentPlrX,currentPlrY] == endPos:
        # endPos hit
        loadLevel()
        return 'nextLevel'
    
    return False

# plr controls functions
def up(keyInfo):
    playerY.set(playerY.get()-0.05)
    if not checkForObject() == 'wall':
        playerDisplay.place(anchor = 'center', relx = playerX.get(), rely = playerY.get())
    else: playerY.set(playerY.get()+0.05)

def down(keyInfo):
    playerY.set(playerY.get()+0.05)
    if not checkForObject() == 'wall':
        playerDisplay.place(anchor = 'center', relx = playerX.get(), rely = playerY.get())
    else: playerY.set(playerY.get()-0.05)

def left(keyInfo):
    playerX.set(playerX.get()-0.05)
    if not checkForObject() == 'wall':
        playerDisplay.place(anchor = 'center', relx = playerX.get(), rely = playerY.get())
    else: playerX.set(playerX.get()+0.05)

def right(keyInfo):
    playerX.set(playerX.get()+0.05)
    if not checkForObject() == 'wall':
        playerDisplay.place(anchor = 'center', relx = playerX.get(), rely = playerY.get())
    else: playerX.set(playerX.get()-0.05)
    
window.bind('<w>', up)
window.bind('<s>', down)
window.bind('<a>', left)
window.bind('<d>', right)

# player object
playerDisplay = tk.Label(
    window,
    text = ':(',
    font = ('Arial', 12),
    bg = '#000000',
    fg = '#FFFFFF'
)

playerDisplay.place(anchor = 'center', relx = playerX.get(), rely = playerY.get())

# draw objects
def drawLevel():
    for data in collisionObjectPositions:
        if len(data) == 2:
            newObject = tk.Label(
                window,
                text = '    ',
                font = ('Arial', 15),
                bg = '#0000FF'
            )
        else:
            newObject = tk.Label(
                    window,
                    text = '    ',
                    font = ('Arial', 15),
                    bg = data[2]
                )
        
        newObject.place(anchor = 'center', relx = data[0], rely = data[1])
        collisionObjects.append(newObject)

    for position in coinObjectsPositions:
        newObject = tk.Label(
            window,
            text = '£',
            font = ('Arial', 15),
            bg = '#FFFF00'
        )
        
        newObject.place(anchor = 'center', relx = position[0], rely = position[1])
        coinObjects.append(newObject)
        
    for position in killObjectsPositions:
        newObject = tk.Label(
            window,
            text = '    ',
            font = ('Arial', 15),
            bg = '#FF0000'
        )
        
        newObject.place(anchor = 'center', relx = position[0], rely = position[1])
        killObjects.append(newObject)
        
    endObject = tk.Label(
        window,
        text = '    ',
        font = ('Arial', 15),
        bg = '#00FF00'
    )
        
    endObject.place(anchor = 'center', relx = endPos[0], rely = endPos[1])
    otherObjects.append(endObject)
    
drawLevel()

# debug co-ordinates
if coordsActive:
    plrCoords1 = tk.Label(
        window,
        textvariable=playerX,
        font = ('Arial', 12),
    )

    plrCoords2 = tk.Label(
        window,
        textvariable=playerY,
        font = ('Arial', 12),
    )

    plrCoords1.pack()
    plrCoords2.pack()

# Stats display

plrCoinText = tk.Label(
        window,
        text = 'Coins:',
        font = ('Arial', 12)
    )

plrCoinText.place(anchor = 'nw', relx = 0.88, rely = 0.85)

playerCoinsDisplay = tk.Label(
        window,
        textvariable=playerCoins,
        font = ('Arial', 12),
    )

playerCoinsDisplay.place(anchor = 'nw', relx = 0.9, rely = 0.9)

timer = tk.IntVar(value = 0)
def incrementTimer():
    timer.set(timer.get()+1)
    window.after(1000, incrementTimer)
incrementTimer()

timerDisplay = tk.Label(
        window,
        textvariable=timer,
        font = ('Arial', 12),
    )

timerDisplay.place(anchor = 'nw', relx = 0.1, rely = 0.9)

# mainloop
window.mainloop()