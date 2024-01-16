# modified version of the main game to speed up level creation

import tkinter as tk

# debug
coordsActive = True

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
    0 : {'wallPositions' : [[0.4,0.5]],
         'coinPositions' : [],
         'killPositions' : [],
         'endPos' : [],
         'startPos' : [0.5,0.5]},
}

collisionObjectPositions = levelData[currentLevel.get()]["wallPositions"]
coinObjectsPositions = levelData[currentLevel.get()]["coinPositions"]
killObjectsPositions = levelData[currentLevel.get()]["killPositions"]

endPos = levelData[currentLevel.get()]["endPos"]
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
    global collisionObjectPositions, coinObjectsPositions, killObjectsPositions, endPos, startPos
    collisionObjectPositions = levelData[currentLevel.get()]["wallPositions"]
    coinObjectsPositions = levelData[currentLevel.get()]["coinPositions"]
    killObjectsPositions = levelData[currentLevel.get()]["killPositions"]

    endPos = levelData[currentLevel.get()]["endPos"]
    startPos = levelData[currentLevel.get()]["startPos"]
    
    # dont kill player in editor
    #playerKilled()

# hit detections
def checkForObject():
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

# draw level
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
    
    if len(endPos) == 2:
        endObject = tk.Label(
            window,
            text = '    ',
            font = ('Arial', 15),
            bg = '#00FF00'
        )
            
        endObject.place(anchor = 'center', relx = endPos[0], rely = endPos[1])
        otherObjects.append(endObject)

drawLevel()

# player object
playerDisplay = tk.Label(
    window,
    text = '00',
    font = ('Arial', 12),
    bg = '#000000',
    fg = '#FFFFFF'
)

playerDisplay.place(anchor = 'center', relx = playerX.get(), rely = playerY.get())

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

# level editor functionality
buildMode = tk.StringVar(value = 'wall')

# level data format
#newLevelData = {
#    0 : {'wallPositions' : [],
#         'coinPositions' : [],
#         'killPositions' : [],
#         'endPos' : [],
#         'startPos' : [0.5,0.5]},
#}

allModes = ['wall', 'coin', 'end', 'start', 'killObj']
def changeBuild(catch = None):
    if buildMode.get() == 'killObj':
        buildMode.set('wall')
    else:
        buildMode.set(allModes[(allModes.index(buildMode.get())+1)])

def placeBuild(catch = None):
    currentPos = [round(playerX.get(), 3), round(playerY.get(), 3)]
    match buildMode.get():
        case 'wall':
            levelData[currentLevel.get()]["wallPositions"].append(currentPos)
            drawLevel()
        case 'coin':
            levelData[currentLevel.get()]["coinPositions"].append(currentPos)
            drawLevel()
        case 'killObj':
            levelData[currentLevel.get()]["killPositions"].append(currentPos)
            drawLevel()
        case 'end':
            levelData[currentLevel.get()]["endPos"] = currentPos
            drawLevel()
        case 'start':
            levelData[currentLevel.get()]["startPos"] = currentPos
            drawLevel()
      
            
window.bind('<space>', changeBuild)
window.bind('<Return>', placeBuild)

modeDisplay = tk.Label(window, textvariable = buildMode)
modeDisplay.place(anchor='ne', relx = 0.1, rely = 0.9)

def generateLevelData():
    print('New level data:\n')  
    print(levelData, '\n')

printDataBtn = tk.Button(window, text='Generate Level Data', command = generateLevelData)
printDataBtn.place(anchor='ne', relx = 0.2, rely = 0.95)

# mainloop
window.mainloop()