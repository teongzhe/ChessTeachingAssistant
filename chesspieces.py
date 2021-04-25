import tkinter

class ChessPieces:
	def __init__(self, frame, parameters, state, chessboard):
		self.frame = frame
		self.parameters = parameters
		self.state = state

		self.initialize_menu()

	def initialize_menu(self):
		for widget in self.frame.winfo_children():
			widget.destroy()

		self.add_menu()


	def add_menu(self):
		colors = self.parameters[self.state['chess_type']]['PLAYER_COLORS']
		pieces = self.parameters[self.state['chess_type']]['TYPES_OF_CHESS_PIECES']
		
		self.state['game_is_ongoing'] = True
		var = tkinter.StringVar(value='deselect')
		def callback():
			self.state['selected_piece_to_add_to_board'] = var.get()
			self.state['game_is_ongoing'] = True if var.get() == 'deselect' else False
		
		for piece in pieces:
			temp_frame = tkinter.Frame(self.frame)
			temp_frame.pack(anchor='w')
			for color in colors:
				temp_str = color + '_' + piece
				img = self.parameters[self.state['chess_type']]['IMG'][temp_str]
				radiobtn_size = self.parameters[self.state['chess_type']]['PIECE_SIZE']

				radiobtn = tkinter.Radiobutton(temp_frame, command=callback, variable=var, value=temp_str, image=img, indicatoron=0, width=radiobtn_size, height=radiobtn_size)
				radiobtn.image = img
				radiobtn.pack(side=tkinter.LEFT)

		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='remove', text='Remove').pack(anchor='w')
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='deselect', text='Deselect').pack(anchor='w')
