import pygame, random, time
pygame.init()

def won(taken):
	for player in taken:
		if "" in player: return True
	return False
	
def winning(r):
	winners = [{'1','2','3'},{'4','5','6'},{'7','8','9'},{'1','4','7'},{'2','5','8'},{'3','6','9'},{'1','5','9'},{'3','5','7'}]
	for winner in winners:
		if winner.intersection(r) == winner: return True
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
		


def tic_game(n = 4):
	
	screenwidth = 1000
	width = 2*sum([3**i for i in range(n)])+3**n
	screenwidth = (screenwidth//width)*width
	SCREENSIZE = (screenwidth, screenwidth)
	BLOCKSIZE = screenwidth//width

	COLORS = {"player0":(100,0,240),"player1":(0,200,150),"empty":(20,20,20), "select":(200,200,200)}
	
	def generate_data(prefix, m):
		if m == 0: return [[prefix]]
		else: 
			pieces = [generate_data(prefix+str(i),m-1) for i in range(1,10)]
			re = []
			for i in range(3):
				for k in range(len(pieces[0])):
					row = [prefix]+pieces[i*3][k]+pieces[i*3+1][k]+pieces[i*3+2][k]+[prefix]
					re.append(row)
			return [[prefix]*(len(re[0]))]+re+[[prefix]*(len(re[0]))]
		
	def render():
		for i in range(width):
			for j in range(width):
				code = data[i][j]
				color = [k*len(code) for k in COLORS["empty"]]
				if code == current: color = COLORS["select"]
				if code in taken[0]: color = COLORS["player0"]
				if code in taken[1]: color = COLORS["player1"]

				tile = pygame.Surface((BLOCKSIZE,BLOCKSIZE))
				tile.fill(color)
				screen.blit(tile, (BLOCKSIZE*(i),BLOCKSIZE*(j)))
		pygame.display.flip()
	
	current = ""
	taken = [set(),set()]
	player = 0
	winner = None
	round_number = 0
	data = generate_data("",n)
	bot = True
	bot_visible = True
		
	screen = pygame.display.set_mode(SCREENSIZE)
	background = pygame.Surface(screen.get_size())
	background.fill((255,255,255))
	background = background.convert()
	screen.blit(background, (0, 0))
	
	mainloop = True
	
	render()
	
	while mainloop:
		
		if bot:
				
			move = current
			while len(move) < n:
				move += str(random.randint(1,9))
			
			valid = True
			if move[0:len(current)] != current: valid = False
			elif len(move) != n: valid = False
			elif conflicting(move, taken[0].union(taken[1]), n): valid = False
			
			if valid:
				additions = []
				victory = move
				while victory is not None:
					additions.append(victory)
					taken[player].add(victory)
					victory = compute(taken[player], n)
											
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
				round_number += 1
				if bot_visible: render()
		
				if winner is not None:
					if winner == -1: pygame.display.set_caption("It's a draw!")
					else: pygame.display.set_caption("Player "+str(winner)+" wins!")
					mainloop = False
				else:
					message = "Turn "+str(round_number)+". Player "+str(player)+"'s turn."
					pygame.display.set_caption(message)
		
		
		else:
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False 
				
				
					if event.type == pygame.MOUSEBUTTONUP:
						mouse_position = tuple([i//BLOCKSIZE for i in pygame.mouse.get_pos()])
						if -1 not in mouse_position:
							
							move = data[mouse_position[0]][mouse_position[1]]
							valid = True
							if move[0:len(current)] != current: valid = False
							elif len(move) != n: valid = False
							elif conflicting(move, taken[0].union(taken[1]), n): valid = False
							
							if valid:
							
								additions = []
								victory = move
								while victory is not None:
									additions.append(victory)
									taken[player].add(victory)
									victory = compute(taken[player], n)
															
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
								round_number += 1
								render()
						
								if winner is not None:
									if winner == -1: pygame.display.set_caption("It's a draw!")
									else: pygame.display.set_caption("Player "+str(winner)+" wins!")
									mainloop = False
								else:
									message = "Turn "+str(round_number)+". Player "+str(player)+"'s turn."
									pygame.display.set_caption(message)
	secondloop = True
	render()
	while secondloop:							
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				secondloop = False 
								
	pygame.quit()

if __name__ == "__main__":
	tic_game()
