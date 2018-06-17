import msvcrt # character input retrieval
import string # alphabetical character verification
import re # find multiple matches for characters correctly guessed
import os # visuals

# clears screen
def clear_screen():
	cls = os.system("cls")
	del cls # garbage collection

alphabet = list(string.ascii_lowercase)
guesses = [] # listed to make things easier
limit = 10 # guess limit
game_over = True # set to False when answer is reached
word = "hangman"
checksum = list(word) # listed to be used as checksum
guess = list("_" * len(word)) # fancy visuals: ____

while len(guesses) != limit:
	clear_screen()
	guess_str = " ".join(guess) # increasing fanciness(?) on visuals: _ _ _ _
	match_found = False
	
	print("Guesses:", repr(guesses)[1:-1].replace("'", ""), "\n")
	print(guess_str + "\n")
	
	char = msvcrt.getwch() # get inputted char

	if char in alphabet: # if character is a letter, check if its been guessed before
		if not (char in guesses): # if it hasnt, add it
			guesses.append(char)
		else: # if it has, warn the user that the letter has already been guessed
			print("%s has already been guessed" % char)
			
			char = msvcrt.getwch() # "press a key then get sent back to where you were" type of aesthetic
			continue
	
	for letter in checksum:
		if char == letter:
			# get letter match positions
			positions = [m.start() for m in re.finditer(char, word)]
			
			for index in positions: # had to convert to list because you cant change string characters individually
				guess[index] = char # but you can with lists
			
			match_found = True
			print("%d matches found" % len(positions))
			char = msvcrt.getwch()
			break # because we have already found all the matches needed, doing it more times is unnecessary
	
	if not match_found and char in alphabet:
		print("No matches found\n")
		char = msvcrt.getwch()
	
	if "".join(guess) == word:
		game_over = False
		break

clear_screen()
if game_over:
	print("Game over!\n\nThe word was \"%s\"" % word)
else:
	print("Congratulations!\nYou won in %d guesses!" % len(guesses))