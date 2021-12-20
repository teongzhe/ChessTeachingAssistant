import settings
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
		
		self.canvas.bind("<Button-1>", self.lmb_callback)


	def InitChessBoard(self):
		self.clear_pieces_from_board()
		for object in self.chessboardObjects:
			self.canvas.delete(object)

		if State().GetChessType() == "Chess":
			self.draw_chess_board()
		elif State().GetChessType() == "XiangQi":
			self.draw_xiangqi_board()
		self.starting_positions()

	def resize_canvas(self, canvasSize):
		# Save position of current pieces
		currentPositions = dict()
		for coordinate, piece in State().GetChessPiecePositions().items():
			currentPositions[coordinate] = piece

		# Recalculate parameters
		Parameters().CalculateDimensionParam(canvasSize)
		self.canvas.config(width = canvasSize, height = canvasSize)

		# Clear all objects
		self.clear_pieces_from_board()
		for object in self.chessboardObjects:
			self.canvas.delete(object)
		
		# Call functions to draw the chess board
		if State().GetChessType() == "Chess":
			self.draw_chess_board()
		elif State().GetChessType() == "XiangQi":
			self.draw_xiangqi_board()
		
		# Add pieces to board
		for coordinate, chessPiece in currentPositions.items():
			self.add_piece_to_board(coordinate, chessPiece["PlayerColor"] + "_" + chessPiece["PieceType"])
	
	def remove_highlights(self):
		for object in self.active_square_objects:
			self.canvas.delete(object)
		self.active_square_objects = list()

	def add_highlight(self, square):
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



	def draw_chess_board(self):
		ChessType = "Chess"
		BoardMargin = Parameters().GetBoardMargin()
		BoardSize = Parameters().GetBoardSize()
		CellSize = Parameters().GetCellSize(ChessType)
		TextMargin = Parameters().GetTextMargin(ChessType)

		# Draw black and white squares
		self.chessboardObjects.append(self.canvas.create_rectangle(BoardMargin, BoardMargin, BoardMargin+BoardSize, BoardMargin+BoardSize, fill="white", width=4))
		for i in range(Parameters().GetChessboardXArray(ChessType)):
			for j in range(Parameters().GetChessboardYArray(ChessType)):
				cell_color = "white" if (i+j)%2 == 0 else "black"
				x = BoardMargin + i * CellSize
				y = BoardMargin + j * CellSize
				self.chessboardObjects.append(self.canvas.create_rectangle(x, y, x+CellSize, y+CellSize, fill=cell_color, width=0))
		
		# Insert alphabets and numbers for notation
		alphabets = ("a","b","c","d","e","f","g","h")
		for i in range(Parameters().GetChessboardXArray(ChessType)):
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + (i+0.5)*CellSize, BoardMargin + BoardSize + TextMargin, text=alphabets[i], font=12))
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin - TextMargin, BoardMargin + BoardSize - (i+0.5)*CellSize, text=i+1, font=12))

			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + (i+0.5)*CellSize, BoardMargin - TextMargin, text=alphabets[i], font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(BoardMargin + BoardSize + TextMargin, BoardMargin + BoardSize - (i+0.5)*CellSize, text=i+1, font=12, angle=180))

	def draw_xiangqi_board(self):
		ChessType = "XiangQi"
		BoardMargin = Parameters().GetBoardMargin()
		BoardSize = Parameters().GetBoardSize()
		CellSize = Parameters().GetCellSize(ChessType)
		TextMargin = Parameters().GetTextMargin(ChessType)

		BoardYStart, BoardYEnd = Parameters().GetBoardYLimits(ChessType)
		linewidth = 2
		linelength = int(0.35 * CellSize)
		offset = 2 * linewidth

		# Draw horizontal lines
		for i in range(Parameters().GetChessboardYArray(ChessType)):
			self.chessboardObjects.append(self.canvas.create_line(
				BoardMargin + CellSize - 0.5*linewidth, BoardMargin + (i+0.5)*CellSize,
				BoardMargin - CellSize + 0.5*linewidth + BoardSize, BoardMargin + (i+0.5)*CellSize,
				width=linewidth))

		# Draw vertical lines
		for i in range(Parameters().GetChessboardXArray(ChessType)):
			if i == 0 or i == Parameters().GetChessboardXArray(ChessType)-1:
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
		
		# Draw top "X"
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + 0.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + 2.5*CellSize,
			width=linewidth))
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + 2.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + 0.5*CellSize,
			width=linewidth))

		# Draw bottom "X"
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + BoardSize - 0.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + BoardSize - 2.5*CellSize,
			width=linewidth))
		self.chessboardObjects.append(self.canvas.create_line(
			BoardMargin + 0.5*BoardSize - CellSize, BoardMargin + BoardSize - 2.5*CellSize,
			BoardMargin + 0.5*BoardSize + CellSize, BoardMargin + BoardSize - 0.5*CellSize,
			width=linewidth))

		# Draw lines for "pao" and "bing"
		left_hand_side_coordinates = list()
		right_hand_side_coordinates = list()
		for i in (1,7):
			for j in (2,7):
				left_hand_side_coordinates.append((i,j))
				right_hand_side_coordinates.append((i,j))

		for j in (3,6):
			for i in range(2,9,2):
				left_hand_side_coordinates.append((i,j))
			for i in range(0,7,2):
				right_hand_side_coordinates.append((i,j))

		for coordinate in left_hand_side_coordinates:
			x,y = Parameters().GetCellCenter(ChessType, coordinate)
			self.chessboardObjects.append(self.canvas.create_line(x-offset, y-offset, x-linelength, y-offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x-offset, y-offset, x-offset, y-linelength, width=linewidth))

			self.chessboardObjects.append(self.canvas.create_line(x-offset, y+offset, x-linelength, y+offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x-offset, y+offset, x-offset, y+linelength, width=linewidth))

		for coordinate in right_hand_side_coordinates:
			x,y = Parameters().GetCellCenter(ChessType, coordinate)
			self.chessboardObjects.append(self.canvas.create_line(x+offset, y-offset, x+linelength, y-offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x+offset, y-offset, x+offset, y-linelength, width=linewidth))

			self.chessboardObjects.append(self.canvas.create_line(x+offset, y+offset, x+linelength, y+offset, width=linewidth))
			self.chessboardObjects.append(self.canvas.create_line(x+offset, y+offset, x+offset, y+linelength, width=linewidth))

		# Add numbers
		for i in range(Parameters().GetChessboardXArray(ChessType)):
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
			if x >= Parameters().GetChessboardXArray(ChessType):
				x = Parameters().GetChessboardXArray(ChessType) - 1

			if y < 0: y = 0
			if y >= Parameters().GetChessboardYArray(ChessType):
				y = Parameters().GetChessboardYArray(ChessType) - 1
			
			coordinate = (x,y)

			if State().IsGameOngoing():
				# self.move_piece(coordinate)
				MoveHandler().Process(coordinate)
			else:
				self.change_piece_on_board(coordinate)

	def change_piece_on_board(self, coordinate):
		self.remove_piece_from_board(coordinate)
		if settings.state["selected_piece_to_add_to_board"] != "remove":
			self.add_piece_to_board(coordinate, settings.state["selected_piece_to_add_to_board"])

	def RemovePieceFromBoard(self, coordinate):
		if coordinate in State().GetChessPiecePositions():
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
			State().RemoveChessPieceFromPosition(coordinate)

	def AddPieceToBoard(self, PlayerColor, PieceType, coordinate):
		State().AddChessPieceToPosition(PlayerColor, PieceType, coordinate)
		ChessType = State().GetChessType()
		img = ImgProcessor().GetPhotoImage(ChessType, PlayerColor + "_" + PieceType)
		self.chesspiecesObjects[coordinate] = [self.canvas.create_image(Parameters().GetCellCenter(ChessType, coordinate), image=img), img]

	def remove_piece_from_board(self, coordinate):
		if coordinate in State().GetChessPiecePositions():
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
			State().RemoveChessPieceFromPosition(coordinate)
	
	def add_piece_to_board(self, coordinate, ChessPiece):
		PlayerColor, PieceType = ChessPiece.split("_")
		State().AddChessPieceToPosition(PlayerColor, PieceType, coordinate)
		ChessType = State().GetChessType()
		img = ImgProcessor().GetPhotoImage(ChessType, ChessPiece)
		self.chesspiecesObjects[coordinate] = [self.canvas.create_image(Parameters().GetCellCenter(ChessType, coordinate), image=img), img]

	def clear_pieces_from_board(self):
		for coordinate in State().GetChessPiecePositions():
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
		State().ClearChessPiecePositions()
		State().ClearMoveList()
		self.remove_highlights()

	def move_piece(self, coordinate):
		CurrentMove = State().GetCurrentMove()
		CurrentMove.update(coordinate)

		# Execute move
		def move_normally(move):
			self.remove_piece_from_board(move.start_pos)
			if move.piece_taken != "":
				self.remove_piece_from_board(move.piece_taken_pos)
			self.add_piece_to_board(move.end_pos, move.end_piece)

		if CurrentMove.start_pos != 0 and CurrentMove.end_pos != 0:
			# Move king (including castling)
			if CurrentMove.start_piece == "white_king":
				# Update castling states
				for castle_type in ("white_short", "white_long"):
					if settings.state["Chess"]["CASTLE"][castle_type]:
						CurrentMove.disabled_castling.append(castle_type)
						settings.state["Chess"]["CASTLE"][castle_type] = False

				if CurrentMove.start_pos == (4,7) and CurrentMove.end_pos == (6,7):
					self.remove_piece_from_board(CurrentMove.start_pos)
					self.add_piece_to_board(CurrentMove.end_pos, CurrentMove.end_piece)
					self.remove_piece_from_board((7,7))
					self.add_piece_to_board((5,7), "white_rook")
				elif CurrentMove.start_pos == (4,7) and CurrentMove.end_pos == (2,7):
					self.remove_piece_from_board(CurrentMove.start_pos)
					self.add_piece_to_board(CurrentMove.end_pos, CurrentMove.end_piece)
					self.remove_piece_from_board((0,7))
					self.add_piece_to_board((3,7), "white_rook")
				else:
					move_normally(CurrentMove)
			elif CurrentMove.start_piece == "black_king":
				for castle_type in ("black_short", "black_long"):
					if settings.state["Chess"]["CASTLE"][castle_type]:
						CurrentMove.disabled_castling.append(castle_type)
						settings.state["Chess"]["CASTLE"][castle_type] = False

				if CurrentMove.start_pos == (4,0) and CurrentMove.end_pos == (6,0):
					self.remove_piece_from_board(CurrentMove.start_pos)
					self.add_piece_to_board(CurrentMove.end_pos, CurrentMove.end_piece)
					self.remove_piece_from_board((7,0))
					self.add_piece_to_board((5,0), "black_rook")
				elif CurrentMove.start_pos == (4,0) and CurrentMove.end_pos == (2,0):
					self.remove_piece_from_board(CurrentMove.start_pos)
					self.add_piece_to_board(CurrentMove.end_pos, CurrentMove.end_piece)
					self.remove_piece_from_board((0,0))
					self.add_piece_to_board((3,0), "black_rook")
				else:
					move_normally(CurrentMove)
			elif CurrentMove.start_piece == "white_rook" and CurrentMove.start_pos == (7,7) and settings.state["Chess"]["CASTLE"]["white_short"]:
				settings.state["Chess"]["CASTLE"]["white_short"] = False
				CurrentMove.disabled_castling.append("white_short")
				move_normally(CurrentMove)
			elif CurrentMove.start_piece == "white_rook" and CurrentMove.start_pos == (0,7) and settings.state["Chess"]["CASTLE"]["white_long"]:
				settings.state["Chess"]["CASTLE"]["white_long"] = False
				CurrentMove.disabled_castling.append("white_long")
				move_normally(CurrentMove)
			elif CurrentMove.start_piece == "black_rook" and CurrentMove.start_pos == (7,0) and settings.state["Chess"]["CASTLE"]["black_short"]:
				settings.state["Chess"]["CASTLE"]["black_short"] = False
				CurrentMove.disabled_castling.append("black_short")
				move_normally(CurrentMove)
			elif CurrentMove.start_piece == "black_rook" and CurrentMove.start_pos == (0,0) and settings.state["Chess"]["CASTLE"]["black_long"]:
				settings.state["Chess"]["CASTLE"]["black_long"] = False
				CurrentMove.disabled_castling.append("black_long")
				move_normally(CurrentMove)
				
			# Move pieces with no special moves
			else:
				move_normally(CurrentMove)
			
			State().RecordMove(CurrentMove)
		
		# Highlight active squares
		self.remove_highlights()
		self.add_highlight(CurrentMove.start_pos)
		self.add_highlight(CurrentMove.end_pos)



	def take_back(self):
		# Get information
		index = State().GetCurrentMoveIndex()
		if index >= 0:
			move = State().GetMoveList()[index]

			# Reverse move
			def take_back_normally(move):
				self.remove_piece_from_board(move.end_pos)
				self.add_piece_to_board(move.start_pos, move.start_piece)
				if move.piece_taken != "":
					self.add_piece_to_board(move.piece_taken_pos, move.piece_taken)
				for castle_type in move.disabled_castling:
					settings.state["Chess"]["CASTLE"][castle_type] = True

				self.remove_highlights()
				self.add_highlight(move.start_pos)
				self.add_highlight(move.end_pos)

			if move.start_piece == "white_king" and move.start_pos == (4,7):
				if move.end_pos == (6,7):
					self.remove_piece_from_board((5,7))
					self.add_piece_to_board((7,7), "white_rook")
				elif move.end_pos == (2,7):
					self.remove_piece_from_board((3,7))
					self.add_piece_to_board((0,7), "white_rook")
				take_back_normally(move)
			elif move.start_piece == "black_king" and move.start_pos == (4,0):
				if move.end_pos == (6,0):
					self.remove_piece_from_board((5,0))
					self.add_piece_to_board((7,0), "black_rook")
				elif move.end_pos == (2,0):
					self.remove_piece_from_board((3,0))
					self.add_piece_to_board((0,0), "black_rook")
				take_back_normally(move)
			else:
				take_back_normally(move)
			
			# Update state
			settings.state["current_move_index"] -= 1
			index = settings.state["current_move_index"]
			settings.state["previous_player"] = settings.state["move_list"][index].player_color if index >= 0 else ""

	def forward(self):
		# Get information
		index = settings.state["current_move_index"]
		if index < len(settings.state["move_list"]) - 1:
			move = settings.state["move_list"][index+1]

			# Execute move
			def forward_normally(move):
				self.remove_piece_from_board(move.start_pos)
				if move.piece_taken != "":
					self.remove_piece_from_board(move.end_pos)
				self.add_piece_to_board(move.end_pos, move.end_piece)
				for castle_type in move.disabled_castling:
					settings.state["Chess"]["CASTLE"][castle_type] = False

				# Highlight active squares
				self.remove_highlights()
				self.add_highlight(move.start_pos)
				self.add_highlight(move.end_pos)
			
			if move.start_piece == "white_king" and move.start_pos == (4,7):
				if move.end_pos == (6,7):
					self.remove_piece_from_board((7,7))
					self.add_piece_to_board((5,7), "white_rook")
				elif move.end_pos == (2,7):
					self.remove_piece_from_board((0,7))
					self.add_piece_to_board((3,7), "white_rook")
				forward_normally(move)
			elif move.start_piece == "black_king" and move.start_pos == (4,0):
				if move.end_pos == (6,0):
					self.remove_piece_from_board((7,0))
					self.add_piece_to_board((5,0), "black_rook")
				elif move.end_pos == (2,0):
					self.remove_piece_from_board((0,0))
					self.add_piece_to_board((3,0), "black_rook")
				forward_normally(move)
			else:
				forward_normally(move)
			
			# Update state
			settings.state["current_move_index"] += 1
			index = settings.state["current_move_index"]
			settings.state["previous_player"] = settings.state["move_list"][index].player_color



	def starting_positions(self):
		self.clear_pieces_from_board()

		# Chess
		if State().GetChessType() == "Chess":
			order = ("rook","knight","bishop","queen","king","bishop","knight","rook")
			for i in range(len(order)):
				# Add white pieces
				self.add_piece_to_board((i,7), "white_" + order[i])
				self.add_piece_to_board((i,6), "white_pawn")

				# Add black pieces
				self.add_piece_to_board((i,0), "black_" + order[i])
				self.add_piece_to_board((i,1), "black_pawn")
		# Xiangqi
		elif State().GetChessType() == "XiangQi":
			# Add main pieces
			order = ("ju","ma","xiang","shi","shuai","shi","xiang","ma","ju")
			for i in range(len(order)):
				self.add_piece_to_board((i,9), "red_" + order[i])
				self.add_piece_to_board((i,0), "black_" + order[i])
			
			# Add pao
			for i in (1,7):
				self.add_piece_to_board((i,7), "red_pao")
				self.add_piece_to_board((i,2), "black_pao")
			
			# Add bing
			for i in range(0,9,2):
				self.add_piece_to_board((i,6), "red_bing")
				self.add_piece_to_board((i,3), "black_bing")
		
		State().ClearMoveList()
		self.remove_highlights()
