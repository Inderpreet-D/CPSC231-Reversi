#Removes all instances of \n character
#Params: line, The line to remove \n from
#Returns: A string with no \n characters
def removeNewLine(line):
    new_line = ""
    for i in range(len(line)):
        if line[i] == "\n":
            #Exclude just the \n character, which counts as only one indx in the string
            new_line = line[:i] + line[i + 1:]
    return new_line

#Finds a line beginning with a specified string in a list of lines
#Params: lines, The lines to look in
#        name, What the desired line starts with
#Returns: The first line that beigns with name
def findVarLine(lines, name):
    #Go through each line from the file
    for line in lines:
        #Take out any \n characters
        stripped = removeNewLine(line)

        #Check if the variable name matches
        if stripped.startswith(name + ":"):
            #Return the string
            return stripped

#Writes a variable to variables.txt
#Params: name, The name of the variable to write
#        value, The value of the variable to write
#Returns: None
def saveVariable(name, value):
    #Open a file for reading and writing
    var_file = open("variables.txt", "r+")

    #Read each line and store it as a list element
    lines = var_file.readlines()

    #Initialize a list
    line_list = []

    #Go through lines
    for line in lines:
        #Check if we found the line we wanted to change
        if line.startswith(name + ":"):
            stripped = removeNewLine(line)
            stripped_split = stripped.split(":")
            line_list.append(stripped_split[0] + ":" + value + "\n")
        else:
            line_list.append(line)

    #Wipe the file
    open("variables.txt", "w").close()

    #Reopen the file
    var_file = open("variables.txt", "r+")

    #Go to the beginning
    var_file.seek(0)

    #Writes the list
    var_file.writelines(line_list)

    #Close the file
    var_file.close()

#Reads a variable from variables.txt
#Params: name, The name of the variable to read
#Returns: The value of the variable if found, None otherwise
def loadVariable(name):
    #Open a file for reading and writing
    var_file = open("variables.txt", "r+")

    #Read each line and store it as a list element
    lines = var_file.readlines()

    #Close the file
    var_file.close()

    #Find the line containing the variable
    found_line = findVarLine(lines, name)

    #Make sure line is valid
    if found_line != None:
        return found_line.split(":")[1]

def main():
    saveVariable("State", "N" * 64)
    print(loadVariable("State"))
    saveVariable("Move", str(4))
    print(loadVariable("Move"))

if __name__ == "__main__":
    main()
