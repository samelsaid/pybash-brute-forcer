#! python3

# need these to pass bash and let the program reset before trying again
import subprocess
import time

# initialize some stuff


guess = []
guessCharacters = []
totalCharacters = 0

# dictionary of useable characters
passwordCharacters = {"numbers": \
                          (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), \
                      "upper": (
                          "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                          "T", "U", "V", "W", "X", "Y", "Z"), \
                      "lower": (
                          "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                          "t", "u", "v", "w", "x", "y", "z"), \
                      "symbols" : ("`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "{", \
                          "]", "}", "\\", "|", ":", ";", "\"", "'", ",", "<", ".", ">", "/", "?") \
                      }


# uses character dictionary to determine which characters to guess from
def parameterGenerator(length, legals):
    global totalCharacters
    for i in range(0, length):
        guess.append(0)

    # builds list of possible characters for this password
    for possibleList in legals:
        for possibility in passwordCharacters[possibleList]:
            guessCharacters.append(possibility)
    totalCharacters = len(guessCharacters)

# "counting" function to restart from first character when set is complete
def increment():
    global totalCharacters
    nextLetter = 1
    guess[0] += 1
    if guess[0] >= totalCharacters:
        guess[0] = 0
        good = False
        while not good:
            guess[nextLetter] += 1
            if guess[nextLetter] >= totalCharacters:
                guess[nextLetter] = 0
                nextLetter += 1
            else:
                good = True

# generates a guess string using the indexes in the "guess" list
def passwordGuesser():
    guessWord = ""

    for letter in guess:
        guessWord += str(guessCharacters[int(letter)])

    return guessWord

# sends guess to path and returns response
def shellGuesser(guess, path):
    attempt = "echo " + guess + " | " + path
    time.sleep(1) # gives time for program to exit before next attempt
    return str(subprocess.check_output(attempt, shell=True))

# for testing the program before deployment
def testGuesser(guess):
    gotIt = "Got it!" if str(guess) == "123456446" else wrongPhrase
    return gotIt


possiblesList = [] # intake for user given character names
passLength = int(input("How long is the password (set to lowest you know it can be): "))
# will only try the full length, otherwise sets length as maximum and works up to it
exactLength = True if input("Exact length? ").lower().startswith("y") else False
correct = False
pathToFile = input("Path to binary to crack (include the './' if in current directory): ")
wrongPhrase = input("Program output when password is wrong (provide an exact consistent phrase): ")

# collects info from user and generates list of acceptable characters
while True:
    possibles = input("Symbols to guess: ")
    if possibles in passwordCharacters:
        possiblesList.append(possibles)
    elif not possibles and possiblesList:
        break
    else:
        print("Not a valid option, try again")

parameterGenerator(passLength, possiblesList)

# execution code here
print("Starting Brute Force...")
starting = input("Set a manual start point? ") # incase program quit unexpectadly and not lose previous work
if starting.lower().startswith("y"):
    print("Remember to give the value based on the guess list:")
    for i in range(0, len(guess)):
        guess[i] = guessCharacters.index(input("Start position " + str(i) + " at: "))

while not correct:
    passGuess = passwordGuesser()
#    check = shellGuesser(passGuess, pathToFile)  # real check
    check = testGuesser(passGuess)  # test check; change the test password in the function above

    if wrongPhrase not in check:
        print("\nFound it:", passGuess)
        break
    print("\rTried: " + passGuess + " ... Taking a nap", end="")

    try:
        increment()
    except IndexError:
        print(f"\rSorry couldn't find the password for length {passLength} =(\nLast password was: " + passGuess)
        if exactLength == True:
            exit(404)
        else:
            print("Gonna start over with a longer password...")
            guess.append(0)
            passLength += 1
            for letter in guess:
                guess[letter] = 0
