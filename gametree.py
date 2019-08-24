# Here is the board class; it has two attributes, knight and pawns; each piece is a pair of numbers between 0 and 7
class Board:
	def __init__(self, pieces):
		self.knight = pieces[0]
		self.pawns = pieces[1:]

	# prints board as 8 strings, 1 per line, with optional heading
	def printBoard(self, heading=""):
		if (heading):
			print(heading)
		board = [" - - - - - - - -"]*8
		(x,y) = self.knight
		row = board[x]
		board[x] = row[0:2*y+1] + "X" + row[2*y+2:]
		for (x,y) in self.pawns:
			row = board[x]
			board[x] = row[0:2*y+1] + "o" + row[2*y+2:]
		for row in board[:]:
			print(row)

	# returns list of knight moves that will eat a pawn, if any
	def findGoodMoves(self):
		(x0, y0) = self.knight
		moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
		goodMoves = []
		for (x, y) in moves:
			(x1, y1) = (x0 + x, y0 + y)
			#print ("trying move ", x, y)
			if (x1, y1) in self.pawns:
				goodMoves += [(x, y)]
		return goodMoves

	# returns a new board that's a copy of this one
	def copyBoard(self):
		newBoard = Board([self.knight]+self.pawns)
		return newBoard

	#given a board and a move, compute the next board
	def applyMove(self, move):
		(x0, y0) = self.knight
		(x, y) = move
		if ((x0 + x) >= 0 and (y0 + y) >= 0) and ((x0 + x) < 8 and (y0 + y) < 8):
			self.knight = (x0 + x, y0 + y)
			if self.knight in self.pawns:
				self.pawns.remove(self.knight)
			return True
		else:
			return False

	## Part 1
	def printGoodMovesBoard(self):
		good = self.findGoodMoves()
		for x in good:
			board = self.copyBoard()
			board.applyMove(x)
			head = (self.knight[0] + x[0], self.knight[1] + x[1])
			board.printBoard("Board with move " + str(head))

	def printAllMovesBoard(self):
		moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
		for x in moves:
			head = (self.knight[0] + x[0], self.knight[1] + x[1])
			board = self.copyBoard()
			if board.applyMove(x):
				board.printBoard("Board with move " + str(head))
			else:
				print("Invalid move:", str(head))

## Part 2
#dfsCapture: generate the good moves possible for the current board state
	#perform a move on a copy of the board, then generate new boards that act as the copy's children
	#continue until no more moves can be made
def dfsCapture(board):
	moves = board.findGoodMoves()
	if not moves:
		if not board.pawns:
			return True
		else:
			return False
	for x in moves:
		copy = board.copyBoard()
		copy.applyMove(x)
		y = dfsCapture(copy)
		if y:
			return y
		else:
			continue
	return False

def bfsCapture(board): #passes each case as of 5:00pm, 4/8
	q = []
	q.append(board)
	k = 0
	pawns = len(board.pawns)
	while len(q) > 0:
		x = q[0]
		q.remove(q[0])
		moves = x.findGoodMoves()
		if len(moves) > 0:
			for move in moves:
				k += 1
				if k % pawns == 0:
					return True
				copy = x.copyBoard()
				copy.applyMove(move)
				q.append(copy)
	return False

## Part 3
def findPath(board, pos = None):
	if pos == None:
		pos = []
	moves = board.findGoodMoves()
	copy = board.copyBoard()
	if not moves:
		if not board.pawns:
			return pos
		else:
			return []
	for move in moves:
		copy.applyMove(move)
		# print("Position:", copy.knight)
		posCopy = pos[:]
		posCopy.append(copy.knight)
		# copy.printBoard()
		x = findPath(copy, posCopy)
		if x:
			return x
		else:
			return []


## Part 4
def findAllPaths(board, path = None, truePath = None):
    if not path:
        path = [board.knight]
    if not truePath:
        truePath = [1]
    moves = board.findGoodMoves()
    for x in moves:
        copy = board.copyBoard()
        copy.applyMove(x)
        copyMoves = copy.findGoodMoves()
        if not copyMoves and not copy.pawns:
            truePath.append(path + [copy.knight])
        pathCopy = path[:]
        pathCopy.append(copy.knight)
        findAllPaths(copy, pathCopy, truePath)
    y = []
    for x in truePath[1:]:
        y.append(x)
    return y

# bb = Board([(1, 1), (0, 3), (1, 5), (2, 3), (2, 7), (3, 5)])
# print(findPath(bb))
# print(bb.findGoodMoves())
# bb.applyMove((-1,2))
# bb.printBoard()
# print(bb.findGoodMoves())
# bb.applyMove((1,2))
# bb.printBoard()
# print(bb.findGoodMoves())
# print(findAllPaths(bb))
# [(1, 1), (2, 3), (3, 5), (2, 7), (1, 5), (0, 3)]
# [(1, 1), (0, 3), (1, 5), (2, 7), (3, 5), (2, 3)]
# [(1, 1), (0, 3), (1, 5), (2, 3), (3, 5), (2, 7)]
