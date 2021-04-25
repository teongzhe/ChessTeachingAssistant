import tkinter

class ChessBoard:
	def __init__(self, canvas, state):
		self.canvas = canvas
		self.state = state

		# Compute margin and board size
		self.BOARD_MARGIN = 0.1 * self.state["canvas_size"]
		self.BOARD_SIZE = 0.8 * self.state["canvas_size"]

		# Prepare variables to store objects when drawing boards and pieces
		self.chess_board_objects = list()
		self.chess_pieces_objects = list()

		self.initialize_chess_board()
	

	def initialize_chess_board(self):
		# Create variable to store position of pieces
		self.state['position'] = list()

		# Clear chess board and chess pieces
		for object in self.chess_board_objects:
			self.canvas.delete(object)

		# Call functions to draw the chess board
		if self.state["chess_type"] == "CHESS":
			self.draw_chess_board()
		elif self.state["chess_type"] == "XIANGQI":
			self.draw_xiangqi_board()

		# Bind left mouse button events
		self.canvas.bind('<Button-1>', self.lmb_callback);


	def draw_chess_board(self):
		self.set_board_xy_array_size(8,8)
		self.CELL_SIZE = self.BOARD_SIZE / self.state["chessboard_x_array"]
		self.TEXT_MARGIN = 10
		self.state['chess_piece_size'] = int(0.8 * self.CELL_SIZE)

		self.state['board_x_start'] = self.BOARD_MARGIN
		self.state['board_x_end'] = self.BOARD_MARGIN + self.BOARD_SIZE
		self.state['board_y_start'] = self.BOARD_MARGIN
		self.state['board_y_end'] = self.BOARD_MARGIN + self.BOARD_SIZE

		# Allocate arrays for storing position of pieces
		for i in range(self.state['chessboard_x_array']):
			self.state['position'].append(list())
			for j in range(self.state['chessboard_y_array']):
				self.state['position'][-1].append('')

		# Allocate arrays for storing objects used to draw the pieces
		self.chess_pieces_objects = list()
		for i in range(self.state['chessboard_x_array']):
			self.chess_pieces_objects.append(list())
			for j in range(self.state['chessboard_y_array']):
				self.chess_pieces_objects[-1].append('')

		# Draw black and white squares
		for i in range(self.state["chessboard_x_array"]):
			for j in range(self.state["chessboard_y_array"]):
				cell_color = "white" if (i+j)%2 == 0 else "black"
				x = self.BOARD_MARGIN + i * self.CELL_SIZE
				y = self.BOARD_MARGIN + j * self.CELL_SIZE
				self.chess_board_objects.append(self.canvas.create_rectangle(x, y, x+self.CELL_SIZE, y+self.CELL_SIZE, fill=cell_color))
		
		# Insert alphabets and numbers for notation
		alphabets = ('a','b','c','d','e','f','g','h')
		for i in range(self.state["chessboard_x_array"]):
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE + self.TEXT_MARGIN, text=alphabets[i], font=12))
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN - self.TEXT_MARGIN, self.BOARD_MARGIN + self.BOARD_SIZE - (i+0.5)*self.CELL_SIZE, text=i+1, font=12))

			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, self.BOARD_MARGIN - self.TEXT_MARGIN, text=alphabets[i], font=12, angle=180))
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + self.BOARD_SIZE + self.TEXT_MARGIN, self.BOARD_MARGIN + self.BOARD_SIZE - (i+0.5)*self.CELL_SIZE, text=i+1, font=12, angle=180))
		
		self.state['center'] = list()
		for i in range(self.state['chessboard_x_array']):
			temp = list()
			for j in range(self.state['chessboard_y_array']):
				temp.append((int((i+0.5)*self.CELL_SIZE + self.BOARD_MARGIN), int((j+0.5)*self.CELL_SIZE + self.BOARD_MARGIN)))
			self.state['center'].append(tuple(temp))



	def draw_xiangqi_board(self):
		self.set_board_xy_array_size(9, 10)
		self.CELL_SIZE = self.BOARD_SIZE / self.state["chessboard_y_array"]
		self.TEXT_MARGIN = 0
		self.LINEWIDTH = 2
		self.state['chess_piece_size'] = int(0.8 * self.CELL_SIZE)

		self.state['board_x_start'] = self.BOARD_MARGIN + self.CELL_SIZE - self.state['chess_piece_size']
		self.state['board_x_end'] = self.BOARD_MARGIN + self.BOARD_SIZE - self.CELL_SIZE + self.state['chess_piece_size']
		self.state['board_y_start'] = self.BOARD_MARGIN + 0.5*self.CELL_SIZE - self.state['chess_piece_size']
		self.state['board_y_end'] = self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE + self.state['chess_piece_size']


		# Draw horizontal lines
		for i in range(self.state["chessboard_y_array"]):
			self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + self.CELL_SIZE - 0.5*self.LINEWIDTH, self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - self.CELL_SIZE + 0.5*self.LINEWIDTH, self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, width=self.LINEWIDTH))

		# Draw vertical lines
		for i in range(self.state["chessboard_x_array"]):
			if i == 0 or i == self.state["chessboard_x_array"]-1:
				self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.CELL_SIZE, self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE, width=self.LINEWIDTH))
			else:
				self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.CELL_SIZE, self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - 0.5*self.CELL_SIZE, width=self.LINEWIDTH))
				self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + 0.5*self.CELL_SIZE, self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE, width=self.LINEWIDTH))
		
		# Draw top 'X'
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + 2.5*self.CELL_SIZE, width=self.LINEWIDTH))
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + 2.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.CELL_SIZE, width=self.LINEWIDTH))

		# Draw bottom 'X'
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 2.5*self.CELL_SIZE, width=self.LINEWIDTH))
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 2.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE, width=self.LINEWIDTH))

		# Add numbers
		for i in range(self.state['chessboard_x_array']):
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + (i+1)*self.CELL_SIZE, self.state['board_y_start'] - self.TEXT_MARGIN, text=i+1, font=12, angle=180))
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + self.BOARD_SIZE - (i+1)*self.CELL_SIZE, self.state['board_y_end'] + self.TEXT_MARGIN, text=i+1, font=12))

		# Get center of chess pieces
		self.state['center'] = list()
		for i in range(self.state['chessboard_x_array']):
			temp = list()
			for j in range(self.state['chessboard_y_array']):
				temp.append((int((i+1)*self.CELL_SIZE + self.BOARD_MARGIN), int((j+0.5)*self.CELL_SIZE + self.BOARD_MARGIN)))
			self.state['center'].append(tuple(temp))



	def lmb_callback(self, event):
		# Handle events within the chessboard
		if event.x > self.state['board_x_start'] and event.x < self.state['board_x_end'] and event.y > self.state['board_y_start'] and event.y < self.state['board_y_end']:
			# Check if game is ongoing
			if self.state['game_is_ongoing']:
				print('Not implemented yet')
			# When game is not ongoing
			else:
				x = int((event.x - self.state['board_x_start']) / self.CELL_SIZE)
				y = int((event.y - self.state['board_y_start']) / self.CELL_SIZE)

				self.change_pieces_on_board(x, y)


	def set_board_xy_array_size(self, x, y):
		self.state['chessboard_x_array'] = x
		self.state['chessboard_y_array'] = y

	def change_pieces_on_board(self, x, y):
		# Check if any piece exists on the selected box
		if self.state['position'][x][y] != '':
			self.canvas.delete(self.chess_pieces_objects[x][y])
			self.state['position'][x][y] = ''
			self.chess_pieces_objects[x][y] = ''
		
		# Add piece
		if self.state['selected_piece_to_add_to_board'] != 'remove':
			self.state['position'][x][y] = self.state['selected_piece_to_add_to_board']

			img = self.state['img'][self.state['chess_type']][self.state['selected_piece_to_add_to_board']]
			self.chess_pieces_objects[x][y] = self.canvas.create_image(self.state['center'][x][y], image = img)


	def clear_pieces_from_board(self):
		for x in range(self.state['chessboard_x_array']):
			for y in range(self.state['chessboard_y_array']):
				self.canvas.delete(self.chess_pieces_objects[x][y])
				self.state['position'][x][y] = ''
				self.chess_pieces_objects[x][y] = ''
