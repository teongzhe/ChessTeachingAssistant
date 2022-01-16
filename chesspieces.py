import tkinter
from PIL import ImageTk

from settings import Parameters, State
from ImgProcessor import *


class ChessPieces:
	def __init__(self, frame, chessboard, imageSize = 50):
		self.frame = frame
		self.ChessBoard = chessboard
		self.__RadiobtnSize = imageSize
		self.InitializeMenu()

	def InitializeMenu(self):
		for widget in self.frame.winfo_children():
			widget.destroy()
		self.AddMenu()

	def AddMenu(self):
		ChessType = State().GetChessType()
		PlayerColors = Parameters().GetPlayerColors(ChessType)
		TypesOfChessPieces = Parameters().GetTypesOfChessPieces(ChessType)
		
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
		
		for piece in TypesOfChessPieces:
			RadiobtnFrame = tkinter.Frame(self.frame)
			RadiobtnFrame.pack(anchor='w')
			for PlayerColor in PlayerColors:
				ChessPieceString = PlayerColor + '_' + piece
				img = ImgProcessor().GetImage(ChessType, ChessPieceString)
				LongerSide = img.size[0] if img.size[0] > img.size[1] else img.size[1]
				ScalingFactor = self.__RadiobtnSize / LongerSide
				ScaledSize = (int(ScalingFactor*img.size[0]), int(ScalingFactor*img.size[1]))
				img = ImageTk.PhotoImage(img.resize(ScaledSize))
				
				Radiobtn = tkinter.Radiobutton(RadiobtnFrame, command=callback, variable=var, value=ChessPieceString, image=img, indicatoron=0, width=self.__RadiobtnSize, height=self.__RadiobtnSize)
				Radiobtn.image = img
				Radiobtn.pack(side=tkinter.LEFT)
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='remove', text='Remove').pack(anchor='w')
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='deselect', text='Deselect').pack(anchor='w')
