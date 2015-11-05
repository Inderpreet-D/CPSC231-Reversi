#Running this file in the terminal will let you play the board with input from the command prompt.
#It will setup the board and place the correct piece colour based on the turn number.
#It will prompt the user for moves in the terminal and will only take a valid move so a Capital and a number.
#It will update the board and the token string based on the move.
import Constants
import TurtleMove
import ReversiGrid

#This function will take a game state and update the gamestate on the game board.
#It takes the game state, which is a 64 character string
#It returns nothing
#Author: Kyle Hinton
def stringToPiece(game_state):
	index = 0
	for y in range(len(Constants.ROW_NUMBERS)):
		for x in range(len(Constants.COLUMN_LETTERS)):
			#Get location
			x_coord = Constants.COLUMN_LETTERS[x]
			y_coord = Constants.ROW_NUMBERS[y]

			#Check each piece at the index in the game state
			piece = game_state[index]
			if piece == "B":
				TurtleMove.placePiece(x_coord, y_coord, "Black")
			elif piece == "W":
				TurtleMove.placePiece(x_coord, y_coord, "White")

			#Increment index
			index += 1

#This function will decide on the colour of the next piece based on whose turn number it is.
#The takes a counter for the turns as a parameter.
#It returns a B or a W depending on whose turn it is.
def whoseTurn(counter):
	if counter % 2 == 0:
		return "W"
	else:
		return "B"

#This function will convert a move coordinate into a string.
#It receives the parameters are a token, a move coordinate, and the turn number.
#It returns the updated string as new_token.
#For testing, you can get the index number of the changed character with move_to_string
#Author: Kyle Hinton
def stringInterpret(token, NewMove, turn):
		column = NewMove[0].upper()
		row = int(NewMove[1])

		column_IDX = (Constants.COLUMN_LETTERS.index(column))
		row_IDX = (Constants.ROW_NUMBERS.index(row))

 		#Equation for converting a move coordinate to the index number to be changed
		move_to_string = ((row_IDX * Constants.NUM_OF_ROWS) + column_IDX)

		turn_colour = whoseTurn(turn)

		new_token = token[:move_to_string] + turn_colour + token[move_to_string + 1:]

		if whoseTurn(turn) == "W":
			color = "White"
		else:
			color = "Black"

		TurtleMove.placePiece(column, row, color)

		if __name__ == "__main__":
			#TESTING TESTING TESTING
			##########################
			print("Testing")
			print("turn ", turn)
			print(column_IDX, "column_IDX") # Column index number from letters
			print(row_IDX, "row_IDX")	#Row index number from numbers
			print(column, "Column")	#Prints the Column Letter
			print(row, "Row") #Prints the Row Number
			print(token[move_to_string], ": Character at the move's index number.") #Prints the character at the index [move_to_string]
			print(move_to_string, "Index number of new move") #Takes the move and converts it to the index number for the string
			print(new_token)	#Prints the new_token with the character at index.move_to_string in place
			print()
			##########################
		return new_token	#returns the new_token, The updated move.

#Sets up the board using the pieces and reading through the string.
def setup2():
	new_token = StringInterpret(("NNNNNNNN" * 8), "D4", -2)
	new_token = StringInterpret((new_token), "E4", -1)
	new_token = StringInterpret((new_token), "D5", -1)
	new_token = StringInterpret((new_token), "E5", -2)
	for turn in range(64):
		new_token = StringInterpret((new_token), input("Move?"), turn + 1)

if __name__ == "__main__":
		TurtleMove.setup()
		setup2()
		Constants.WINDOW.exitonclick()
