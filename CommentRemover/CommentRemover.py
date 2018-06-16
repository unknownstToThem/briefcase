import sys
import os

file = sys.argv[1]

# if file exists and is a python script
if os.path.isfile(file):
	if file.endswith(".py"):
		with open(file, "r+") as f: # opens file
			body = ""
			
			for i, line in enumerate(f.readlines()): # iterate through lines of script
				i += 1
				
				found_line = line.find("#")
				
				if found_line == -1: # if cannot find comment, write line and skip to next line
					body += line
				else: # if comment found, process text then write it
					comment_pos = found_line
					
					edit_text = line[:comment_pos]
					
					if comment_pos != 0:
						edit_text += "\n"
					
					body += edit_text
			
			f.seek(0)
			f.truncate()
			f.write(body)
	else:
		print("TypeError: File must be a \".py\" script")
