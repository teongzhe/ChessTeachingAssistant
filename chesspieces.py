import tkinter
from PIL import Image, ImageTk

class ChessPieces:
	def __init__(self, frame, state, chessboard):
		self.frame = frame
		self.state = state

		self.read_img()
		self.initialize_menu()


	def read_img(self):
		def process_png(chess_piece):
			img = Image.open('img/' + chess_piece + '.png')

			# Scale image
			longer_side = img.size[0] if img.size[0] > img.size[1] else img.size[1]
			scaling_factor = self.state['chess_piece_size'] / longer_side
			scaled_size = (int(scaling_factor*img.size[0]), int(scaling_factor*img.size[1]))
			img = img.resize(scaled_size)

			return ImageTk.PhotoImage(img)

		# Initialize dictionary
		self.state['img'] = dict()
		self.state['player_colors'] = dict()
		self.state['types_of_chess_pieces'] = dict()

		# Read img for chess pieces
		self.state['img']['CHESS'] = dict()
		self.state['player_colors']['CHESS'] = ('white','black')
		self.state['types_of_chess_pieces']['CHESS'] = ('king','queen','rook','knight','bishop','pawn')

		for color in self.state['player_colors']['CHESS']:
			for piece in self.state['types_of_chess_pieces']['CHESS']:
				temp_str = color + '_' + piece
				self.state['img']['CHESS'][temp_str] = process_png(temp_str)

		# Read img for xiangqi pieces
		self.state['player_colors']['XIANGQI'] = ('red','black')
		self.state['types_of_chess_pieces']['XIANGQI'] = ('shuai', 'shi', 'xiang', 'ju', 'ma', 'pao', 'bing')


	def initialize_menu(self):
		for widget in self.frame.winfo_children():
			widget.destroy()

		if self.state['chess_type'] == 'CHESS':
			self.chess_menu()
		elif self.state['chess_type'] == 'XIANGQI':
			self.xiangqi_menu()


	def chess_menu(self):
		colors = self.state['player_colors']['CHESS']
		pieces = self.state['types_of_chess_pieces']['CHESS']
		
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
				img = self.state['img']['CHESS'][temp_str]

				radiobtn = tkinter.Radiobutton(temp_frame, command=callback, variable=var, value=temp_str, image=img, indicatoron=0, width=self.state['chess_piece_size'], height=self.state['chess_piece_size'])
				radiobtn.image = img
				radiobtn.pack(side=tkinter.LEFT)

		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='remove', text='Remove').pack(anchor='w')
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='deselect', text='Deselect').pack(anchor='w')


	def xiangqi_menu(self):
		print('Not implemented yet')
