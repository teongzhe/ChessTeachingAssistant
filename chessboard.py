import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk

import settings
from ImgProcessor import *
import moves

class ChessBoard:
	def __init__(self, canvas):
		self.canvas = canvas

		# Prepare variables to store objects when drawing boards and pieces
		self.chessboardObjects = list()
		self.chesspiecesObjects = dict()

		# Prepare to highlight active square
		self.active_square_objects = list()
		settings.state["remove_highlights"] = self.remove_highlights

		# Setup canvas parameters
		self.setup_canvas_param()

		# Initialize chess board
		self.initialize_chess_board()

		# Bind mouse left click
		self.canvas.bind("<Button-1>", self.lmb_callback)

	
	def setup_canvas_param(self, canvasSize = 700):
		# Set commonly used measurements
		self.canvas.config(width=canvasSize, height=canvasSize)
		self.__boardMargin = 0.05 * canvasSize
		self.__boardSize = 0.9 * canvasSize
		self.__cellSize = {	"Chess": self.__boardSize / 8,
							"XiangQi": self.__boardSize / 10}
		self.__pieceSize = {"Chess": 0.8 * self.__cellSize["Chess"],
							"XiangQi": 0.98 * self.__cellSize["XiangQi"]}
		self.__textMargin = { "Chess": 10, "XiangQi": 15}

		# Set number of arrays of chess board
		self.__xArray = {"Chess": 8, "XiangQi": 9}
		self.__yArray = {"Chess": 8, "XiangQi": 10}

		# Set X and Y limits for chess board
		self.__boardXLimits = {
			"Chess": (self.__boardMargin, self.__boardMargin + self.__boardSize),
			"XiangQi": (self.__boardMargin + self.__cellSize["XiangQi"] - 0.5*self.__pieceSize["XiangQi"], self.__boardMargin + self.__boardSize - self.__cellSize["XiangQi"] + 0.5*self.__pieceSize["XiangQi"])
		}
		self.__boardYLimits = {
			"Chess": (self.__boardMargin, self.__boardMargin + self.__boardSize),
			"XiangQi": (self.__boardMargin + 0.5*self.__cellSize["XiangQi"] - 0.5*self.__pieceSize["XiangQi"], self.__boardMargin + self.__boardSize - 0.5*self.__cellSize["XiangQi"] + 0.5*self.__pieceSize["XiangQi"])
		}

		# Highlight settings
		self.__highlightLinewidth = {
			"Chess": 0.1 * self.__cellSize["Chess"],
			"XiangQi": 0.1 * self.__cellSize["XiangQi"]
		}
		self.__highlightColor = {"Chess": "red", "XiangQi": "blue"}

		# Generate center of squares
		self.__center = {"Chess": dict(), "XiangQi": dict()}
		for i in range(8):
			for j in range(8):
				self.__center["Chess"][(i,j)] = ((i+0.5)*self.__cellSize["Chess"] + self.__boardMargin, (j+0.5)*self.__cellSize["Chess"] + self.__boardMargin)
		for i in range(9):
			for j in range(10):
				self.__center["XiangQi"][(i,j)] = ((i+1)*self.__cellSize["XiangQi"] + self.__boardMargin, (j+0.5)*self.__cellSize["XiangQi"] + self.__boardMargin)



	def initialize_chess_board(self):
		# Clear chess board and chess pieces
		self.clear_pieces_from_board()
		for object in self.chessboardObjects:
			self.canvas.delete(object)

		# Call functions to draw the chess board
		if settings.state["chess_type"] == "Chess":
			self.draw_chess_board()
		elif settings.state["chess_type"] == "XiangQi":
			self.draw_xiangqi_board()

		self.starting_positions()

	def resize_canvas(self, canvasSize):
		# Save position of current pieces
		currentPositions = dict()
		for coordinate, piece in settings.state["position"].items():
			currentPositions[coordinate] = piece

		# Recalculate parameters
		self.setup_canvas_param(canvasSize)

		# Clear all objects
		self.clear_pieces_from_board()
		for object in self.chessboardObjects:
			self.canvas.delete(object)
		
		# Call functions to draw the chess board
		if settings.state["chess_type"] == "Chess":
			self.draw_chess_board()
		elif settings.state["chess_type"] == "XiangQi":
			self.draw_xiangqi_board()
		
		# Add pieces to board
		for coordinate, chessPiece in currentPositions.items():
			self.add_piece_to_board(coordinate, chessPiece)
	
	def remove_highlights(self):
		for object in self.active_square_objects:
			self.canvas.delete(object)
		self.active_square_objects = list()

	def add_highlight(self, square):
		# Highlight active square
		if square != 0:
			linewidth = self.__highlightLinewidth[settings.state["chess_type"]]
			color = self.__highlightColor[settings.state["chess_type"]]
			x,y = self.__center[settings.state["chess_type"]][square]
			size = 0.5 * self.__cellSize[settings.state["chess_type"]]
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
		# Draw black and white squares
		self.chessboardObjects.append(self.canvas.create_rectangle(self.__boardMargin, self.__boardMargin, self.__boardMargin+self.__boardSize, self.__boardMargin+self.__boardSize, fill="white", width=4))
		for i in range(self.__xArray["Chess"]):
			for j in range(self.__yArray["Chess"]):
				cell_color = "white" if (i+j)%2 == 0 else "black"
				x = self.__boardMargin + i * self.__cellSize["Chess"]
				y = self.__boardMargin + j * self.__cellSize["Chess"]
				self.chessboardObjects.append(self.canvas.create_rectangle(x, y, x+self.__cellSize["Chess"], y+self.__cellSize["Chess"], fill=cell_color, width=0))
		
		# Insert alphabets and numbers for notation
		alphabets = ("a","b","c","d","e","f","g","h")
		for i in range(self.__xArray["Chess"]):
			self.chessboardObjects.append(self.canvas.create_text(self.__boardMargin + (i+0.5)*self.__cellSize["Chess"], self.__boardMargin + self.__boardSize + self.__textMargin["Chess"], text=alphabets[i], font=12))
			self.chessboardObjects.append(self.canvas.create_text(self.__boardMargin - self.__textMargin["Chess"], self.__boardMargin + self.__boardSize - (i+0.5)*self.__cellSize["Chess"], text=i+1, font=12))

			self.chessboardObjects.append(self.canvas.create_text(self.__boardMargin + (i+0.5)*self.__cellSize["Chess"], self.__boardMargin - self.__textMargin["Chess"], text=alphabets[i], font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(self.__boardMargin + self.__boardSize + self.__textMargin["Chess"], self.__boardMargin + self.__boardSize - (i+0.5)*self.__cellSize["Chess"], text=i+1, font=12, angle=180))



	def draw_xiangqi_board(self):
		BOARD_Y_START, BOARD_Y_END = self.__boardYLimits["XiangQi"]
		LINEWIDTH = 2
		LINELENGTH = int(0.35 * self.__cellSize["XiangQi"])
		OFFSET = 2 * LINEWIDTH

		# Draw horizontal lines
		for i in range(self.__yArray["XiangQi"]):
			self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + self.__cellSize["XiangQi"] - 0.5*LINEWIDTH, self.__boardMargin + (i+0.5)*self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - self.__cellSize["XiangQi"] + 0.5*LINEWIDTH, self.__boardMargin + (i+0.5)*self.__cellSize["XiangQi"], width=LINEWIDTH))

		# Draw vertical lines
		for i in range(self.__xArray["XiangQi"]):
			if i == 0 or i == self.__xArray["XiangQi"]-1:
				self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__cellSize["XiangQi"], self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - 0.5*self.__cellSize["XiangQi"], width=LINEWIDTH))
			else:
				self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__cellSize["XiangQi"], self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__boardSize - 0.5*self.__cellSize["XiangQi"], width=LINEWIDTH))
				self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__boardSize + 0.5*self.__cellSize["XiangQi"], self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - 0.5*self.__cellSize["XiangQi"], width=LINEWIDTH))
		
		# Draw top "X"
		self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + 0.5*self.__boardSize - self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__boardSize + self.__cellSize["XiangQi"], self.__boardMargin + 2.5*self.__cellSize["XiangQi"], width=LINEWIDTH))
		self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + 0.5*self.__boardSize - self.__cellSize["XiangQi"], self.__boardMargin + 2.5*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__boardSize + self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__cellSize["XiangQi"], width=LINEWIDTH))

		# Draw bottom "X"
		self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + 0.5*self.__boardSize - self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - 0.5*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__boardSize + self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - 2.5*self.__cellSize["XiangQi"], width=LINEWIDTH))
		self.chessboardObjects.append(self.canvas.create_line(self.__boardMargin + 0.5*self.__boardSize - self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - 2.5*self.__cellSize["XiangQi"], self.__boardMargin + 0.5*self.__boardSize + self.__cellSize["XiangQi"], self.__boardMargin + self.__boardSize - 0.5*self.__cellSize["XiangQi"], width=LINEWIDTH))

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
			x, y = self.__center["XiangQi"][coordinate]

			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y-OFFSET, x-LINELENGTH, y-OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y-OFFSET, x-OFFSET, y-LINELENGTH, width=LINEWIDTH))

			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y+OFFSET, x-LINELENGTH, y+OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y+OFFSET, x-OFFSET, y+LINELENGTH, width=LINEWIDTH))


		for coordinate in right_hand_side_coordinates:
			x, y = self.__center["XiangQi"][coordinate]

			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y-OFFSET, x+LINELENGTH, y-OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y-OFFSET, x+OFFSET, y-LINELENGTH, width=LINEWIDTH))

			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y+OFFSET, x+LINELENGTH, y+OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y+OFFSET, x+OFFSET, y+LINELENGTH, width=LINEWIDTH))

		# Add numbers
		for i in range(self.__xArray["XiangQi"]):
			self.chessboardObjects.append(self.canvas.create_text(self.__boardMargin + (i+1)*self.__cellSize["XiangQi"], BOARD_Y_START - self.__textMargin["XiangQi"], text=i+1, font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(self.__boardMargin + self.__boardSize - (i+1)*self.__cellSize["XiangQi"], BOARD_Y_END + self.__textMargin["XiangQi"], text=i+1, font=12))
		


	def lmb_callback(self, event):
		CELL_SIZE = self.__cellSize[settings.state["chess_type"]]
		BOARD_X_START, BOARD_X_END = self.__boardXLimits[settings.state["chess_type"]]
		BOARD_Y_START, BOARD_Y_END = self.__boardYLimits[settings.state["chess_type"]]

		# Handle events within the chessboard
		if BOARD_X_START < event.x < BOARD_X_END and BOARD_Y_START < event.y < BOARD_Y_END:
			x = int((event.x - BOARD_X_START) / CELL_SIZE)
			y = int((event.y - BOARD_Y_START) / CELL_SIZE)

			# Check if x,y are allowed values
			if x < 0: x = 0
			if x >= self.__xArray[settings.state["chess_type"]]:
				x = self.__xArray[settings.state["chess_type"]] - 1

			if y < 0: y = 0
			if y >= self.__yArray[settings.state["chess_type"]]:
				y = self.__yArray[settings.state["chess_type"]] - 1
			
			coordinate = (x,y)

			# Check if game is ongoing
			if settings.state["game_is_ongoing"]:
				self.move_piece(coordinate)
			else:
				self.change_piece_on_board(coordinate)


	def change_piece_on_board(self, coordinate):
		# Check if any piece exists on the selected box
		self.remove_piece_from_board(coordinate)

		# Add piece
		if settings.state["selected_piece_to_add_to_board"] != "remove":
			self.add_piece_to_board(coordinate, settings.state["selected_piece_to_add_to_board"])

	def remove_piece_from_board(self, coordinate):
		if coordinate in settings.state["position"]:
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
			settings.state["position"].pop(coordinate)
	
	def add_piece_to_board(self, coordinate, ChessPiece):
		settings.state["position"][coordinate] = ChessPiece
		ChessType = settings.state["chess_type"]
		img = ImgProcessor().GetPhotoImage(ChessType, ChessPiece)
		self.chesspiecesObjects[coordinate] = [self.canvas.create_image(self.__center[ChessType][coordinate], image=img), img]

	def clear_pieces_from_board(self):
		for coordinate in settings.state["position"]:
			self.canvas.delete(self.chesspiecesObjects[coordinate][0])
			self.chesspiecesObjects.pop(coordinate)
		settings.state["position"] = dict()

		settings.state["clear_move_list"]()
		settings.state["remove_highlights"]()

	def move_piece(self, coordinate):
		current_move = settings.state["current_move"]
		current_move.update(settings.state, coordinate)

		# Execute move
		def move_normally(move):
			self.remove_piece_from_board(move.start_pos)
			if move.piece_taken != "":
				self.remove_piece_from_board(move.piece_taken_pos)
			self.add_piece_to_board(move.end_pos, move.end_piece)

		if current_move.start_pos != 0 and current_move.end_pos != 0:
			# Move king (including castling)
			if current_move.start_piece == "white_king":
				# Update castling states
				for castle_type in ("white_short", "white_long"):
					if settings.state["Chess"]["CASTLE"][castle_type]:
						current_move.disabled_castling.append(castle_type)
						settings.state["Chess"]["CASTLE"][castle_type] = False

				if current_move.start_pos == (4,7) and current_move.end_pos == (6,7):
					self.remove_piece_from_board(current_move.start_pos)
					self.add_piece_to_board(current_move.end_pos, current_move.end_piece)
					self.remove_piece_from_board((7,7))
					self.add_piece_to_board((5,7), "white_rook")
				elif current_move.start_pos == (4,7) and current_move.end_pos == (2,7):
					self.remove_piece_from_board(current_move.start_pos)
					self.add_piece_to_board(current_move.end_pos, current_move.end_piece)
					self.remove_piece_from_board((0,7))
					self.add_piece_to_board((3,7), "white_rook")
				else:
					move_normally(current_move)
			elif current_move.start_piece == "black_king":
				for castle_type in ("black_short", "black_long"):
					if settings.state["Chess"]["CASTLE"][castle_type]:
						current_move.disabled_castling.append(castle_type)
						settings.state["Chess"]["CASTLE"][castle_type] = False

				if current_move.start_pos == (4,0) and current_move.end_pos == (6,0):
					self.remove_piece_from_board(current_move.start_pos)
					self.add_piece_to_board(current_move.end_pos, current_move.end_piece)
					self.remove_piece_from_board((7,0))
					self.add_piece_to_board((5,0), "black_rook")
				elif current_move.start_pos == (4,0) and current_move.end_pos == (2,0):
					self.remove_piece_from_board(current_move.start_pos)
					self.add_piece_to_board(current_move.end_pos, current_move.end_piece)
					self.remove_piece_from_board((0,0))
					self.add_piece_to_board((3,0), "black_rook")
				else:
					move_normally(current_move)
			elif current_move.start_piece == "white_rook" and current_move.start_pos == (7,7) and settings.state["Chess"]["CASTLE"]["white_short"]:
				settings.state["Chess"]["CASTLE"]["white_short"] = False
				current_move.disabled_castling.append("white_short")
				move_normally(current_move)
			elif current_move.start_piece == "white_rook" and current_move.start_pos == (0,7) and settings.state["Chess"]["CASTLE"]["white_long"]:
				settings.state["Chess"]["CASTLE"]["white_long"] = False
				current_move.disabled_castling.append("white_long")
				move_normally(current_move)
			elif current_move.start_piece == "black_rook" and current_move.start_pos == (7,0) and settings.state["Chess"]["CASTLE"]["black_short"]:
				settings.state["Chess"]["CASTLE"]["black_short"] = False
				current_move.disabled_castling.append("black_short")
				move_normally(current_move)
			elif current_move.start_piece == "black_rook" and current_move.start_pos == (0,0) and settings.state["Chess"]["CASTLE"]["black_long"]:
				settings.state["Chess"]["CASTLE"]["black_long"] = False
				current_move.disabled_castling.append("black_long")
				move_normally(current_move)
				
			# Move pieces with no special moves
			else:
				move_normally(current_move)
			
			# Record move
			settings.state["current_move_index"] += 1
			if (len(settings.state["move_list"]) > settings.state["current_move_index"]):
				settings.state["move_list"] = settings.state["move_list"][:settings.state["current_move_index"]]
			settings.state["move_list"].append(current_move)
			settings.state["current_move"] = moves.Moves()
			settings.state["previous_player"] = current_move.player_color
		
		# Highlight active squares
		settings.state["remove_highlights"]()
		self.add_highlight(current_move.start_pos)
		self.add_highlight(current_move.end_pos)



	def take_back(self):
		# Get information
		index = settings.state["current_move_index"]
		if index >= 0:
			move = settings.state["move_list"][index]

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
		if settings.state["chess_type"] == "Chess":
			order = ("rook","knight","bishop","queen","king","bishop","knight","rook")
			for i in range(len(order)):
				# Add white pieces
				self.add_piece_to_board((i,7), "white_" + order[i])
				self.add_piece_to_board((i,6), "white_pawn")

				# Add black pieces
				self.add_piece_to_board((i,0), "black_" + order[i])
				self.add_piece_to_board((i,1), "black_pawn")
		# Xiangqi
		elif settings.state["chess_type"] == "XiangQi":
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
		
		settings.state["clear_move_list"]()
		settings.state["remove_highlights"]()
