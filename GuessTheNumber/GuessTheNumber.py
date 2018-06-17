import random

def check_input(ans):
	try:
		ans = int(ans)
		return ans
	except ValueError:
		return False

def get_diff(ans, num):
	diff = num - ans
	
	if diff < 0:
		diff = ans - num
	
	if ans == num:
		return (True, "\nCongratulations! You got the number!")
	elif diff > 0 and diff <= 3:
		return (False, "\nSo very close!")
	elif diff > 3 and diff <= 5:
		return (False, "\nNear - not far off now..")
	elif diff > 5 and diff <= 15:
		return (False, "\nWarmer...")
	elif diff > 15 and diff <= 20:
		return (False, "\nWarm.")
	elif diff > 20 and diff <= 30:
		return (False, "\nCold.")
	elif diff > 30 and diff <= 50:
		return (False, "\nColder...")
	elif diff > 50:
		return (False, "\nYikes - frozen solid!")
	else:
		return (False, "Error")

num = random.randint(1,100)
tries = 0

while True:
	answer = input("Guess the number: ")
	answer = check_input(answer)
	
	if type(answer) is int:
		won, msg = get_diff(answer, num)
		print(msg + "\n")
		
		if won is True:
			print("\nTries:", tries)
			break
		else:
			tries += 1
			continue