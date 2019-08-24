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
            return truePath
        pathCopy = path[:]
        pathCopy.append(copy.knight)
        findAllPaths(copy, pathCopy, truePath)
    y = []
    for x in truePath[1:]:
        y.append(x)
    return y


    # if not moves:
    #     if not board.pawns:
    #         truePath.append(path)
    #         print(truePath)
    #         return truePath
    #     else:
    #         return []


    # if not path:
    #     path = [board.knight]
    # moves = board.findGoodMoves()
    # copy = board.copyBoard()
    # for move in moves:
    #     copy.applyMove(move)
    #     pathCopy = path[:]
    #     pathCopy.append(copy.knight)
    #     copy.printBoard()
    #     print("_______________________________________")
    #     findAllPaths(copy, pathCopy)

# def findAllPaths(board, path=[]):
# 	# moves = board.findGoodMoves()
# 	# for move in moves:
# 	# 	copy = board.copyBoard()
# 	# 	copy.applyMove(move)
# 	# 	if findPath(copy): #if there is a path
# 	# 		join = [[board.knight] + [(board.knight[0] + move[0], board.knight[1] + move[1])]+ findPath(copy)]
# 	# 		path += join
# 	# return path

class Tree:
    def __init__(self, spec):
        if type(spec) is tuple or type(spec) is list:
            self.data = spec[0]
            self.children = [Tree(subSpec) for subSpec in spec[1:]]
        else:
            self.data = spec
            self.children = []

    def printpreorder(self):
        print(self.data)
        for child in self.children:
            child.printpreorder()

class QNode:
    def __init__(self, val):
        self.val = val
        self.nxt = None

class Queue:
    def __init__(self, l=[]):
        self.head = None
        self.tail = None
        self.size = 0
        if l:
            for thing in l:
                self.push(thing)

    def push(self, value):
        self.size += 1
        if self.head:
            newNode = QNode(value)
            self.tail.nxt = newNode
            self.tail = self.tail.nxt
        else:
            newNode = QNode(value)
            self.head = newNode
            self.tail = newNode

    def peek(self):
        if self.head:
            return self.head.val

    def pop(self):
        if self.head:
            self.size -= 1
            val = self.head.val
            self.head = self.head.nxt
            return val

# def BFS(tree):
#     q = Queue()
#     q.push(tree.data)
#     while q.size > 0:
#         x = q.pop()
#         print(x.data)
#         if type(x) is not tuple:
#             q.push(x.children)
#             print(q.size)


Tfile = [('CSE1010/', None), [('Section 1', None), [('HWs/', None),
[('hw1.doc', 5)], [('hw2.doc', 15)]], [('LABs/', None), [('lab1.py', 7)],
[('lab2.py', 10)], [('lab3.py', 10)]]], [('Section 2', None),
[('HWs/', None), [('hw1.doc', 5)], [('hw2.doc', 18)]], [('LABs/', None),
[('lab1.py', 6)], [('lab2.py', 10)], [('lab3.py', 14)]]]]
treeFile = Tree(Tfile)
# # treeFile.printpreorder()
# BFS(treeFile)
bb = Board([(1, 1), (0, 3), (1, 5), (2, 3), (2, 7), (3, 5)])
print(findAllPaths(bb))
