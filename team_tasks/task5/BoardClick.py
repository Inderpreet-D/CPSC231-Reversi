import Constants
import TurtleMove
import StringInterpret
import StringMove
import VictoryStatus
import PlayerVictory
import Main

#We need a global variable to hold the state
#of the game and the move number
game_state = ""
move_num = 4

#Converts an x coordinate to a cell on the board
#Params: x, The x coordinate
#Returns: An index of the x coordinate of a cell
def convertXToBoard(x):
    x = (x / Constants.CELL_WIDTH) - Constants.OFFSET_OF_COLUMNS
    return int(x)

#Converts a y coordinate to a cell on the board
#Params: y, The y coordinate
#Returns: An index of the y coordinate of a cell
def convertYToBoard(y):
    y = (y / Constants.CELL_HEIGHT) - Constants.OFFSET_OF_ROWS
    return int(y)

#Checks if a piece can be placed at a location
#Params: x, The x coordinate of the location
#        y, The y coordinate of the location
#Returns: True if a piece can be placed at a location, False otherwise
def isValidSquare(x, y):
    #Check if each coordinate is valid separately
    xValid = x >= Constants.LEFT_MOST_X and x <= Constants.RIGHT_MOST_X
    yValid = y >= Constants.BOTTOM_MOST_Y and y <= Constants.TOP_MOST_Y

    #Check if the x and y are in any cell
    return xValid and yValid

#Places a piece at a location if it is a cell
#Params: x, The x location to check
#        y, The y location to check
#Returns: None
def place_piece(x, y):
    #Specify that we are using global move_num and game_state
    global move_num
    global game_state

    #Make sure the game is not over
    if VictoryStatus.endGameStatus(game_state) != True:
        #Check if the point is valid
        if isValidSquare(x, y):
            #Convert the x and y to the coordinate of a cell
            x = convertXToBoard(x)
            y = convertYToBoard(y)

            #Convert x and y to column and row
            letter = Constants.COLUMN_LETTERS[x]
            number = Constants.ROW_NUMBERS[Constants.NUM_OF_ROWS - (y + 1)]

            #Make sure a piece is not in this location
            if StringMove.validateMoveLocation(game_state, letter + str(number)):

                #Update the game state
                game_state = StringInterpret.stringInterpret(game_state, letter + str(number), move_num)
                move_num += 1
    else:
        #Print who won
    	print(PlayerVictory.playerWon(game_state))

    	#Wait for user
    	Constants.WINDOW.exitonclick()

#The main loop of the function
#Waits for input from the user
#Params: state, The current game state
#Returns: None
def run(state):
    #Specify the need to use a global variable
    global game_state
    game_state = state

    #Set up the window
    wn = Constants.WINDOW
    wn.onclick(place_piece)
    wn.onkey(wn.bye, "space")
    wn.listen()
    wn.mainloop()