import pygame, random, time
pygame.init()

def won(taken):
	for player in taken:
		if "" in player: return True
	return False
		
def compute(player_taken, all_taken, victory, n):
	winners = [{'1','2','3'},{'4','5','6'},{'7','8','9'},{'1','4','7'},{'2','5','8'},{'3','6','9'},{'1','5','9'},{'3','5','7'}]
	prefix = victory[:-1]
	
	
		
	# check if it completes a win
	for winner in winners:
		valid = True
		for i in winner:
			if prefix + i not in player_taken: valid = False
		if valid and prefix not in player_taken:
			return (prefix, False)
			
	# check if it completes a draw
	draw = True
	for i in range(1,10):
		if prefix + str(i) not in all_taken: draw = False
	if draw and prefix not in all_taken:
		return (prefix, True)
			
	return (None, False)
	
def conflicting(move, propert, n):
	for i in range(n+1):
		if move[0:i] in propert: return True
	return False
	
def possible(prefix, taken, n):
	for i in range(len(prefix)+1):
		if prefix[0:i] in taken: return False
	if len(prefix) == n:
		return True
	assert len(prefix) <= n 
	if len(prefix) < n:
		for i in range(1,10):
			assert i in [1,2,3,4,5,6,7,8,9]
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
		
def tic_game(n = 5, bot = True, bot_visible = False):
	
	screenwidth = 2000
	width = 2*sum([3**i for i in range(n)])+3**n
	screenwidth = (screenwidth//width)*width
	SCREENSIZE = (screenwidth, screenwidth)
	BLOCKSIZE = screenwidth//width

	COLORS = {"player0":(120,30,240),"player1":(10,200,180),"empty":(60,60,60), "select":(200,200,200), "draw":(70,0,0)}
	
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
		
	def render(everything = False):
		for i in range(width):
			for j in range(width):
				code = data[i][j]
				if everything or code in fresh:
					if n == 0: factor = 0
					else: factor = len(code)/n
					color = [k*factor for k in COLORS["empty"]]
					if display_hover and hover is not None and hover == code and len(code) == n and possible(code, taken_pruned[0].union(taken_pruned[1]).union(drawn_pruned), n):
						color = [COLORS["player"+str(player)][k]*hover_factor + COLORS["empty"][k]*(1-hover_factor) for k in range(3)]
					if code == current: color = COLORS["select"]
					if code in taken[0]: color = COLORS["player0"]
					if code in taken[1]: color = COLORS["player1"]
					if display_draw and draw_track:
						if code in drawn: color = COLORS["draw"]

					tile = pygame.Surface((BLOCKSIZE,BLOCKSIZE))
					tile.fill(color)
					screen.blit(tile, (BLOCKSIZE*(i),BLOCKSIZE*(j)))
		pygame.display.flip()
	
	display_draw = False
	display_hover = True
	hover_factor = 0.30
	
	draw_track = False
	prune_leaves = False
	wait_time = 0
	
	current = ""
	old_current = None
	taken = [set(),set()]
	taken_pruned = [set(),set()]
	drawn = set()
	drawn_pruned = set()
	fresh = set()
	player = 0
	winner = None
	round_number = 0
	data = generate_data("",n)
	hover = None
		
	screen = pygame.display.set_mode(SCREENSIZE)
	background = pygame.Surface(screen.get_size())
	background.fill((255,255,255))
	background = background.convert()
	screen.blit(background, (0, 0))
	
	mainloop = True
	
	start_time = None
	timing = n >= 3 and bot
	if timing:
		start_time = time.time()
		
	render(everything = True)
	
	while mainloop:
		move = None
		if bot:
			move = current
			while len(move) < n:
				nexts = [str(i) for i in range(1,10)]
				nex = random.choice(nexts)
				while not possible(move+nex, taken_pruned[0].union(taken_pruned[1]).union(drawn_pruned), n):
					nexts = [i for i in nexts if i != nex]
					nex = random.choice(nexts)
				move += nex
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False 
					
				if display_hover:
					mouse_position = tuple([i//BLOCKSIZE for i in pygame.mouse.get_pos()])
					if -1 not in mouse_position:
						old_hover = hover
						hover = data[mouse_position[0]][mouse_position[1]]
						fresh.add(hover)
						if old_hover is not None: fresh.add(old_hover)
						render()
						fresh = set()
							
				if event.type == pygame.MOUSEBUTTONUP:
					mouse_position = tuple([i//BLOCKSIZE for i in pygame.mouse.get_pos()])
					if -1 not in mouse_position:
						move = data[mouse_position[0]][mouse_position[1]]
		if move is not None:			
			valid = True
			if move[0:len(current)] != current: valid = False
			elif len(move) != n: valid = False
			elif conflicting(move, taken_pruned[0].union(taken_pruned[1]).union(drawn_pruned), n): valid = False
						
			if valid:
				if bot and wait_time > 0:
					time.sleep(wait_time)
					
				additions = []
				victory = move
				draw = False
				while victory is not None:
					if bot_visible or not bot: 
						fresh.add(victory)
					if prune_leaves: 
						if draw_track:
							drawn_pruned = {i for i in drawn_pruned if i[:len(victory)] != victory}
						taken_pruned[0] = {i for i in taken_pruned[0] if i[:len(victory)] != victory}
						taken_pruned[1] = {i for i in taken_pruned[1] if i[:len(victory)] != victory}
					if draw: 
						if draw_track:
							drawn_pruned.add(victory)
							drawn.add(victory)
					else: 
						additions.append(victory)
						taken_pruned[player].add(victory)
						taken[player].add(victory)
						
					victory, draw = compute(taken_pruned[player], taken_pruned[0].union(taken_pruned[1]).union(drawn_pruned), victory, n)
	
				old_current = current							
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
											
					while not possible(current, taken_pruned[0].union(taken_pruned[1]).union(drawn_pruned), n):
						if current == "": 
							winner = -1
							break
						else: 
							current = current[:-1]
					
				player = 1-player
				round_number += 1
				
				if bot_visible or not bot: 
					fresh.add(current)
					fresh.add(old_current)
					render()
					fresh = set()
		
				if winner is not None:
					if winner == -1: pygame.display.set_caption("It's a draw!")
					else: pygame.display.set_caption("Player "+str(winner)+" wins!")
					mainloop = False
				else:
					message = "Turn "+str(round_number)+". Player "+str(player)+"'s turn. "+current
					pygame.display.set_caption(message)
	
	if timing:
		duration = time.time() - start_time
		if duration >= 10: duration = int(duration)
		print("Took",duration,"seconds.")	
		
	secondloop = True
	render(everything = True)
	while secondloop:							
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				secondloop = False 
								
	pygame.quit()

if __name__ == "__main__":
	tic_game()
