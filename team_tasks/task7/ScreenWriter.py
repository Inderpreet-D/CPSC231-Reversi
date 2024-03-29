#This file contains methods for writing a string to a point in the window and
#for clearing a small section of the window
import Constants

#Goes to a postion without drawing a line
#Params: x, The x position to go to
#        y, The y position to go to
#Returns: None
def goto(x, y):
    t = Constants.TURTLE
    t.up()
    t.goto(x, y)
    t.down()

#Writes a message at the current position
#Params: message, The message to write
#Returns: None
#Notes: Font will be left-justified, bold, Arial in size 20
def write(message):
    t = Constants.TURTLE
    t.write(message, False, "left", ("Arial", 20, "bold"))

#Draws a white box at a location
#Params: x, The x coordinate of the location
#        y, The y coordinate of the location
#Returns: None
#Notes: The bax drawn will be 75x75 and will be all white
def clearArea(x, y):
    t = Constants.TURTLE
    t.up()
    t.fillcolor("White")

    #Draw a filled box
    t.begin_fill()
    for i in range(4):
        t.forward(75)
        t.right(90)
    t.end_fill()

    t.down()

#Writes the current score to the screen
#Params: black, Black's current score
#        white, White's current score
#Returns: None
def writeScore(black, white):
    #Store the starting position so the turtle can return there later
    starting_X, starting_y = Constants.TURTLE.pos()

    #Go to Black's area and draw their score
    goto(Constants.BLACK_SCORE_X, Constants.BLACK_SCORE_Y)
    clearArea(Constants.BLACK_SCORE_X, Constants.BLACK_SCORE_Y)
    write("BLACK\n    " + str(black))

    #Go to White's area and draw their score
    goto(Constants.WHITE_SCORE_X, Constants.WHITE_SCORE_Y)
    clearArea(Constants.WHITE_SCORE_X, Constants.WHITE_SCORE_Y)
    write("WHITE\n    " + str(white))

    #Return to starting position
    goto(starting_X, starting_y)

#Writes a message to the bottom of the screen
#Params: message, The message to write
#Returns: None
def writeMessage(message):
    #Store starting location for later use
    starting_X, starting_y = Constants.TURTLE.pos()

    #Move to message are and display message
    goto(Constants.MESSAGE_X, Constants.MESSAGE_Y)
    write(message)

    #Return to starting area
    goto(starting_X, starting_y)
