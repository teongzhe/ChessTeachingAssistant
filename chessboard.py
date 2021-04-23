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
		# Clear chess board and chess pieces
		for object in self.chess_board_objects:
			self.canvas.delete(object)
		for object in self.chess_pieces_objects:
			self.canvas.delete(object)

		# Call functions to draw the chess board
		if self.state["chess_type"] == "CHESS":
			self.draw_chess_board()
		elif self.state["chess_type"] == "XIANGQI":
			self.draw_xiangqi_board()

	def draw_chess_board(self):
		self.state["chessboard_x_array"] = 8
		self.state["chessboard_y_array"] = 8
		self.CELL_SIZE = self.BOARD_SIZE / self.state["chessboard_x_array"]
		self.TEXT_MARGIN = 20
		self.state['chess_piece_size'] = int(0.8 * self.CELL_SIZE)

		# Draw black and white squares
		for i in range(self.state["chessboard_x_array"]):
			for j in range(self.state["chessboard_y_array"]):
				cell_color = "black" if (i+j)%2 == 0 else "white"
				x = self.BOARD_MARGIN + i * self.CELL_SIZE
				y = self.BOARD_MARGIN + j * self.CELL_SIZE
				self.chess_board_objects.append(self.canvas.create_rectangle(x, y, x+self.CELL_SIZE, y+self.CELL_SIZE, fill=cell_color))
		
		# Insert alphabets and numbers for notation
		alphabets = ('a','b','c','d','e','f','g','h')
		for i in range(self.state["chessboard_x_array"]):
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, self.BOARD_MARGIN - self.TEXT_MARGIN, text=alphabets[i], font=12))
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE + self.TEXT_MARGIN, text=alphabets[i], font=12, angle=180))
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN - self.TEXT_MARGIN, self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, text=i+1, font=12))
			self.chess_board_objects.append(self.canvas.create_text(self.BOARD_MARGIN + self.BOARD_SIZE + self.TEXT_MARGIN, self.BOARD_MARGIN + (i+0.5)*self.CELL_SIZE, text=i+1, font=12, angle=180))

		# Flip y coordinates
		self.canvas.scale("all", 0, 0.5*self.state["canvas_size"], 1, -1)

	def draw_xiangqi_board(self):
		self.state["chessboard_x_array"] = 9
		self.state["chessboard_y_array"] = 10
		self.CELL_SIZE = self.BOARD_SIZE / self.state["chessboard_y_array"]
		self.TEXT_MARGIN = 50
		self.LINEWIDTH = 2
		self.state['chess_piece_size'] = int(0.8 * self.CELL_SIZE)


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
		
		# Draw bottom 'X'
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + 2.5*self.CELL_SIZE, width=self.LINEWIDTH))
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + 2.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.CELL_SIZE, width=self.LINEWIDTH))

		# Draw top 'X'
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 2.5*self.CELL_SIZE, width=self.LINEWIDTH))
		self.chess_board_objects.append(self.canvas.create_line(self.BOARD_MARGIN + 0.5*self.BOARD_SIZE - self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 2.5*self.CELL_SIZE, self.BOARD_MARGIN + 0.5*self.BOARD_SIZE + self.CELL_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE - 0.5*self.CELL_SIZE, width=self.LINEWIDTH))

		# Flip y coordinates
		self.canvas.scale("all", 0, 0.5*self.state["canvas_size"], 1, -1)
