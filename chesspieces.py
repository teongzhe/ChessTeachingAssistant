import tkinter

class ChessPieces:
	def __init__(self, frame, state):
		self.frame = frame

		white_pawn_frame = tkinter.Frame(frame)
		white_pawn_frame.pack(side=tkinter.TOP)
		tkinter.Label(white_pawn_frame, text="White Pawn").pack(side=tkinter.LEFT)
