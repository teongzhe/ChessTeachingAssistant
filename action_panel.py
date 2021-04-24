import tkinter
import chesspieces, chessboard

class ActionPanel:
	def __init__(self, frame, state, chesspieces, chessboard):
		self.frame = frame
		self.state = state
		self.chesspieces = chesspieces
		self.chessboard = chessboard

		self.chess_type_panel()

	def chess_type_panel(self):
		save_function_frame = tkinter.Frame(self.frame)
		save_function_frame.pack(side=tkinter.TOP)
		tkinter.Label(save_function_frame, text="What would you like to play today?").pack(side=tkinter.LEFT)

		# Callback function and variable
		var = tkinter.StringVar(value='CHESS')
		def callback():
			self.state["chess_type"] = var.get()
			self.chessboard.clear_pieces_from_board()
			self.chessboard.initialize_chess_board()
			self.chesspieces.initialize_menu()
			

		R1 = tkinter.Radiobutton(self.frame, command=callback, variable=var, value="CHESS", text="Chess")
		R1.pack(anchor='w')

		R2 = tkinter.Radiobutton(self.frame, command=callback, variable=var, value="XIANGQI", text="Xiang Qi")
		R2.pack(anchor='w')
