import tkinter

import settings
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

		# Initialize chess board
		self.initialize_chess_board()

		# Bind mouse left click
		self.canvas.bind("<Button-1>", self.lmb_callback);


	def initialize_chess_board(self):
		# Clear chess board and chess pieces
		for object in self.chessboardObjects:
			self.canvas.delete(object)

		# Call functions to draw the chess board
		if settings.state["chess_type"] == "CHESS":
			self.draw_chess_board()
		elif settings.state["chess_type"] == "XIANGQI":
			self.draw_xiangqi_board()

		self.starting_positions()
	
	def remove_highlights(self):
		for object in self.active_square_objects:
			self.canvas.delete(object)
		self.active_square_objects = list()

	def add_highlight(self, square):
		# Highlight active square
		if square != 0:
			linewidth = settings.parameters[settings.state["chess_type"]]["HIGHLIGHT_LINEWIDTH"]
			color = settings.parameters[settings.state["chess_type"]]["HIGHLIGHT_COLOR"]
			x,y = settings.parameters[settings.state["chess_type"]]["CENTER"][square]
			size = 0.5 * settings.parameters[settings.state["chess_type"]]["CELL_SIZE"]
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
		self.set_board_xy_array_size(8,8)
		BOARD_MARGIN = settings.parameters["BOARD_MARGIN"]
		BOARD_SIZE = settings.parameters["BOARD_SIZE"]

		CELL_SIZE = settings.parameters["CHESS"]["CELL_SIZE"]
		TEXT_MARGIN = settings.parameters["CHESS"]["TEXT_MARGIN"]
		PIECE_SIZE = settings.parameters["CHESS"]["PIECE_SIZE"]

		# Allocate dictionary for storing objects used to draw the pieces
		self.chesspiecesObjects = dict()

		# Draw black and white squares
		self.chessboardObjects.append(self.canvas.create_rectangle(BOARD_MARGIN, BOARD_MARGIN, BOARD_MARGIN+BOARD_SIZE, BOARD_MARGIN+BOARD_SIZE, fill="white", width=4))
		for i in range(settings.state["chessboard_x_array"]):
			for j in range(settings.state["chessboard_y_array"]):
				cell_color = "white" if (i+j)%2 == 0 else "black"
				x = BOARD_MARGIN + i * CELL_SIZE
				y = BOARD_MARGIN + j * CELL_SIZE
				self.chessboardObjects.append(self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill=cell_color, width=0))
		
		# Insert alphabets and numbers for notation
		alphabets = ("a","b","c","d","e","f","g","h")
		for i in range(settings.state["chessboard_x_array"]):
			self.chessboardObjects.append(self.canvas.create_text(BOARD_MARGIN + (i+0.5)*CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] + TEXT_MARGIN, text=alphabets[i], font=12))
			self.chessboardObjects.append(self.canvas.create_text(BOARD_MARGIN - TEXT_MARGIN, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - (i+0.5)*CELL_SIZE, text=i+1, font=12))

			self.chessboardObjects.append(self.canvas.create_text(BOARD_MARGIN + (i+0.5)*CELL_SIZE, BOARD_MARGIN - TEXT_MARGIN, text=alphabets[i], font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(BOARD_MARGIN + settings.parameters["BOARD_SIZE"] + TEXT_MARGIN, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - (i+0.5)*CELL_SIZE, text=i+1, font=12, angle=180))



	def draw_xiangqi_board(self):
		self.set_board_xy_array_size(9, 10)
		BOARD_MARGIN = settings.parameters["BOARD_MARGIN"]
		BOARD_SIZE = settings.parameters["BOARD_SIZE"]

		CELL_SIZE = settings.parameters["XIANGQI"]["CELL_SIZE"]
		TEXT_MARGIN = settings.parameters["XIANGQI"]["TEXT_MARGIN"]
		PIECE_SIZE = settings.parameters["XIANGQI"]["PIECE_SIZE"]

		BOARD_Y_START = settings.parameters["XIANGQI"]["BOARD_Y_START"]
		BOARD_Y_END = settings.parameters["XIANGQI"]["BOARD_Y_END"]

		LINEWIDTH = 2
		LINELENGTH = int(0.35 * settings.parameters["XIANGQI"]["CELL_SIZE"])
		OFFSET = 2 * LINEWIDTH

		# Draw horizontal lines
		for i in range(settings.state["chessboard_y_array"]):
			self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + CELL_SIZE - 0.5*LINEWIDTH, BOARD_MARGIN + (i+0.5)*CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - CELL_SIZE + 0.5*LINEWIDTH, BOARD_MARGIN + (i+0.5)*CELL_SIZE, width=LINEWIDTH))

		# Draw vertical lines
		for i in range(settings.state["chessboard_x_array"]):
			if i == 0 or i == settings.state["chessboard_x_array"]-1:
				self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - 0.5*CELL_SIZE, width=LINEWIDTH))
			else:
				self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] - 0.5*CELL_SIZE, width=LINEWIDTH))
				self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] + 0.5*CELL_SIZE, BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - 0.5*CELL_SIZE, width=LINEWIDTH))
		
		# Draw top "X"
		self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] - CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] + CELL_SIZE, BOARD_MARGIN + 2.5*CELL_SIZE, width=LINEWIDTH))
		self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] - CELL_SIZE, BOARD_MARGIN + 2.5*CELL_SIZE, BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] + CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, width=LINEWIDTH))

		# Draw bottom "X"
		self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] - CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - 0.5*CELL_SIZE, BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] + CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - 2.5*CELL_SIZE, width=LINEWIDTH))
		self.chessboardObjects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] - CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - 2.5*CELL_SIZE, BOARD_MARGIN + 0.5*settings.parameters["BOARD_SIZE"] + CELL_SIZE, BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - 0.5*CELL_SIZE, width=LINEWIDTH))

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
			x, y = settings.parameters["XIANGQI"]["CENTER"][coordinate]

			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y-OFFSET, x-LINELENGTH, y-OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y-OFFSET, x-OFFSET, y-LINELENGTH, width=LINEWIDTH))

			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y+OFFSET, x-LINELENGTH, y+OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x-OFFSET, y+OFFSET, x-OFFSET, y+LINELENGTH, width=LINEWIDTH))


		for coordinate in right_hand_side_coordinates:
			x, y = settings.parameters["XIANGQI"]["CENTER"][coordinate]

			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y-OFFSET, x+LINELENGTH, y-OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y-OFFSET, x+OFFSET, y-LINELENGTH, width=LINEWIDTH))

			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y+OFFSET, x+LINELENGTH, y+OFFSET, width=LINEWIDTH))
			self.chessboardObjects.append(self.canvas.create_line(x+OFFSET, y+OFFSET, x+OFFSET, y+LINELENGTH, width=LINEWIDTH))

		# Add numbers
		for i in range(settings.state["chessboard_x_array"]):
			self.chessboardObjects.append(self.canvas.create_text(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_Y_START - TEXT_MARGIN, text=i+1, font=12, angle=180))
			self.chessboardObjects.append(self.canvas.create_text(BOARD_MARGIN + settings.parameters["BOARD_SIZE"] - (i+1)*CELL_SIZE, BOARD_Y_END + TEXT_MARGIN, text=i+1, font=12))
		


	def lmb_callback(self, event):
		CELL_SIZE = settings.parameters[settings.state["chess_type"]]["CELL_SIZE"]
		BOARD_X_START = settings.parameters[settings.state["chess_type"]]["BOARD_X_START"]
		BOARD_X_END = settings.parameters[settings.state["chess_type"]]["BOARD_X_END"]
		BOARD_Y_START = settings.parameters[settings.state["chess_type"]]["BOARD_Y_START"]
		BOARD_Y_END = settings.parameters[settings.state["chess_type"]]["BOARD_Y_END"]

		# Handle events within the chessboard
		if BOARD_X_START < event.x < BOARD_X_END and BOARD_Y_START < event.y < BOARD_Y_END:
			x = int((event.x - BOARD_X_START) / CELL_SIZE)
			y = int((event.y - BOARD_Y_START) / CELL_SIZE)

			# Check if x,y are allowed values
			if x < 0: x = 0
			if x >= settings.parameters[settings.state["chess_type"]]["CHESSBOARD_X_ARRAY"]: x = settings.parameters[settings.state["chess_type"]]["CHESSBOARD_X_ARRAY"] - 1

			if y < 0: y = 0
			if y >= settings.parameters[settings.state["chess_type"]]["CHESSBOARD_Y_ARRAY"]: y = settings.parameters[settings.state["chess_type"]]["CHESSBOARD_Y_ARRAY"] - 1
			
			coordinate = (x,y)

			# Check if game is ongoing
			if settings.state["game_is_ongoing"]:
				self.move_piece(coordinate)
			else:
				self.change_piece_on_board(coordinate)


	def set_board_xy_array_size(self, x, y):
		settings.state["chessboard_x_array"] = x
		settings.state["chessboard_y_array"] = y

	def change_piece_on_board(self, coordinate):
		# Check if any piece exists on the selected box
		self.remove_piece_from_board(coordinate)

		# Add piece
		if settings.state["selected_piece_to_add_to_board"] != "remove":
			self.add_piece_to_board(coordinate, settings.state["selected_piece_to_add_to_board"])

	def remove_piece_from_board(self, coordinate):
		if coordinate in settings.state["position"]:
			self.canvas.delete(self.chesspiecesObjects[coordinate])
			self.chesspiecesObjects.pop(coordinate)
			settings.state["position"].pop(coordinate)
	
	def add_piece_to_board(self, coordinate, chess_piece):
		settings.state["position"][coordinate] = chess_piece

		img = settings.parameters[settings.state["chess_type"]]["IMG"][chess_piece]
		self.chesspiecesObjects[coordinate] = self.canvas.create_image(settings.parameters[settings.state["chess_type"]]["CENTER"][coordinate], image=img)

	def clear_pieces_from_board(self):
		for coordinate in settings.state["position"]:
			self.canvas.delete(self.chesspiecesObjects[coordinate])
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
					if settings.state["CHESS"]["CASTLE"][castle_type]:
						current_move.disabled_castling.append(castle_type)
						settings.state["CHESS"]["CASTLE"][castle_type] = False

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
					if settings.state["CHESS"]["CASTLE"][castle_type]:
						current_move.disabled_castling.append(castle_type)
						settings.state["CHESS"]["CASTLE"][castle_type] = False

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
			elif current_move.start_piece == "white_rook" and current_move.start_pos == (7,7) and settings.state["CHESS"]["CASTLE"]["white_short"]:
				settings.state["CHESS"]["CASTLE"]["white_short"] = False
				current_move.disabled_castling.append("white_short")
				move_normally(current_move)
			elif current_move.start_piece == "white_rook" and current_move.start_pos == (0,7) and settings.state["CHESS"]["CASTLE"]["white_long"]:
				settings.state["CHESS"]["CASTLE"]["white_long"] = False
				current_move.disabled_castling.append("white_long")
				move_normally(current_move)
			elif current_move.start_piece == "black_rook" and current_move.start_pos == (7,0) and settings.state["CHESS"]["CASTLE"]["black_short"]:
				settings.state["CHESS"]["CASTLE"]["black_short"] = False
				current_move.disabled_castling.append("black_short")
				move_normally(current_move)
			elif current_move.start_piece == "black_rook" and current_move.start_pos == (0,0) and settings.state["CHESS"]["CASTLE"]["black_long"]:
				settings.state["CHESS"]["CASTLE"]["black_long"] = False
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
					settings.state["CHESS"]["CASTLE"][castle_type] = True

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
					settings.state["CHESS"]["CASTLE"][castle_type] = False

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
		if settings.state["chess_type"] == "CHESS":
			order = ("rook","knight","bishop","queen","king","bishop","knight","rook")
			for i in range(len(order)):
				# Add white pieces
				self.add_piece_to_board((i,7), "white_" + order[i])
				self.add_piece_to_board((i,6), "white_pawn")

				# Add black pieces
				self.add_piece_to_board((i,0), "black_" + order[i])
				self.add_piece_to_board((i,1), "black_pawn")
		# Xiangqi
		elif settings.state["chess_type"] == "XIANGQI":
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
