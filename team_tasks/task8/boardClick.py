#This file handles all the clicking and logic of the game
import constants
import turtleMove
import listInterpret
import listUpdater
import victoryStatus
import playerVictory
import fileHandler
import random
import screenWriter
import converter
import time

#Updates the scoreboard to reflect the game state
#Params: game_state, The state of the game
#Returns: None
def updateScoreBoard(game_state):
    black_score = victoryStatus.countPieces(constants.PIECE_BLACK, game_state)
    white_score = victoryStatus.countPieces(constants.PIECE_WHITE, game_state)
    screenWriter.writeScore(black_score, white_score)

#Gets a move from an x and y coordinate
#Params: x, The x coordinate of a click
#        y, The x coordinate of a click
#Returns: A string containing the move. ex, 'A1'
def getMove(x, y):
    #Convert the x and y to the coordinate of a cell
    x = convertXToBoard(x)
    y = convertYToBoard(y)

    #Convert x and y to column and row
    letter = constants.COLUMN_LETTERS[x]
    number = constants.ROW_NUMBERS[constants.NUM_OF_ROWS - (y + 1)]

    #The move being made
    move = letter + str(number)

    return move

def countUpdatedPieces(game_state, move, move_num):
    #Create a deep copy of game state
    state_string = converter.toString(game_state)
    copy_state = converter.toList(state_string)

    piece = listInterpret.whoseTurn(move_num)
    changed_state = listUpdater.updateGameState(copy_state, move, piece, False)

    change_count = 0
    for i in range(len(game_state)):
        for j in range(len(game_state[i])):
            if game_state[j][i] != changed_state[j][i]:
                change_count += 1

    return change_count


#Gets valid moves depending on state and move number
#Params: state, The game state
#        move_num, The current move numbers
#Returns: Possible moves for move number
def getMovesForTurn(state, move_num):#TODO Comment this method
    moves_list = []

    for i in range(len(state)):
        for j in range(len(state[i])):
            letter = constants.COLUMN_LETTERS[i]
            number = constants.ROW_NUMBERS[j]
            move = letter + str(number)

            if state[j][i] == constants.PIECE_NONE:
                changes = countUpdatedPieces(state, move, move_num)

                if changes > constants.PIECE_CHANGE_THRESHOLD:
                    moves_list.append(move)

    return moves_list

#Displays all valid moves to the board
#Params: state, Current game state
#        move_num, Move number
#Returns: None
def displayValidMoves(state, move_num):
    valid_moves = getMovesForTurn(state, move_num)
    turtleMove.displayValidMoves(valid_moves, state)

#Checks if a move is valid
#Params: state, The game state
#        move, The move to check
#        move_num, The number of the move
#Returns: True if the move is valid, False otherwise
def isValidMove(state, move, move_num):
    isValid = move in getMovesForTurn(state, move_num)
    return isValid

#Converts an x coordinate to a cell on the board
#Params: x, The x coordinate
#Returns: An index of the x coordinate of a cell
def convertXToBoard(x):
    x = (x / constants.CELL_WIDTH) - constants.OFFSET_OF_COLUMNS
    return int(x)

#Converts a y coordinate to a cell on the board
#Params: y, The y coordinate
#Returns: An index of the y coordinate of a cell
def convertYToBoard(y):
    y = (y / constants.CELL_HEIGHT) - constants.OFFSET_OF_ROWS
    return int(y)

#Checks if a piece can be placed at a location
#Params: x, The x coordinate of the location
#        y, The y coordinate of the location
#Returns: True if a piece can be placed at a location, False otherwise
def isValidSquare(x, y):
    #Check if each coordinate is valid separately
    x_valid = x >= constants.LEFT_MOST_X and x <= constants.RIGHT_MOST_X
    y_valid = y >= constants.BOTTOM_MOST_Y and y <= constants.TOP_MOST_Y

    #Check if the x and y are in any cell
    return x_valid and y_valid

#The computer generates a move and places a piece if possible
#Params: state, The current game state
#        move_num, The current move number
#Returns: The new game state
def computerTurn(state, move_num):
    #Get a list of possible moves
    valid_moves = getMovesForTurn(state, move_num)

    #If no moves are valid then the move is skipped
    if len(valid_moves) == 0:
        return state
    else:
        #Generate a random number
        random_num = random.randrange(len(valid_moves))

        #Get a move from the list
        move = valid_moves[random_num]

        #Make the move
        return listInterpret.listInterpret(state, move, move_num)

#Displays an ending message and clears the temporary file
#Params: game_state, The state of the game
#Returns: None
def finishGame(game_state):
    #Print who won
    game_status = playerVictory.playerWon(game_state)
    screenWriter.writeMessage(game_status)

    #Wait for user
    constants.WINDOW.exitonclick()

    #Reset state and move
    fileHandler.saveVariable(constants.VARIABLE_STATE, constants.VARIABLE_BLANK)
    fileHandler.saveVariable(constants.VARIABLE_MOVE, constants.VARIABLE_BLANK)

#Changes variables needed for a move
#Params: None
#Returns: A tuple of (game_state, move_num)
def startMove():
    #Save variable
    fileHandler.saveVariable(constants.VARIABLE_MOVING, constants.VARIABLE_BOOL_TRUE)

    #Load the variables we need
    game_state = converter.toList(fileHandler.loadVariable(constants.VARIABLE_STATE))
    move_num = int(fileHandler.loadVariable(constants.VARIABLE_MOVE))

    #Return game_state and move_num as a tuple
    return (game_state, move_num)

#Saves state and move number to a file,
#as well as updating the score board and showing valid moves
#Params: game_state, The state of the game
#        move_num, The number of the move
#Returns: None
def endMove(game_state, move_num):
    #Save the variables
    fileHandler.saveVariable(constants.VARIABLE_STATE, converter.toString(game_state))
    fileHandler.saveVariable(constants.VARIABLE_MOVE, str(move_num))

    #Reload the board
    loadGame(constants.TEMP_FILE, False)

    #Update the scoreboard
    updateScoreBoard(converter.toList(fileHandler.loadVariable(constants.VARIABLE_STATE)))

    #Update the window
    constants.WINDOW.update()

#Makes the player's move visible
#Params: game_state, The game state
#        move, The move being made
#        move_num, The current move number
#Returns: move_num + 1
def makePlayerMove(game_state, move, move_num):
    #Clear space at move
    turtleMove.resetSquare(move)

    #Update the game state
    game_state = listInterpret.listInterpret(game_state, move, move_num)

    #Return the new move number
    return move_num + 1

#Places a piece at a location if it is a cell
#Params: x, The x location to check
#        y, The y location to check
#Returns: None
def placePiece(x, y):
    #Make sure a move is not being made
    if fileHandler.loadVariable(constants.VARIABLE_MOVING) == constants.VARIABLE_BOOL_FALSE:
        #Get the variables for the start of the move
        game_state, move_num = startMove()

        #Make sure the game is not over
        if not victoryStatus.endGameStatus(game_state):
            #Check if the point is valid
            if isValidSquare(x, y) and isValidMove(game_state, getMove(x, y), move_num):
                #Get the move
                move = getMove(x, y)

                #Make the player's move
                move_num = makePlayerMove(game_state, move, move_num)

                screenWriter.writeTurn(move_num)

                #Check if the game is over
                if not victoryStatus.endGameStatus(game_state):
                    #Small delay
                    time.sleep(constants.MOVE_DELAY)

                    #Let the computer make a turn
                    game_state = computerTurn(game_state, move_num)
                    move_num += 1

                #End the move
                endMove(game_state, move_num)
        else:
            finishGame(game_state)

        #Save variable
        fileHandler.saveVariable(constants.VARIABLE_MOVING, constants.VARIABLE_BOOL_FALSE)

#Saves the current game configuration
#Params: None
#Returns: None
def saveGame():
    #Get current game info
    current_state = fileHandler.loadVariable(constants.VARIABLE_STATE)
    current_move_num = fileHandler.loadVariable(constants.VARIABLE_MOVE)

    #Save game info
    fileHandler.saveVariable(constants.VARIABLE_STATE, current_state, constants.SAVE_FILE)
    fileHandler.saveVariable(constants.VARIABLE_MOVE, current_move_num, constants.SAVE_FILE)

#Loads the saved game configuration
#Params: file_name, The file to load from
#        redraw, Whether the board should be redrawn
#Returns: None
def loadGame(file_name = constants.SAVE_FILE, redraw = True):
    #Load game info
    saved_state = fileHandler.loadVariable(constants.VARIABLE_STATE, file_name)
    saved_move_num = fileHandler.loadVariable(constants.VARIABLE_MOVE, file_name)

    #Write loaded variables to variables file
    fileHandler.saveVariable(constants.VARIABLE_STATE, saved_state)
    fileHandler.saveVariable(constants.VARIABLE_MOVE, saved_move_num)

    #Convert state from string to list
    saved_state = converter.toList(saved_state)

    if redraw:
        #Load board configuration
        listInterpret.listToPiece(saved_state)

    #Update the scoreboard
    updateScoreBoard(saved_move_num)

    screenWriter.writeTurn(saved_move_num)

    #Reset valid moves from turtleMove
    turtleMove.SHOWN_MOVES = []

    #Show possible moves
    displayValidMoves(saved_state, int(saved_move_num))

#Gracefully quits the game
#Params: None
#Returns: None
def quitGame():
    #Reset variables
    fileHandler.saveVariable(constants.VARIABLE_STATE, constants.VARIABLE_BLANK)
    fileHandler.saveVariable(constants.VARIABLE_MOVE, constants.VARIABLE_BLANK)
    fileHandler.saveVariable(constants.VARIABLE_MOVING, constants.VARIABLE_BOOL_FALSE)

    #Close the game
    wn = constants.WINDOW
    wn.bye()

#The main loop of the function
#Waits for input from the user
#Params: game_state, The current game state
#        move_num, The current move number
#        player_move, Whether it is the player's move or not
#Returns: None
def run(game_state, move_num, player_move):
    #Allow the computer to make it's move
    if not player_move:
        state = computerTurn(game_state, move_num)
        move_num += 1

    #End the computer's move
    endMove(game_state, move_num)

    #Show possible moves
    displayValidMoves(game_state, move_num)

    #Save variables to be used later
    fileHandler.saveVariable(constants.VARIABLE_STATE, converter.toString(game_state))
    fileHandler.saveVariable(constants.VARIABLE_MOVE, str(move_num))
    fileHandler.saveVariable(constants.VARIABLE_MOVING, constants.VARIABLE_BOOL_FALSE)

    #Set up the window
    wn = constants.WINDOW
    wn.onclick(placePiece)
    wn.onkey(saveGame, constants.SAVE_KEY)
    wn.onkey(loadGame, constants.LOAD_KEY)
    wn.onkey(quitGame, constants.EXIT_KEY)
    wn.listen()
    wn.mainloop()
