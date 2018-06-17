import random

min = 1
max = 6
roll_again = True

while roll_again:
	rand = random.randint(min, max)
	print("Dice rolled!\n\nYou rolled a " + str(rand) + "\n\n\nWould you like to roll again? (Y/N)\n")
	answer = input().upper()[:1]
	
	if answer == "Y":
		continue
	elif answer == "N" or answer != "Y":
		roll_again = False
		break