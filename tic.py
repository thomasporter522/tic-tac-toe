
def won(taken):
	for player in taken:
		if "" in player: return True
	return False
	
def winning(r):
	winners = [{'1','2','3'},{'4','5','6'},{'7','8','9'},{'1','4','7'},{'2','5','8'},{'3','6','9'},{'1','5','9'},{'3','5','7'}]
	for winner in winners:
		if winner == r: return True
	return False
		
def compute(taken, n):
	for i in range(n):
		prefixes = set([j[0:i] for j in taken if len(j) >= i])
		for prefix in prefixes:
			if prefix not in taken:
				relevant = set([j[-1] for j in taken if (len(j) == i + 1) and j[0:i] == prefix])
				if winning(relevant): return prefix
	return None
	
def conflicting(move, propert, n):
	for i in range(n+1):
		if move[0:i] in propert: return True
	return False
	
def possible(prefix, taken, n):
	if prefix in taken: return False
	if len(prefix) == n: return True
	if len(prefix) < n:
		for i in range(1,10):
			if possible(prefix+str(i), taken, n): return True
	return False
	
def string_of(i, j, n):
	re = ""
	
	for k in range(1,n+1):
		
		vi = (i % (3**k))//(3**(k-1))
		i = i - (i % (3**k))
		vj = (j % (3**k))//(3**(k-1))
		j = j - (j % (3**k))
		
		re = str(vi*3+vj+1) + re
	
	return re	
		
def display(taken, n):
	print(taken)
	for i in range(3**n):
		#for k in range(n): if i%(3**k) == 0: print()
		row = ""
		for j in range(3**n):
			#for k in range(n): if j%(3**k) == 0: row += " "
			s = string_of(i, j, n)
			if s in taken[0]: row += "X"
			elif s in taken[1]: row += "O"
			else: row += "_"
		print(row)
	
def run(n):
	
	current = ""
	taken = [set(),set()]
	player = 0
	winner = None
	
	while winner is None:
		
		display(taken, n)
		
		if n > 1:
			if current == "": print("Move anywhere.")
			else: print("Move inside "+current+".")
		
		acceptable = False
		while not acceptable:
			move = input("Player "+str(player)+"'s move: ")
			if move == "exit": quit()
			if "0" in move: 
				print("Please use only digits 1-9.")
			elif move[0:len(current)] != current:
				print("Please move within the current area.")
			elif len(move) != n: 
				print("Please write "+str(n)+" numbers to specify your move.")
			elif conflicting(move, taken[0].union(taken[1]), n):
				print("That move resides in claimed territory.")
			else: acceptable = True
			
		additions = []
		victory = move
		while victory is not None:
			additions.append(victory)
			taken[player].add(victory)
			victory = compute(taken[player], n)
			
		#print("Territory:",taken[player])
		
		current = additions[-1]
		if len(current) == 0: winner = player
		else:
			if len(current) == 1: 
				# version 1
				current = ""
				# version 2
				if len(additions) > 1:
					current = additions[-2]
					
			if len(current) > 1: 
				current = current[:-2]+current[-1]
				
				while not possible(current, taken[0].union(taken[1]), n):
					if current == "": 
						winner = -1
						break
					else: 
						current = current[:-1]
			
		player = 1-player
		
	display(taken, n)

	if winner == -1:
		print("It's a draw!")
	else: print("Player "+str(winner)+" wins!")
		
run(3)
