import tweepy # twitter manipulation
import os # visuals
import time # time management & program pausing
import sys # basic, low-level output
import traceback # retrieving error info

# clearing screen for visuals
def clear_screen():
	cls = os.system("cls") # clears screen & assigns return code to variable to prevent visual output
	del cls # gc

# creates and updates progress bar
def update_pbar(max, value, width=10):
	if value is 0: # avoiding ZeroDivisionError
		fill_amount = 0
		bar = "-" * width
		percentage = 0
	else:
		fill_amount = int(value / (max / width)) # bar creation
		bar = "#" * fill_amount + "-" * (width - fill_amount)
		percentage = int(value / max * 100)
		
	sys.stdout.write("[%s] %s%% (%d/%d)\r" % (bar, percentage, value, max))
	sys.stdout.flush() # show text that was editted

# prerequisites - local to account, application & program
title = "Twitter Status Console"
key = "" # Consumer Key (API Key)
c_secret = "" # Consumer Secret (API Secret)
token = "" # Access Token
a_secret = "" # Access Token Secret
auth = tweepy.OAuthHandler(key, c_secret) # set up account authentication through account key & secret
auth.set_access_token(token, a_secret) # enables account to be accessed by app through app token & secret
api = tweepy.API(auth) # get user data through twitter API
iterations, statuses = [None] * 2 # instantiated for later use

# visuals
clear_screen()
color = os.system("color b") # light blue like twitter
print(title + "\n") # program title (in screen, not on window)
title = os.system("title " + title) # console title
del color # garbage collection
del title

while True:
	msg = "" # status variable
	bar_active = False # for progress bar
	
	try:
		msg = input(">>> ") # getting user input
	except (KeyboardInterrupt, EOFError):
		continue # reset loop if user tries to force an interruption through ctrl+C and whatnot
	
	cmd = msg.lower() # for command processing
	
	try:
		if len(msg) != 0: # make sure message isnt blank - if it is, reset loop
			if cmd[:4] == "help": # show help dialogue
				print("Help\n\nhelp - opens help menu\nexit - exits program\nflush number - deletes number of statuses or all if number isn't specified\nspam iterations=20 message=\"\" - tweets message, defaults to numbers, an iterative number of times, defaults to 20\ntotal - shows total number of tweets on user's timeline")
			elif cmd[:4] == "exit": # quit program
				quit()
			elif cmd[:5] == "flush": # mass delete all (or number of) statuses of user
				args = cmd.split(" ") # command argument processing
				statuses, timeline = [None] * 2
				
				if len(args) is 1:
					statuses = len(list(tweepy.Cursor(api.user_timeline).items())) # total number of statuses
					timeline = tweepy.Cursor(api.user_timeline).items() # list (had to do it twice or it wouldnt work, not sure why)
				elif len(args) >= 2:
					statuses = args[1]
					timeline = tweepy.Cursor(api.user_timeline).items(statuses)
					
					if len(statuses) is 0: # if blank message...
						raise TypeError()
					else: # not a blank message
						statuses = int(statuses) # will error out if not a number
				
				update_pbar(statuses, 0) # create progress bar
				
				# iterate through user's timeline and removes status(es)
				for i, status in enumerate(timeline):
					i += 1 # starts at 1 as opposed to 0, then increases incrementally
					
					status.destroy()
					update_pbar(statuses, i) # update progress bar
				
				print(statuses, ("status" if statuses is 1 else "statuses") + " successfully removed!")
			elif cmd[:4] == "spam": # send multiple similar statuses
				args = cmd.split(" ")[1:] # eg "spam 20 test" now becomes ["20", "test"]
				iterations, msg = [None] * 2
				
				if len(args) == 1: # only number, defaults message to blank
					iterations, msg = args[0], ""
				else:
					iterations, msg = args[:2] # get only 2 commands if more than 2
				
				if len(iterations) == 0:
					raise TypeError()
				else:
					iterations = int(iterations)
				
				update_pbar(iterations, 0) # create progress bar
				
				for i in range(iterations):
					i += 1
					body, end = [None] * 2
					
					if msg == "":
						body = i # defaults status to numbers if no message is given
					else:
						body = "%s_%d" % (msg, i)
					
					api.update_status(body) # creates status with status text as the body of it
					update_pbar(iterations, i) # updates progress bar
				
				print(iterations, ("status" if iterations is 1 else "statuses"), "successfully created!")
			elif cmd[:5] == "total": # get total number of tweets from user's timeline
				total = len(list(tweepy.Cursor(api.user_timeline).items())) # total number of statuses
				
				print("Current number of statuses:", total)
			else: # just making a status
				api.update_status(msg) # make status with text as msg contents
	except ValueError:
		e_arg = ""
		
		# to check which command was used and used the argument from that program section
		if iterations:
			e_arg = iterations
		else:
			e_arg = statuses
		
		print("Error -", e_arg, "is not a number")
	except TypeError:
		print("Error - not enough arguments (maybe you have a space at the end of your command)")
	except tweepy.TweepError as e:
		e = e.response # http error returned
		
		print("Error", e.status_code, "-", e.reason)
	except (AttributeError, Exception):
		print("Error - send traceback to developer\n\n" + traceback.format_exc())
