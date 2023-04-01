#!/usr/bin/python

import random

print()
print( "-------------------------------------")
print( "Welcome to rock-paper-scissors!")
print()
print( 'Enter "r" for rock')
print( '      "p" for paper')
print( '      "s" for scissors')
print( '      "e" to end the game.')

# number of moves the computer remembers
ai_memory_length = 6

valid_responses = ['r','p','s','e']
response_strings = {
	'r': 'ROCK',
	'p': 'PAPER',
	's': 'SCISSORS',
	'e': 'END'
}
response_to_num = {
	'r': 0,
	'p': 1,
	's': 2
}
num_to_response = {
	 0:'r',
	 1:'p',
	 2:'s'
}
choice_to_winning_choice = {
	'r': 'p',
	'p': 's',
	's': 'r'
}
game_responses = valid_responses[0:3]
totals = {
	'r': 0,
	'p': 0,
	's': 0 
}
you_win = "YOU WIN this round"
i_win = "I WIN this round"

num_responses = 0
response_vec = []
response = ""
num_rounds = 0.
num_ai_wins = 0.
num_draw = 0.

def MakeTwoWayTable(history):
	mat = [[1 for x in range(3)] for x in range(3)]
	for i in range(1,(len(history))):
		thisRespNum = response_to_num[history[i]]
		lastRespNum = response_to_num[history[i-1]]
		mat[lastRespNum][thisRespNum] += 1
	return mat

def SampleFrom(vec):
	return vec[random.randint(0,len(vec)-1)]

def PickAiResponse(history,strategy,current):
	if strategy == 'random':
		return valid_responses[random.randint(0,2)]
	elif (strategy == 'twoWay'):
		tab = MakeTwoWayTable(history)
		print( tab)
		thisVec = tab[response_to_num[current]]
		maxVal = max(thisVec)
		maxInds = [i for i,j in enumerate(thisVec) if j == maxVal]
		randomResponseInt = SampleFrom(maxInds)
		return choice_to_winning_choice[num_to_response[randomResponseInt]]
	else:
		raise Exception('Unknown strategy selected.')

while response != "e":
	response = ""
	while response not in valid_responses:
		print()
		print('Enter your response:')
		print('[r]ock   [p]aper   [s]cissors   [e]nd')
		response = input("")
	print()
	print( 'You responded ' + response_strings[response] + '!')
	if response in game_responses:
		# update stats
		response_vec.append(response)
		totals[response] += 1
		num_responses += 1

		# decide current strategy
		#curr_strategy = PickStrategy(response_vec)

		# make next move
		#ai_response = 'r'
		if len(response_vec) == 0:
			ai_response = PickAiResponse('','random','')
		else:
			# whole sequence, or last few governed by ai_memory_length, whichever is shorter
			ai_response = PickAiResponse(response_vec[len(response_vec)-1-min(len(response_vec)-1,ai_memory_length):(len(response_vec)-1)],'twoWay',response_vec[len(response_vec)-2])

		# report results
		num_rounds += 1
		print( 'I responded ' + response_strings[ai_response])
		if response == ai_response:
			print( 'This round is a DRAW')
			num_draw += 1
		elif (response == 'r'):
			if ai_response == 'p':
				print( i_win)
				num_ai_wins += 1
			else:
				print( you_win)
		elif (response == 'p'):
			if ai_response == 's':
				print( i_win)
				num_ai_wins += 1
			else:
				print( you_win)
		else: # response is s
			if ai_response == 'r':
				print( i_win)
				num_ai_wins += 1
			else:
				print( you_win)
	else:
		break
	print()
	input('Press any key to continue')

print( "-------------------------------------")
print( "Thanks for playing! Here are your stats:")
print( response_vec)
print( totals)
print( 'AI won ' + str(num_ai_wins/num_rounds*100) + '% of the time')
print( 'Draws ' + str(num_draw/num_rounds*100) + '% of the time')
print( 'Player won ' + str((num_rounds - num_ai_wins - num_draw)/num_rounds*100) + '% of the time')
print( 'Bye!')
print( "-------------------------------------")
