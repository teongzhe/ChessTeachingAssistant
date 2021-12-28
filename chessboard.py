from settings import Parameters, State
from ImgProcessor import *
from moves import MoveHandler


class ChessBoard:
	def __init__(self, canvas):
		self.canvas = canvas
		self.__InitCanvasParameters()
		self.InitChessBoard()

	def __InitCanvasParameters(self):
		Parameters().CalculateDimensionParam()
		self.canvas.config(width = Parameters().GetCanvasSize(), height = Parameters().GetCanvasSize())

		self.chessboardObjects = list()
		self.chesspiecesObjects = dict()
		self.active_square_objects = list()
		
		self.canvas.bind('<Button-1>', self.lmb_callback)


	def InitChessBoard(self):
		self.ClearPiecesFromBoard()
		for object in self.chessboardObjects:
			self.canvas.delete(object)

		if State().GetChessType() == 'Chess':
			self.DrawChessBoard()
		elif State().GetChessType() == 'XiangQi':
			self.DrawXiangQiBoard()
		self.StartingPositions()

	def ResizeCanvas(self, canvasSize):
		# Save position of current pieces
		currentPositions = dict()
		for coordinate, piece in State().GetChessPiecePositions().items():
			currentPositions[coordinate] = piece

		# Recalculate parameters
		Parameters().CalculateDimensionParam(canvasSize)
		self.canvas.config(width = canvasSize, height = canvasSize)

		# Clear all objects
		self.ClearPiecesFromBoard()
		for object in self.chessboardObjects:
			self.canvas.delete(object)
		
		# Call functions to draw the chess board
		if State().GetChessType() == 'Chess':
			self.DrawChessBoard()
		elif State().GetChessType() == 'XiangQi':
			self.DrawXiangQiBoard()
		else:
			print('Wrong "ChessType" when calling ResizeCanvas!')
			exit(1)
		
		# Add pieces to board
		for coordinate, chessPiece in currentPositions.items():
			self.AddPieceToBoard(chessPiece['PlayerColor'], chessPiece['PieceType'], coordinate)
	
	def RemoveHighlights(self):
		for object in self.active_square_objects:
			self.canvas.delete(object)
		self.active_square_objects = list()

	def AddHighlight(self, square):
		if square != 0:
			ChessType = State().GetChessType()
			linewidth = Parameters().GetHighlightLinewidth()
			color = Parameters().GetHighlightColor(ChessType)
			x,y = Parameters().GetCellCenter(ChessType, square)
			size = 0.5 * Parameters().GetCellSize(ChessType)
			length = 0.6 * size
			offset = 0.1 * linewidth

			# Top left corner
			self.active_square_objects.append(self.canvas.create_rectangle(x-size+offset, y-size+offset, x-size+length, y-size+linewidth, width=0, fill=color))
			self.active_square_objects.append(self.canvas.create_rectangle(x-size+offset, y-size+offset, x-size+linewidth, y-size+length, width=0, fill=color))

			# Top right corner
			self.active_square_objects.append(self.canvas.create_rectangle(x+size-offset, y-size+offset, x+size-length, y-size+linewidth, width=0, fill=color))
			self.active_square_objects.append(self.canvas.create_rectangle(x+size-offset, y-size+offset, x+size-linewidth, y-size+length, width=0, fill=color))

			# Bottom left corner
			self.active_square_objects.append(self.canvas.create_rectangle(x-size+offset, y+size-offset, x-size+length, y+size-linewidth, width=0, fill=color))
			self.active_square_objects.append(self.canvas.create_rectangle(x-size+offset, y+size-offset, x-size+linewidth, y+size-length, width=0, fill=color))

			# Bottom right corner
			self.active_square_objects.append(self.canvas.create_rectangle(x+size-offset, y+size-offset, x+size-length, y+size-linewidth, width=0, fill=color))
			self.active_square_objects.append(self.canvas.create_rectangle(x+size-offset, y+size-offset, x+size-linewidth, y+size-length, width=0, fill=color))



	def DrawChessBoard(self):
		ChessType = 'Chess'
		BoardMargin = Parameters().GetBoardMargin()
		BoardSize = Parameters().GetBoardSize()
		CellSize = Parameters().GetCellSize(ChessType)
		TextMargin = Parameters().GetTextMargin(ChessType)

		# Draw black and white squares
		self.chessboardObjects.append(self.canvas.create_rectangle(BoardMargin, BoardMargin, BoardMargin+BoardSize, BoardMargin+BoardSize, fill='white', width=4))
		for i in range(Parameters().GetChessBoardXArray(ChessType)):
			for j in range(Parameters().GetChessBoardYArray(ChessType)):
				cell_color = 'white' if (i+j)%2 == 0 else 'black'
				x = BoardMargin + i * CellSize
				y = BoardMargin + j * CellSize
				self.chessboardObjects.append(self.canvas.create_rectangle(x, y, x+CellSize, y+CellSize, fill=cell_color, width=0))
		
		# Insert alphabets and numbers for notation
		alphabets = ('a','b','c','d','e','f','g','h')
		for i in range(Parameters().GetChessBoardXArray(ChessType)):
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + (i+0.5)*CellSize, BoardMargin + BoardSize + TextMargin, text=alphabets[i], font=12))
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin - TextMargin, BoardMargin + BoardSize - (i+0.5)*CellSize, text=i+1, font=12))

			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + (i+0.5)*CellSize, BoardMargin - TextMargin, text=alphabets[i], font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + BoardSize + TextMargin, BoardMargin + BoardSize - (i+0.5)*CellSize, text=i+1, font=12, angle=180))

	def DrawXiangQiBoard(self):
		ChessType = 'XiangQi'
		BoardMargin = Parameters().GetBoardMargin()
		BoardSize = Parameters().GetBoardSize()
		CellSize = Parameters().GetCellSize(ChessType)
		TextMargin = Parameters().GetTextMargin(ChessType)

		BoardYStart, BoardYEnd = Parameters().GetBoardYLimits(ChessType)
		linewidth = 2
		linelength = int(0.35 * CellSize)
		offset = 2 * linewidth

		# Draw horizontal lines
		for i in range(Parameters().GetChessBoardYArray(ChessType)):
			self.chessboardObjects.append(self.canvas.create_line(
				BoardMargin + CellSize - 0.5*linewidth, BoardMargin + (i+0.5)*CellSize,
				BoardMargin - CellSize + 0.5*linewidth + BoardSize, BoardMargin + (i+0.5)*CellSize,
				width=linewidth))

		# Draw vertical lines
		for i in range(Parameters().GetChessBoardXArray(ChessType)):
			if i == 0 or i == Parameters().GetChessBoardXArray(ChessType)-1:
				self.chessboardObjects.append(self.canvas.create_line(
					BoardMargin + (i+1)*CellSize, BoardMargin + 0.5*CellSize,
					BoardMargin + (i+1)*CellSize, BoardMargin - 0.5*CellSize + BoardSize,
					width=linewidth))
			else:
				self.chessboardObjects.append(self.canvas.create_line(
					BoardMargin + (i+1)*CellSize, BoardMargin + 0.5*CellSize,
					BoardMargin + (i+1)*CellSize, BoardMargin - 0.5*CellSize + 0.5*BoardSize,
					width=linewidth))
				self.chessboardObjects.append(self.canvas.create_line(
					BoardMargin + (i+1)*CellSize, BoardMargin + 0.5*CellSize + 0.5*BoardSize,
					BoardMargin + (i+1)*CellSize, BoardMargin - 0.5*CellSize + BoardSize,
					width=linewidth))
		
		# Draw top 'X'
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + 0.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + 2.5*CellSize,
			width=linewidth))
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + 2.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + 0.5*CellSize,
			width=linewidth))

		# Draw bottom 'X'
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + BoardSize - 0.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + BoardSize - 2.5*CellSize,
			width=linewidth))
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + BoardSize - 2.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + BoardSize - 0.5*CellSize,
			width=linewidth))

		# Draw lines for 'pao' and 'bing'
		LHSCoordinates = list()
		RHSCoordinates = list()
		for i in (1,7):
			for j in (2,7):
				LHSCoordinates.append((i,j))
				RHSCoordinates.append((i,j))

		for j in (3,6):
			for i in range(2,9,2):
				LHSCoordinates.append((i,j))
			for i in range(0,7,2):
				RHSCoordinates.append((i,j))

		for coordinate in LHSCoordinates:
			x,y = Parameters().GetCellCenter(ChessType, coordinate)
			self.chessboardObjects.append(self.canvas.create_line(x-offset, y-offset, x-linelength, y-offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x-offset, y-offset, x-offset, y-linelength, width=linewidth))

			self.chessboardObjects.append(self.canvas.create_line(x-offset, y+offset, x-linelength, y+offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x-offset, y+offset, x-offset, y+linelength, width=linewidth))

		for coordinate in RHSCoordinates:
			x,y = Parameters().GetCellCenter(ChessType, coordinate)
			self.chessboardObjects.append(self.canvas.create_line(x+offset, y-offset, x+linelength, y-offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x+offset, y-offset, x+offset, y-linelength, width=linewidth))

			self.chessboardObjects.append(self.canvas.create_line(x+offset, y+offset, x+linelength, y+offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x+offset, y+offset, x+offset, y+linelength, width=linewidth))

		# Add numbers
		for i in range(Parameters().GetChessBoardXArray(ChessType)):
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + (i+1)*CellSize, BoardYStart - TextMargin, text=i+1, font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + BoardSize - (i+1)*CellSize, BoardYEnd + TextMargin, text=i+1, font=12))


	def lmb_callback(self, event):
		ChessType = State().GetChessType()
		CellSize = Parameters().GetCellSize(ChessType)
		BoardXStart, BoardXEnd = Parameters().GetBoardXLimits(ChessType)
		BoardYStart, BoardYEnd = Parameters().GetBoardYLimits(ChessType)

		# Handle events within the chessboard
		if BoardXStart < event.x < BoardXEnd and BoardYStart < event.y < BoardYEnd:
			x = int((event.x - BoardXStart) / CellSize)
			y = int((event.y - BoardYStart) / CellSize)

			# Check if x,y are allowed values
			if x < 0: x = 0
			if x >= Parameters().GetChessBoardXArray(ChessType):
				x = Parameters().GetChessBoardXArray(ChessType) - 1

			if y < 0: y = 0
			if y >= Parameters().GetChessBoardYArray(ChessType):
				y = Parameters().GetChessBoardYArray(ChessType) - 1
			
			coordinate = (x,y)
			if State().IsGameOngoing():
				MoveHandler().Process(coordinate)
			else:
				self.ChangePieceOnBoard(coordinate)


	def ChangePieceOnBoard(self, coordinate):
		self.RemovePieceFromBoard(coordinate)
		ChessPiece = State().GetSelectedPieceToAddToBoard()
		if ChessPiece != 'remove':
			PlayerColor, PieceType = ChessPiece.split('_')
			self.AddPieceToBoard(PlayerColor, PieceType, coordinate)

	def RemovePieceFromBoard(self, coordinate):
		if coordinate in State().GetChessPiecePositions():
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
			State().RemoveChessPieceFromPosition(coordinate)

	def AddPieceToBoard(self, PlayerColor, PieceType, coordinate):
		State().AddChessPieceToPosition(PlayerColor, PieceType, coordinate)
		ChessType = State().GetChessType()
		img = ImgProcessor().GetPhotoImage(ChessType, PlayerColor + '_' + PieceType)
		self.chesspiecesObjects[coordinate] = [self.canvas.create_image(Parameters().GetCellCenter(ChessType, coordinate), image=img), img]

	def ClearPiecesFromBoard(self):
		for coordinate in State().GetChessPiecePositions():
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
		State().ClearChessPiecePositions()
		State().ClearMoveList()
		self.RemoveHighlights()

	
	def StartingPositions(self):
		self.ClearPiecesFromBoard()
		ChessType = State().GetChessType()

		if ChessType == 'Chess':
			order = ('rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook')
			for i in range(len(order)):
				self.AddPieceToBoard('white', order[i], (i,7))
				self.AddPieceToBoard('white', 'pawn', (i,6))
				self.AddPieceToBoard('black', order[i], (i, 0))
				self.AddPieceToBoard('black', 'pawn', (i, 1))
		elif ChessType == 'XiangQi':
			order = ('ju', 'ma', 'xiang', 'shi', 'shuai', 'shi', 'xiang', 'ma', 'ju')
			for i in range(len(order)):
				self.AddPieceToBoard('red', order[i], (i,9))
				self.AddPieceToBoard('black', order[i], (i,0))
			for i in (1,7):
				self.AddPieceToBoard('red', 'pao', (i,7))
				self.AddPieceToBoard('black', 'pao', (i,2))
			for i in range(0,9,2):
				self.AddPieceToBoard('red', 'bing', (i,6))
				self.AddPieceToBoard('black', 'bin', (i,3))
		
		State().ClearMoveList()
		self.RemoveHighlights()
