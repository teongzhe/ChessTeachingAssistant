import tkinter
from PIL import Image, ImageTk
import moves

class ChessBoard:
	def __init__(self, canvas, parameters, state):
		self.canvas = canvas
		self.parameters = parameters
		self.state = state

		# Initialize measurements
		self.initialize_parameters()

		# Prepare variables to store objects when drawing boards and pieces
		self.chess_board_objects = list()
		self.chess_pieces_objects = dict()
		self.state['position'] = dict()

		# Initialize chess board
		self.initialize_chess_board()

		# Bind mouse left click
		self.canvas.bind('<Button-1>', self.lmb_callback);

	
	def initialize_parameters(self):
		# Common measurements
		board_margin = self.parameters['BOARD_MARGIN'] = 0.1 * self.parameters['CHESSBOARD_CANVAS_SIZE']
		board_size = self.parameters['BOARD_SIZE'] = 0.8 * self.parameters['CHESSBOARD_CANVAS_SIZE']


		# Chess
		self.parameters['CHESS']['CHESSBOARD_X_ARRAY'] = 8
		self.parameters['CHESS']['CHESSBOARD_Y_ARRAY'] = 8
		self.parameters['CHESS']['CELL_SIZE'] = int(board_size / 8)
		self.parameters['CHESS']['TEXT_MARGIN'] = 10
		self.parameters['CHESS']['PIECE_SIZE'] = int(0.8 * self.parameters['CHESS']['CELL_SIZE'])

		self.parameters['CHESS']['BOARD_X_START'] = self.parameters['BOARD_MARGIN']
		self.parameters['CHESS']['BOARD_X_END'] = self.parameters['BOARD_MARGIN'] + self.parameters['BOARD_SIZE']
		self.parameters['CHESS']['BOARD_Y_START'] = self.parameters['BOARD_MARGIN']
		self.parameters['CHESS']['BOARD_Y_END'] = self.parameters['BOARD_MARGIN'] + self.parameters['BOARD_SIZE']

		self.parameters['CHESS']['CENTER'] = dict()
		for i in range(self.parameters['CHESS']['CHESSBOARD_X_ARRAY']):
			for j in range(self.parameters['CHESS']['CHESSBOARD_Y_ARRAY']):
				self.parameters['CHESS']['CENTER'][(i,j)] = (int((i+0.5)*self.parameters['CHESS']['CELL_SIZE'] + self.parameters['BOARD_MARGIN']), int((j+0.5)*self.parameters['CHESS']['CELL_SIZE'] + self.parameters['BOARD_MARGIN']))


		# Xiangqi
		self.parameters['XIANGQI']['CHESSBOARD_X_ARRAY'] = 9
		self.parameters['XIANGQI']['CHESSBOARD_Y_ARRAY'] = 10
		self.parameters['XIANGQI']['CELL_SIZE'] = int(board_size / 10)
		self.parameters['XIANGQI']['TEXT_MARGIN'] = 15
		self.parameters['XIANGQI']['PIECE_SIZE'] = int(self.parameters['XIANGQI']['CELL_SIZE'])

		self.parameters['XIANGQI']['BOARD_X_START'] = self.parameters['BOARD_MARGIN'] + self.parameters['XIANGQI']['CELL_SIZE'] - 0.5*self.parameters['XIANGQI']['PIECE_SIZE']
		self.parameters['XIANGQI']['BOARD_X_END'] = self.parameters['BOARD_MARGIN'] + self.parameters['BOARD_SIZE'] - self.parameters['XIANGQI']['CELL_SIZE'] + 0.5*self.parameters['XIANGQI']['PIECE_SIZE']
		self.parameters['XIANGQI']['BOARD_Y_START'] = self.parameters['BOARD_MARGIN'] + 0.5*self.parameters['XIANGQI']['CELL_SIZE'] - 0.5*self.parameters['XIANGQI']['PIECE_SIZE']
		self.parameters['XIANGQI']['BOARD_Y_END'] = self.parameters['BOARD_MARGIN'] + self.parameters['BOARD_SIZE'] - 0.5*self.parameters['XIANGQI']['CELL_SIZE'] + 0.5*self.parameters['XIANGQI']['PIECE_SIZE']

		self.parameters['XIANGQI']['CENTER'] = dict()
		for i in range(self.parameters['XIANGQI']['CHESSBOARD_X_ARRAY']):
			for j in range(self.parameters['XIANGQI']['CHESSBOARD_Y_ARRAY']):
				self.parameters['XIANGQI']['CENTER'][(i,j)] = (int((i+1)*self.parameters['XIANGQI']['CELL_SIZE'] + self.parameters['BOARD_MARGIN']), int((j+0.5)*self.parameters['XIANGQI']['CELL_SIZE'] + self.parameters['BOARD_MARGIN']))

		# Read images
		def process_png(chess_piece, img_size):
			img = Image.open('img/' + chess_piece + '.png')

			# Scale image
			longer_side = img.size[0] if img.size[0] > img.size[1] else img.size[1]
			scaling_factor = img_size / longer_side
			scaled_size = (int(scaling_factor*img.size[0]), int(scaling_factor*img.size[1]))
			img = img.resize(scaled_size)

			return ImageTk.PhotoImage(img)
		
		for chess_type in ('CHESS', 'XIANGQI'):
			for color in self.parameters[chess_type]['PLAYER_COLORS']:
				for piece in self.parameters[chess_type]['TYPES_OF_CHESS_PIECES']:
					chess_piece = color + '_' + piece
					self.parameters[chess_type]['IMG'][chess_piece] = process_png(chess_piece, self.parameters[chess_type]['PIECE_SIZE'])


	def initialize_chess_board(self):
		# Clear chess board and chess pieces
		for object in self.chess_board_objects:
			self.canvas.delete(object)

		# Call functions to draw the chess board
		if self.state["chess_type"] == "CHESS":
			self.draw_chess_board()
		elif self.state["chess_type"] == "XIANGQI":
			self.draw_xiangqi_board()

		self.starting_positions()


	def draw_chess_board(self):
		self.set_board_xy_array_size(8,8)
		BOARD_MARGIN = self.parameters['BOARD_MARGIN']
		BOARD_SIZE = self.parameters['BOARD_SIZE']

		CELL_SIZE = self.parameters['CHESS']['CELL_SIZE']
		TEXT_MARGIN = self.parameters['CHESS']['TEXT_MARGIN']
		PIECE_SIZE = self.parameters['CHESS']['PIECE_SIZE']

		# Allocate dictionary for storing objects used to draw the pieces
		self.chess_pieces_objects = dict()

		# Draw black and white squares
		for i in range(self.state["chessboard_x_array"]):
			for j in range(self.state["chessboard_y_array"]):
				cell_color = "white" if (i+j)%2 == 0 else "black"
				x = BOARD_MARGIN + i * CELL_SIZE
				y = BOARD_MARGIN + j * CELL_SIZE
				self.chess_board_objects.append(self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill=cell_color))
		
		# Insert alphabets and numbers for notation
		alphabets = ('a','b','c','d','e','f','g','h')
		for i in range(self.state["chessboard_x_array"]):
			self.chess_board_objects.append(self.canvas.create_text(BOARD_MARGIN + (i+0.5)*CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] + TEXT_MARGIN, text=alphabets[i], font=12))
			self.chess_board_objects.append(self.canvas.create_text(BOARD_MARGIN - TEXT_MARGIN, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - (i+0.5)*CELL_SIZE, text=i+1, font=12))

			self.chess_board_objects.append(self.canvas.create_text(BOARD_MARGIN + (i+0.5)*CELL_SIZE, BOARD_MARGIN - TEXT_MARGIN, text=alphabets[i], font=12, angle=180))
			self.chess_board_objects.append(self.canvas.create_text(BOARD_MARGIN + self.parameters['BOARD_SIZE'] + TEXT_MARGIN, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - (i+0.5)*CELL_SIZE, text=i+1, font=12, angle=180))



	def draw_xiangqi_board(self):
		self.set_board_xy_array_size(9, 10)
		BOARD_MARGIN = self.parameters['BOARD_MARGIN']
		BOARD_SIZE = self.parameters['BOARD_SIZE']

		CELL_SIZE = self.parameters['XIANGQI']['CELL_SIZE']
		TEXT_MARGIN = self.parameters['XIANGQI']['TEXT_MARGIN']
		PIECE_SIZE = self.parameters['XIANGQI']['PIECE_SIZE']

		BOARD_Y_START = self.parameters['XIANGQI']['BOARD_Y_START']
		BOARD_Y_END = self.parameters['XIANGQI']['BOARD_Y_END']

		LINEWIDTH = 2
		LINELENGTH = int(0.35 * self.parameters['XIANGQI']['CELL_SIZE'])
		OFFSET = 2 * LINEWIDTH

		# Draw horizontal lines
		for i in range(self.state["chessboard_y_array"]):
			self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + CELL_SIZE - 0.5*LINEWIDTH, BOARD_MARGIN + (i+0.5)*CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - CELL_SIZE + 0.5*LINEWIDTH, BOARD_MARGIN + (i+0.5)*CELL_SIZE, width=LINEWIDTH))

		# Draw vertical lines
		for i in range(self.state["chessboard_x_array"]):
			if i == 0 or i == self.state["chessboard_x_array"]-1:
				self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - 0.5*CELL_SIZE, width=LINEWIDTH))
			else:
				self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] - 0.5*CELL_SIZE, width=LINEWIDTH))
				self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] + 0.5*CELL_SIZE, BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - 0.5*CELL_SIZE, width=LINEWIDTH))
		
		# Draw top 'X'
		self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] - CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] + CELL_SIZE, BOARD_MARGIN + 2.5*CELL_SIZE, width=LINEWIDTH))
		self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] - CELL_SIZE, BOARD_MARGIN + 2.5*CELL_SIZE, BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] + CELL_SIZE, BOARD_MARGIN + 0.5*CELL_SIZE, width=LINEWIDTH))

		# Draw bottom 'X'
		self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] - CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - 0.5*CELL_SIZE, BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] + CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - 2.5*CELL_SIZE, width=LINEWIDTH))
		self.chess_board_objects.append(self.canvas.create_line(BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] - CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - 2.5*CELL_SIZE, BOARD_MARGIN + 0.5*self.parameters['BOARD_SIZE'] + CELL_SIZE, BOARD_MARGIN + self.parameters['BOARD_SIZE'] - 0.5*CELL_SIZE, width=LINEWIDTH))

		# Draw lines for 'pao' and 'bing'
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
			x, y = self.parameters['XIANGQI']['CENTER'][coordinate]

			self.chess_board_objects.append(self.canvas.create_line(x-OFFSET, y-OFFSET, x-LINELENGTH, y-OFFSET, width=LINEWIDTH))
			self.chess_board_objects.append(self.canvas.create_line(x-OFFSET, y-OFFSET, x-OFFSET, y-LINELENGTH, width=LINEWIDTH))

			self.chess_board_objects.append(self.canvas.create_line(x-OFFSET, y+OFFSET, x-LINELENGTH, y+OFFSET, width=LINEWIDTH))
			self.chess_board_objects.append(self.canvas.create_line(x-OFFSET, y+OFFSET, x-OFFSET, y+LINELENGTH, width=LINEWIDTH))


		for coordinate in right_hand_side_coordinates:
			x, y = self.parameters['XIANGQI']['CENTER'][coordinate]

			self.chess_board_objects.append(self.canvas.create_line(x+OFFSET, y-OFFSET, x+LINELENGTH, y-OFFSET, width=LINEWIDTH))
			self.chess_board_objects.append(self.canvas.create_line(x+OFFSET, y-OFFSET, x+OFFSET, y-LINELENGTH, width=LINEWIDTH))

			self.chess_board_objects.append(self.canvas.create_line(x+OFFSET, y+OFFSET, x+LINELENGTH, y+OFFSET, width=LINEWIDTH))
			self.chess_board_objects.append(self.canvas.create_line(x+OFFSET, y+OFFSET, x+OFFSET, y+LINELENGTH, width=LINEWIDTH))

		# Add numbers
		for i in range(self.state['chessboard_x_array']):
			self.chess_board_objects.append(self.canvas.create_text(BOARD_MARGIN + (i+1)*CELL_SIZE, BOARD_Y_START - TEXT_MARGIN, text=i+1, font=12, angle=180))
			self.chess_board_objects.append(self.canvas.create_text(BOARD_MARGIN + self.parameters['BOARD_SIZE'] - (i+1)*CELL_SIZE, BOARD_Y_END + TEXT_MARGIN, text=i+1, font=12))
		


	def lmb_callback(self, event):
		CELL_SIZE = self.parameters[self.state['chess_type']]['CELL_SIZE']
		BOARD_X_START = self.parameters[self.state['chess_type']]['BOARD_X_START']
		BOARD_X_END = self.parameters[self.state['chess_type']]['BOARD_X_END']
		BOARD_Y_START = self.parameters[self.state['chess_type']]['BOARD_Y_START']
		BOARD_Y_END = self.parameters[self.state['chess_type']]['BOARD_Y_END']

		# Handle events within the chessboard
		if event.x > BOARD_X_START and event.x < BOARD_X_END and event.y > BOARD_Y_START and event.y < BOARD_Y_END:
			x = int((event.x - BOARD_X_START) / CELL_SIZE)
			y = int((event.y - BOARD_Y_START) / CELL_SIZE)
			coordinate = (x,y)

			# Check if game is ongoing
			if self.state['game_is_ongoing']:
				self.move_piece(coordinate)
			else:
				self.change_piece_on_board(coordinate)


	def set_board_xy_array_size(self, x, y):
		self.state['chessboard_x_array'] = x
		self.state['chessboard_y_array'] = y

	def change_piece_on_board(self, coordinate):
		# Check if any piece exists on the selected box
		self.remove_piece_from_board(coordinate)

		# Add piece
		if self.state['selected_piece_to_add_to_board'] != 'remove':
			self.add_piece_to_board(coordinate, self.state['selected_piece_to_add_to_board'])

	def remove_piece_from_board(self, coordinate):
		if coordinate in self.state['position']:
			self.canvas.delete(self.chess_pieces_objects[coordinate])
			self.chess_pieces_objects.pop(coordinate)
			self.state['position'].pop(coordinate)
	
	def add_piece_to_board(self, coordinate, chess_piece):
		self.state['position'][coordinate] = chess_piece

		img = self.parameters[self.state['chess_type']]['IMG'][chess_piece]
		self.chess_pieces_objects[coordinate] = self.canvas.create_image(self.parameters[self.state['chess_type']]['CENTER'][coordinate], image=img)

	def clear_pieces_from_board(self):
		for coordinate in self.state['position']:
			self.canvas.delete(self.chess_pieces_objects[coordinate])
			self.chess_pieces_objects.pop(coordinate)
		self.state['position'] = dict()

	def move_piece(self, coordinate):
		current_move = self.state['current_move']

		selected_piece = ''
		player_color, piece = '', ''
		if coordinate in self.state['position']:
			selected_piece = self.state['position'][coordinate]
			player_color, piece = selected_piece.split('_')
		
		if current_move.moved_piece == '':
			# Select chess piece at specified coordinate
			if selected_piece != '':
				if player_color != self.state['previous_player']:
					current_move.player_color = player_color
					current_move.moved_piece = piece
					current_move.start_pos = coordinate
		else:
			# Change selection to new chess piece at specified coordinate
			if player_color != self.state['previous_player'] and player_color != '':
				if selected_piece != '':
					current_move.player_color = player_color
					current_move.moved_piece = piece
					current_move.start_pos = coordinate
			# Move piece
			else:
				current_move.end_pos = coordinate
				if selected_piece != '':
					current_move.piece_taken = selected_piece
					current_move.piece_taken_pos = coordinate
					self.remove_piece_from_board(current_move.piece_taken_pos)
				
				self.remove_piece_from_board(current_move.start_pos)
				self.add_piece_to_board(current_move.end_pos, current_move.player_color + '_' + current_move.moved_piece)

				# Record move
				self.state['current_move_index'] += 1
				if (len(self.state['move_list']) > self.state['current_move_index']):
					self.state['move_list'] = self.state['move_list'][:self.state['current_move_index']]
				self.state['move_list'].append(current_move)
				self.state['current_move'] = moves.Moves()
				self.state['previous_player'] = current_move.player_color



	def take_back(self):
		# Get information
		index = self.state['current_move_index']
		if index >= 0:
			move = self.state['move_list'][index]

			# Reverse move
			self.remove_piece_from_board(move.end_pos)
			self.add_piece_to_board(move.start_pos, move.player_color + '_' + move.moved_piece)
			if move.piece_taken != '':
				self.add_piece_to_board(move.end_pos, move.piece_taken)

			# Update state
			self.state['current_move_index'] -= 1
			index = self.state['current_move_index']
			self.state['previous_player'] = self.state['move_list'][index].player_color if index >= 0 else ''

	def forward(self):
		# Get information
		index = self.state['current_move_index']
		if index < len(self.state['move_list']) - 1:
			move = self.state['move_list'][index+1]

			# Execute move
			self.remove_piece_from_board(move.start_pos)
			if move.piece_taken != '':
				self.remove_piece_from_board(move.end_pos)
			self.add_piece_to_board(move.end_pos, move.player_color + '_' + move.moved_piece)

			# Update state
			self.state['current_move_index'] += 1
			index = self.state['current_move_index']
			self.state['previous_player'] = self.state['move_list'][index].player_color



	def starting_positions(self):
		# Chess
		if self.state['chess_type'] == 'CHESS':
			order = ('rook','knight','bishop','queen','king','bishop','knight','rook')
			for i in range(len(order)):
				# Add white pieces
				self.add_piece_to_board((i,7), 'white_' + order[i])
				self.add_piece_to_board((i,6), 'white_pawn')

				# Add black pieces
				self.add_piece_to_board((i,0), 'black_' + order[i])
				self.add_piece_to_board((i,1), 'black_pawn')
		# Xiangqi
		elif self.state['chess_type'] == 'XIANGQI':
			# Add main pieces
			order = ('ju','ma','xiang','shi','shuai','shi','xiang','ma','ju')
			for i in range(len(order)):
				self.add_piece_to_board((i,9), 'red_' + order[i])
				self.add_piece_to_board((i,0), 'black_' + order[i])
			
			# Add pao
			for i in (1,7):
				self.add_piece_to_board((i,7), 'red_pao')
				self.add_piece_to_board((i,2), 'black_pao')
			
			# Add bing
			for i in range(0,9,2):
				self.add_piece_to_board((i,6), 'red_bing')
				self.add_piece_to_board((i,3), 'black_bing')
