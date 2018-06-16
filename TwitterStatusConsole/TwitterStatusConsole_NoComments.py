import tweepy 
import os 
import time 
import sys 
import traceback 

def clear_screen():
	cls = os.system("cls") 
	del cls 

def update_pbar(max, value, width=10):
	if value is 0: 
		fill_amount = 0
		bar = "-" * width
		percentage = 0
	else:
		fill_amount = int(value / (max / width)) 
		bar = "
		percentage = int(value / max * 100)
		
	sys.stdout.write("[%s] %s%% (%d/%d)\r" % (bar, percentage, value, max))
	sys.stdout.flush() 

title = "Twitter Status Console"
key = "" 
c_secret = "" 
token = "" 
a_secret = "" 
auth = tweepy.OAuthHandler(key, c_secret) 
auth.set_access_token(token, a_secret) 
api = tweepy.API(auth) 
iterations, statuses = [None] * 2 

clear_screen()
color = os.system("color b") 
print(title + "\n") 
title = os.system("title " + title) 
del color 
del title

while True:
	msg = "" 
	bar_active = False 
	
	try:
		msg = input(">>> ") 
	except (KeyboardInterrupt, EOFError):
		continue 
	
	cmd = msg.lower() 
	
	try:
		if len(msg) != 0: 
			if cmd[:4] == "help": 
				print("Help\n\nhelp - opens help menu\nexit - exits program\nflush number - deletes number of statuses or all if number isn't specified\nspam iterations=20 message=\"\" - tweets message, defaults to numbers, an iterative number of times, defaults to 20\ntotal - shows total number of tweets on user's timeline")
			elif cmd[:4] == "exit": 
				quit()
			elif cmd[:5] == "flush": 
				args = cmd.split(" ") 
				statuses, timeline = [None] * 2
				
				if len(args) is 1:
					statuses = len(list(tweepy.Cursor(api.user_timeline).items())) 
					timeline = tweepy.Cursor(api.user_timeline).items() 
				elif len(args) >= 2:
					statuses = args[1]
					timeline = tweepy.Cursor(api.user_timeline).items(statuses)
					
					if len(statuses) is 0: 
						raise TypeError()
					else: 
						statuses = int(statuses) 
				
				update_pbar(statuses, 0) 
				
				
				for i, status in enumerate(timeline):
					i += 1 
					
					status.destroy()
					update_pbar(statuses, i) 
				
				print(statuses, ("status" if statuses is 1 else "statuses") + " successfully removed!")
			elif cmd[:4] == "spam": 
				args = cmd.split(" ")[1:] 
				iterations, msg = [None] * 2
				
				if len(args) == 1: 
					iterations, msg = args[0], ""
				else:
					iterations, msg = args[:2] 
				
				if len(iterations) == 0:
					raise TypeError()
				else:
					iterations = int(iterations)
				
				update_pbar(iterations, 0) 
				
				for i in range(iterations):
					i += 1
					body, end = [None] * 2
					
					if msg == "":
						body = i 
					else:
						body = "%s_%d" % (msg, i)
					
					api.update_status(body) 
					update_pbar(iterations, i) 
				
				print(iterations, ("status" if iterations is 1 else "statuses"), "successfully created!")
			elif cmd[:5] == "total": 
				total = len(list(tweepy.Cursor(api.user_timeline).items())) 
				
				print("Current number of statuses:", total)
			else: 
				api.update_status(msg) 
	except ValueError:
		e_arg = ""
		
		
		if iterations:
			e_arg = iterations
		else:
			e_arg = statuses
		
		print("Error -", e_arg, "is not a number")
	except TypeError:
		print("Error - not enough arguments (maybe you have a space at the end of your command)")
	except tweepy.TweepError as e:
		e = e.response 
		
		print("Error", e.status_code, "-", e.reason)
	except (AttributeError, Exception):
		print("Error - send traceback to developer\n\n" + traceback.format_exc())
