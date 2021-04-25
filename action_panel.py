import tkinter
import chesspieces, chessboard

class ActionPanel:
	def __init__(self, frame, state, chesspieces, chessboard):
		self.frame = frame
		self.state = state
		self.chesspieces = chesspieces
		self.chessboard = chessboard

		self.chess_type_panel()
		self.chessboard_state_panel()

	def chess_type_panel(self):
		labelFrame = tkinter.Frame(self.frame)
		labelFrame.pack(side=tkinter.TOP)
		tkinter.Label(labelFrame, text="What would you like to play today?").pack(side=tkinter.TOP)

		# Callback function and variable
		var = tkinter.StringVar(value='CHESS')
		def callback():
			if self.state['chess_type'] != var.get():
				self.state['chess_type'] = var.get()
				self.chessboard.clear_pieces_from_board()
				self.chessboard.initialize_chess_board()
				self.chesspieces.initialize_menu()
			

		R1 = tkinter.Radiobutton(self.frame, command=callback, variable=var, value="CHESS", text="Chess")
		R1.pack(anchor='w')

		R2 = tkinter.Radiobutton(self.frame, command=callback, variable=var, value="XIANGQI", text="Xiang Qi")
		R2.pack(anchor='w')

	def chessboard_state_panel(self):
		BUTTON_WIDTH = 20

		main_frame = tkinter.Frame(self.frame)
		main_frame.pack(side=tkinter.TOP)

		# Starting positions and clear board options
		tkinter.Button(main_frame, text='Starting positions', command=self.chessboard.starting_positions, width=BUTTON_WIDTH).pack(anchor='w')
		tkinter.Button(main_frame, text='Clear board', command=self.chessboard.clear_pieces_from_board, width=BUTTON_WIDTH).pack(anchor='w')
