#This will prompt the user for the coordinates of their first move and echo it back.
#Some logical errors include the fact that you can choose coordinates above 8 and below 0 as well as letters.
#

def get_move():
    #Prints a question
    print ("What is your first move?")

    #This prompts the user for the X coordinate
    hori = input("What is your X coordinate? ")

    #This prompts the user for the Y coordinate
    vert = input("What is your Y coordinate? ")

    #Outputs the user's coordinates in a sentence
    return ("You placed a disc on " + str(hori) + ", " + str(vert) + ".")
