import tkinter
from PIL import Image, ImageTk

class ChessPieces:
	def __init__(self, frame, state):
		self.frame = frame
		self.state = state

		self.initialize_menu()

	def initialize_menu(self):
		for widget in self.frame.winfo_children():
			widget.destroy()

		if self.state['chess_type'] == 'CHESS':
			self.chess_menu()
		elif self.state['chess_type'] == 'XIANGQI':
			self.xiangqi_menu()
	
	def process_png(self, chess_piece):
		# img = tkinter.PhotoImage('img/' + chess_piece + '.png')
		img = Image.open('img/' + chess_piece + '.png')

		# Scale image
		longer_side = img.size[0] if img.size[0] > img.size[1] else img.size[1]
		scaling_factor = self.state['chess_piece_size'] / longer_side
		scaled_size = (int(scaling_factor*img.size[0]), int(scaling_factor*img.size[1]))
		img = img.resize(scaled_size)

		return ImageTk.PhotoImage(img)
	
	def chess_menu(self):
		self.state['pieces'] = ('king','queen','rook','knight','bishop','pawn')
		self.state['player_colors'] = ('white','black')

		var = tkinter.StringVar(value='remove')
		def callback():
			self.state['selected_piece_to_add_to_board'] = var.get()
			print(self.state['selected_piece_to_add_to_board'])
		
		for piece in self.state['pieces']:
			temp_frame = tkinter.Frame(self.frame)
			temp_frame.pack(anchor='w')
			for color in self.state['player_colors']:
				tkinter.Radiobutton(temp_frame, command=callback, variable=var, value=color+'_'+piece, image=self.process_png(color+'_'+piece), indicatoron=0).pack(side=tkinter.LEFT)
				# tkinter.Radiobutton(temp_frame, command=callback, variable=var, value=color+'_'+piece, text=color+'_'+piece, indicatoron=0, width=15).pack(side=tkinter.LEFT)
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='remove', text='Remove').pack(anchor='w')
		
		tkinter.Label(self.frame, image = self.process_png('white_rook')).pack(anchor='w')


	def xiangqi_menu(self):
		self.state['pieces'] = ('shuai','shi','xiang','ju','ma','pao','bing')
		self.state['player_colors'] = ('red','black')
