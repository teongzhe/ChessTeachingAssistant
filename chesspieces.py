import tkinter
from PIL import ImageTk

from settings import Parameters, State
from ImgProcessor import *


class ChessPieces:
	def __init__(self, frame, chessboard, imageSize = 70):
		self.frame = frame
		self.ChessBoard = chessboard
		self.__radiobtnSize = imageSize
		self.initialize_menu()

	def initialize_menu(self):
		for widget in self.frame.winfo_children():
			widget.destroy()
		self.add_menu()

	def add_menu(self):
		ChessType = State().GetChessType()
		colors = Parameters().GetPlayerColors(ChessType)
		pieces = Parameters().GetTypesOfChessPieces(ChessType)
		
		State().SetGameIsOngoing(True)
		var = tkinter.StringVar(value='deselect')
		def callback():
			if State().GetSelectedPieceToAddToBoard() != var.get():
				if var.get() != 'deselect':
					State().ClearMoveList()
					self.ChessBoard.RemoveHighlights()

				State().SetSelectedPieceToAddToBoard(var.get())
				if var.get() == 'deselect':
					State().SetGameIsOngoing(True)
				else:
					State().SetGameIsOngoing(False)
		
		for piece in pieces:
			temp_frame = tkinter.Frame(self.frame)
			temp_frame.pack(anchor='w')
			for color in colors:
				ChessPiece = color + '_' + piece
				img = ImgProcessor().GetImage(ChessType, ChessPiece)
				longer_side = img.size[0] if img.size[0] > img.size[1] else img.size[1]
				scalingFactor = self.__radiobtnSize / longer_side
				scaled_size = (int(scalingFactor*img.size[0]), int(scalingFactor*img.size[1]))
				img = ImageTk.PhotoImage(img.resize(scaled_size))
				
				radiobtn = tkinter.Radiobutton(temp_frame, command=callback, variable=var, value=ChessPiece, image=img, indicatoron=0, width=self.__radiobtnSize, height=self.__radiobtnSize)
				radiobtn.image = img
				radiobtn.pack(side=tkinter.LEFT)

		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='remove', text='Remove').pack(anchor='w')
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='deselect', text='Deselect').pack(anchor='w')
