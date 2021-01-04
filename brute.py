#! python3

# need these to pass bash and let the program reset before trying again
import subprocess
import time

# initialize some stuff


guess = []
guessCharacters = []
totalCharacters = 0

passwordCharacters = {"numbers": \
                          (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), \
                      "upper": (
                      "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                      "T", "U", "V", "W", "X", "Y", "Z"), \
                      "lower": (
                      "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                      "t", "u", "v", "w", "x", "y", "z") \
                      }

def parameterGenerator(length, legals, exactness=False):
    global totalCharacters
    for i in range(0, length):
        guess.append(0)

    # builds list of possible characters for this password
    for possibleList in legals:
        for possibility in passwordCharacters[possibleList]:
            guessCharacters.append(possibility)
    totalCharacters = len(guessCharacters)

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

def passwordGuesser():
    guessWord = ""

    for letter in guess:
        guessWord += str(guessCharacters[int(letter)])

    return guessWord



possiblesList = []
passLength = int(input("How long is the password: "))
# will only try the full length, otherwise sets length as maximum and works up to it
exactLength = True if input("Exact length? ").lower().startswith("y") else False
correct = False
pathToFile = input("Path to file to crack (include the './'): ")

while True:
    possibles = input("Symbols to guess: ")
    if possibles in passwordCharacters:
        possiblesList.append(possibles)
    elif not possibles and possiblesList:
        break
    else:
        print("Not a valid option, try again")

parameterGenerator(passLength, possiblesList, exactLength)

# test code here
# print("Starting Brute Force...")
# while not correct:
#     passGuess = passwordGuesser()
#     if "bex" == passGuess:
#         print("\nFound it:", passGuess)
#         break
#     print("\rTried: " + passGuess + " ... Taking a nap", end="")
#     #time.sleep(1)
#     try:
#         increment()
#     except IndexError:
#         print("\nSorry couldn't find the password =(\nLast password was: " + passGuess)
#         exit(404)

# real code here
print("Starting Brute Force...")
starting = input("Set a manual start point? ")
if starting.lower().startswith("y"):
    print("Remember to give the value based on the guess list:")
    for i in range(0, len(guess)):
        guess[i] = guessCharacters.index(input("Start position " + str(i) + " at: "))

while not correct:
    passGuess = passwordGuesser()
    attempt = "echo " + passGuess + " | " + pathToFile
    check = subprocess.check_output(attempt, shell=True)
    if "Wrong" not in str(check):
        print("\nFound it:", passGuess)
        break
    print("\rTried: " + passGuess + " ... Taking a nap", end="")
    time.sleep(1)
    try:
        increment()
    except IndexError:
        print("\nSorry couldn't find the password =(\nLast password was: " + passGuess)
        exit(404)
