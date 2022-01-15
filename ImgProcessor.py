import tkinter
from PIL import Image, ImageTk
import logging

import settings
MainDirectory = 'img'


class ImgProcessor:
	__instance = None
	__img = None
	def __new__(self):
		if not self.__instance:
			logging.info('Initializing singleton')
			self.__instance = super(ImgProcessor, self).__new__(self)
			self.__instance.__Initialize()
		return self.__instance

	def __Initialize(self):
		for ChessType in settings.Parameters().GetTypesOfChess():
			self.ReadChessPieceImagesFromFile(ChessType)
			self.ResizeChessPieceImages(ChessType)
	
	
	def ReadChessPieceImagesFromFile(self, ChessType):
		if self.__img == None:
			self.__img = dict()

		if ChessType not in self.__img.keys():
			self.__img[ChessType] = dict()
			DirectoryPath = MainDirectory + '/' + ChessType + '/'
			for color in settings.Parameters().GetPlayerColors(ChessType):
				for piece in settings.Parameters().GetTypesOfChessPieces(ChessType):
					ChessPiece = color + '_' + piece
					try:
						self.__img[ChessType][ChessPiece] = Image.open(DirectoryPath + ChessPiece + '.png')
					except FileNotFoundError as e:
						tkinter.messagebox.showerror('Error', e)
						exit(1)

	def ResizeChessPieceImages(self, ChessType):
		self.ReadChessPieceImagesFromFile(ChessType)
		for ChessPiece, img in self.__img[ChessType].items():
			LongerSide = img.size[0] if img.size[0] > img.size[1] else img.size[1]
			ScalingFactor = settings.Parameters().GetChessPieceSize(ChessType) / LongerSide
			ScaledSize = (int(ScalingFactor*img.size[0]), int(ScalingFactor*img.size[1]))
			self.__img[ChessType][ChessPiece] = img.resize(ScaledSize)

	
	def GetImage(self, ChessType, ChessPiece):
		return self.__img[ChessType][ChessPiece]
	def GetPhotoImage(self, ChessType, ChessPiece):
		return ImageTk.PhotoImage(self.__img[ChessType][ChessPiece])
