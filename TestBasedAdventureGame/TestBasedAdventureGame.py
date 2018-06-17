import random
import msvcrt
import os

doors_number = 4 # number of doors given - max is 4 as only 4 directions
doors = [] # randomly generated directions
temp_dirs = [] # reduce repeated directions
msg = "" # message variable
doors_opened = 0 # tracking
info_made = False # used for refreshing info
desc_count = 6 # hard limit since desc

# keys = translation of arrow keys to direction
directions = {
	"H":("Up", "infront of"),
	"P":("Down", "behind"),
	"K":("Left", "to the left of"),
	"M":("Right", "to the right of")
}

# (isSafe, "description")
descriptions = [
	(True, "The room is empty - spiders are building cobwebs in the corners of the room, harboring their young. You can hear the mice scuttle under the floor boards and behind the walls; it is truly desolate."),
	(False, "You found a monster!\n\nYou try to escape but manage to trip over your own shoelaces despite wearing velcro shoes and end up getting eaten alive"),
	(True, "You found a monster!\n\nYou manage to escape by dashing through it's legs and into the room behind it. You look behind to check if it is chasing you but it appears to have vanished without a cause..."),
	(True, "The room looks like a bedroom.\nIt reminds you of home and the lovely memories you cherish with the family you were once with.\n\nYou think about how you will get back to them eventually, but for now that should not be your primary focus."),
	(False, "Wow! This room is full of treasures and silverware beyond your wildest dreams! As you go to grab one of the nearby pendants, it vanishes. You wake up back where you started with an enormous headache, aching back and weak limbs."),
	(True, "The room is empty, but you can still feel an ominous presence nearby. You decide to disregard it for now as the feeling is rather weak. You suspect it's just paranormal activity - something you are not an avid believer in.")
]

intro = [
	"You wake up in the middle of a hall and see %d doors as you look around.\n" % doors_number,
	"Curiosity piques your interest, so you decide to open one hoping for answers as to where you are...\n",
]

# clears screen on terminal
def clear_screen():
	temp = None
	
	if os.name == "nt":
		temp = os.system("cls")
	elif os.name == "posix":
		temp = os.system("clear")
	del temp

# debugging
def pause():
	pause = os.system("pause")
	del pause

# gets user pressed key, returns arrow key direction or False
def get_key():
	check = ord(msvcrt.getwch())
	
	if check == 224:
		key = msvcrt.getwch()
		
		try:
			return directions[key]
		except KeyError:
			return None
	else:
		return False

# introductory screen
for text in intro:
	clear_screen()
	print(text)
	get_key()

# main
while True:
	if not info_made:
		# creation and refreshing
		temp_dirs = list(directions.values())
		doors_number = random.randint(2,4)
		msg = ""
	
	clear_screen()
	
	# create doors through random gen directions, msg is blank if first time running
	if not msg: # if message is blank
		msg = "There are doors surrounding you...\n"
		
		if doors_opened > 0:
			msg += "Doors opened: %d\n\n" % doors_opened
		else:
			msg += "\n"
		
		print(msg, end="")
		
		for i in range(doors_number):
			val = random.choice(temp_dirs) # random direction & where it will b
			dir, location = val # tuple format 
			desc = descriptions[random.randint(0, desc_count - 1)] # random description
			dir_msg = "One {} you\n".format(location) # door location from POV
			
			doors.append((dir, *desc)) # list of doors to access
			temp_dirs.remove((dir, location))
			
			msg += dir_msg
			print(dir_msg, end="")
		
		info_made = True
	else:
		print(msg, end="")
		
	print("\n\nWhich door will you take?\n")
	key_found = get_key() # directional key
	
	# check if arrow key pressed & is a direction to one of the doors listed
	# wip
	if key_found and not (key_found in temp_dirs):
		doors_opened += 1
		dir, pdir = key_found # dir, pdir - direction, perspective of it e.g. the direction to the left of you is left
		key = random.randint(0, desc_count - 1)
		isSafe, desc = descriptions[key]
		
		clear_screen()
		print("You went to the door " + pdir + " you...\n")
		get_key() # pause for a bit
		
		print(desc) # make description
		get_key()
		
		if isSafe:
			info_made = False # resets doors
		else:
			score = doors_opened * 100
			
			clear_screen()
			print("Game Over!\nDoors opened: %d\n\nTotal score: %d00" % (doors_opened))
			get_key()
			break
